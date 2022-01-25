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


def vertibayes(client, data, nodes, initial_network, population, *args, **kwargs):
        """
    
        :param client:
        :param exclude_orgs:
        :param node1: organization id of node 1
        :param node2: organization id of node 2
        :param commoditynode: organization id of commodity node
        :return:
        """
        tasks = []
        info('Initializing nodes')
        for node in nodes:
            tasks.append(_initEndpoints(client, [node]))

        # TODO: init commodity server on a different server?
        info('initializing commodity server')
        commodity_node_task = secondary.init_local()

        adresses = []
        for task in tasks:
            adresses.append(_await_addresses(client, task["id"])[0])

        #assuming the last taks before tasks[0] controls the commodity server
        #Assumption is basically that noone got in between the starting of this master-task and its subtasks
        #ToDo make this more stable in case of multiple users
        global_commodity_address = _await_addresses(client, tasks[0]["id"]-1)[0]

        # Assuming commodity server is on same machine
        commodity_address = _http_url('localhost', 8888)
        info(f'Commodity address: {commodity_address}')

        # wait a moment for Spring to start
        info('Waiting for spring to start...')
        _wait()

        info('Sharing addresses & setting ids')
        _setId(commodity_address, "0");
        id = 1
        for adress in adresses:
            _setId(adress, str(id));
            id+=1
            others = adresses.copy()
            others.remove(adress)
            others.append(global_commodity_address)
            urlcollector.put_endpoints(adress, others)

        _initCentralServer(commodity_address, adresses)

        jsonNodes = _trainBayes(commodity_address, initial_network)

        info('Commiting murder')
        for adress in adresses:
            _killSpring(adress)

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
