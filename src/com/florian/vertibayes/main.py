import time
from typing import Any, List
from typing import Dict
from typing import Tuple

import requests
from vantage6.common import info

from com.florian.vertibayes.bayes.VertiBayes import VertiBayes
from com.florian import urlcollector

WAIT = 10
RETRY = 10
IMAGE = 'carrrier-harbor.carrier-mu.src.surf-hosted.nl/carrier/vertibayes'

def vertibayes(client, data, node1, node2, commodity_node, *args, **kwargs):
    """

    :param client:
    :param exclude_orgs:
    :param node1: organization id of node 1
    :param node2: organization id of node 2
    :param commoditynode: organization id of commodity node
    :return:
    """
    # TODO: init node 1
    info('Initializing node 1')
    node1_task = _initEndpoints(client, node1)

    # TODO: init node 2
    info('Initializing node 2')
    node2_task = _initEndpoints(client, node2)
    # TODO: init commodity server?
    info('initializing commodity server')
    commodity_node_task = _initEndpoints(client, commodity_node)

    # TODO: Async would be more efficient
    node1_address = _await_addresses(client, node1_task["id"])[0]
    node2_address = _await_addresses(client, node2_task["id"])[0]
    commodity_address = _await_addresses(client, commodity_node_task["id"])[0]

    # wait a moment for Spring to start
    _wait()

    urlcollector.put_endpoints(node1_address, [node2_address])
    urlcollector.put_endpoints(node2_address, [node1_address])

    _initCentralServer(commodity_address, [node1_address, node2_address])

    return {}

    # jsonNodes = _trainBayes(central, kwargs.get('nodes'))
    # vertibayes = VertiBayes(kwargs.get('population'), jsonNodes)
    # vertibayes.defineLocalNetwork()
    # vertibayes.trainNetwork()
    #
    # return vertibayes.getNetwork()


# def _trainBayes(target, nodes):
#     target_ip, target_port = _get_address_from_result(target)
#
#     targetUrl = "http://" + target_ip + ":" + target_port
#
#     r = requests.get(targetUrl + "/maximumLikelyhood", json={
#         "nodes": nodes
#     })
#
#     return r.json()


def _initCentralServer(central: str, others: List[str]):
    r = requests.get(central + "/initCentralServer", json={
        "secretServer": central,
        "servers": others
    })

    if not r.ok:
        raise Exception("Could not initialize central server")


def _initEndpoints(client, organizations):
    # start the various java endpoints for n2n
    return client.post_task(
        name="vertiBayesSpring",
        image=IMAGE,
        collaboration_id=1,
        input_={'method': 'init'},
        organization_ids=organizations
    )


def _wait():
    time.sleep(WAIT)


def _killEndpoints(client, exclude_orgs):
    # kill the various java endpoints for n2n
    task = client.post_task(
        name="urlCollector",
        image="carrier-harbor2.carrier-mu.surf-hosted.nl/florian-project/urlCollector",
        collaboration_id=1,
        input_={'method': 'killEndpoints', 'master': True,
                'kwargs': {"task_id": id, 'exclude_orgs': exclude_orgs}},
        organization_ids=client.get('organization_ids')
    )


def _await_addresses(client, task_id, n_nodes=1):
    addresses = client.get_other_node_ip_and_port(task_id=task_id)

    c = 0
    while not len(addresses) == n_nodes:
        if c >= RETRY:
            raise Exception('Retried too many times')

        info('Polling results for port numbers...')
        addresses = client.get_other_node_ip_and_port(task_id=task_id)
        c += 1
        time.sleep(4)

    return [_http_url(address['ip'], address['port']) for address in addresses]


def _http_url(address: str, port: int):
    return f'http://{address}:{port}'
