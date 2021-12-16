import time
from typing import Any
from typing import Dict
from typing import Tuple

import requests

from com.florian.vertibayes.bayes.VertiBayes import VertiBayes

WAIT = 10


def vertibayes(client, data, exclude_orgs=None, **kwargs):
    n2nTask = _initEndpoints(client, exclude_orgs)
    ## wait a moment for Spring to start
    _wait()
    _shareEndpoints(client, exclude_orgs, n2nTask.id)

    # collect central and other ipadresses cuz I need to somehow select who central is
    central = _getIPAdresses(client, n2nTask.id, [kwargs.get('commodityServer')])
    organisations = client.get('organization_ids') - kwargs.get('commodityServer')
    others = _getIPAdresses(client, n2nTask.id, organisations)

    _initCentralServer(central, others)

    jsonNodes = _trainBayes(central, kwargs.get('nodes'))
    vertibayes = VertiBayes(kwargs.get('population'), jsonNodes)
    vertibayes.defineLocalNetwork()
    vertibayes.trainNetwork()

    return vertibayes.getNetwork()


def _trainBayes(target, nodes):
    target_ip, target_port = _get_address_from_result(target)

    targetUrl = "http://" + target_ip + ":" + target_port

    r = requests.get(targetUrl + "/maximumLikelyhood", json={
        "nodes": nodes
    })

    return r.json()


def _initCentralServer(central, others):
    target_ip, target_port = _get_address_from_result(central)
    servers = []
    for i in range(len(others)):
        server_ip, server_port = _get_address_from_result(others[i])
        servers.append("http://" + server_ip + ":" + server_port)

    targetUrl = "http://" + target_ip + ":" + target_port

    r = requests.get(targetUrl + "/initCentralServer", json={
        "secretServer": targetUrl,
        "servers": servers
    })


def _get_address_from_result(result: Dict[str, Any]) -> Tuple[str, int]:
    address = result['ip']
    port = result['port']

    return address, port


def _getIPAdresses(client, id, organisations):
    # somehow get only the IP of the node assigned to play the role of commodity server
    task = client.post_task(
        name="urlcollector",
        image="carrier-harbor2.carrier-mu.surf-hosted.nl/florian-project/urlCollector",
        collaboration_id=1,
        input_={'method': 'getEndpoints', 'master': True,
                'kwargs': {"task_id": id, 'exclude_orgs': []}},
        organization_ids=organisations
    )
    return


def _shareEndpoints(client, exclude_orgs, id):
    # TODO: import urlcollector
    # share endpoints amongst the n2n setup
    task = client.post_task(
        name="urlCollector",
        image="carrier-harbor2.carrier-mu.surf-hosted.nl/florian-project/urlCollector",
        collaboration_id=1,
        input_={'method': 'shareEndpoints', 'master': True,
                'kwargs': {"task_id": id, 'exclude_orgs': exclude_orgs}},
        organization_ids=client.get('organization_ids')
    )


def _initEndpoints(client, exclude_orgs):
    # start the various java endpoints for n2n
    return client.post_task(
        name="vertiBayesSpring",
        image="carrier-harbor2.carrier-mu.surf-hosted.nl/florian-project/vertibayes",
        collaboration_id=1,
        input_={'method': 'init', 'master': True,
                'kwargs': {'exclude_orgs': exclude_orgs}},
        organization_ids=client.get('organization_ids')
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
