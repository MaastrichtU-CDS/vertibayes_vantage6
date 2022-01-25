import time
from typing import List

import requests
from vantage6.common import info

from com.florian import urlcollector
from com.florian.vertibayes import secondary
from com.florian.vertibayes.bayes.VertiBayes import VertiBayes

WAIT = 10
RETRY = 20
IMAGE = 'carrrier-harbor.carrier-mu.src.surf-hosted.nl/carrier/vertibayes'


def vertibayes(client, data, node1, node2, initial_network, population, *args, **kwargs):
        """
    
        :param client:
        :param exclude_orgs:
        :param node1: organization id of node 1
        :param node2: organization id of node 2
        :param commoditynode: organization id of commodity node
        :return:
        """
        info('logging something to see if my chances actually get in')

        # ToDo make this run with an arbitrary number of nodes
        # TODO: init node 1
        info('Initializing node 1')
        node1_task = _initEndpoints(client, [node1])

        # TODO: init node 2
        info('Initializing node 2')
        node2_task = _initEndpoints(client, [node2])
        # TODO: init commodity server?
        info('initializing commodity server')
        commodity_node_task = secondary.init_local()

        info('logging something to see if my chances actually get in')
        # TODO: Async would be more efficient
        node1_address = _await_addresses(client, node1_task["id"])[0]
        info(f'Node 1 address: {node1_address}')
        node2_address = _await_addresses(client, node2_task["id"])[0]
        info(f'Node 2 address: {node2_address}')

        #assuming the last taks before node1_task controls the commodity server
        #Assumption is basically that noone got in between the starting of this master-task and its subtasks
        #ToDo make this more stable in case of multiple users
        global_commodity_address = _await_addresses(client, node1_task["id"]-1)[0]

        # Assuming commodity server is on same machine
        commodity_address = _http_url('localhost', 8888)
        info(f'Commodity address: {commodity_address}')

        # wait a moment for Spring to start
        info('Waiting for spring to start...')
        _wait()

        #set ids
        _setId(commodity_address, "0");
        _setId(node1_address, "1");
        _setId(node2_address, "2");
        info('Sharing addresses with node 1')
        urlcollector.put_endpoints(node1_address, [node2_address, global_commodity_address])

        info('Sharing addresses with node 2')
        urlcollector.put_endpoints(node2_address, [node1_address, global_commodity_address])

        _initCentralServer(commodity_address, [node1_address, node2_address])

        jsonNodes = _trainBayes(commodity_address, initial_network)

        info('Commiting murder')
        # Committing murder results in crashes in vantage6
        # Spring gets killed correctly, but vantage6 doesn't like the image closing without a response
        # ToDo fix this, somehow
        _killSpring(node1_address)
        _killSpring(node2_address)

        vertibayes = VertiBayes(population, jsonNodes)
        vertibayes.defineLocalNetwork()
        vertibayes.trainNetwork()
        info(f'Bif: {vertibayes.toBif()}')
        return vertibayes.toBif()


def _trainBayes(targetUrl, initial_network):
    r = requests.post(targetUrl + "/maximumLikelyhood", json={
        "nodes": initial_network
    })

    return r.json()


def _initCentralServer(central: str, others: List[str]):
    r = requests.post(central + "/initCentralServer", json={
        "secretServer": central,
        "servers": others
    })

    if not r.ok:
        raise Exception("Could not initialize central server")

def _killSpring(server: str):
    try:
        r = requests.put(server + "/kill")
    except Exception as e:
        # We expect an error here
        info(e)
        pass

def _setId(ip: str, id:str):
    r = requests.post(ip + "/setID?id="+id)

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

def _await_addresses(client, task_id, n_nodes=1):
    addresses = client.get_other_node_ip_and_port(task_id=task_id)

    c = 0
    while not _addresses_complete(addresses):
        if c >= RETRY:
            raise Exception('Retried too many times')

        info(f'Polling results for port numbers attempt {c}...')
        addresses = client.get_other_node_ip_and_port(task_id=task_id)
        c += 1
        time.sleep(WAIT)

    return [_http_url(address['ip'], address['port']) for address in addresses]


def _addresses_complete(addresses):
    for a in addresses:
        if not a['port']:
            return False

    return True


def _http_url(address: str, port: int):
    return f'http://{address}:{port}'
