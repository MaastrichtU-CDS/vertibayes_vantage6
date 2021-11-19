import time
from typing import Any
from typing import Dict
from typing import Tuple

import requests
import vantage6

WAIT = 10

def vertibayes(client, data, exclude_orgs=None, **kwargs):
    n2nTask = _initEndpoints(client, exclude_orgs)
    ## wait a moment for Spring to start
    _wait()
    _shareEndpoints(client, exclude_orgs, n2nTask.id)

    target = _getCentralIP(n2nTask.id)
    network = _trainBayes(target, kwargs.get('network'))


def _synthesizeData(network):


def _trainLocalBayes(network, data):


def _trainBayes(target, nodes):
    target_ip, target_port = _get_address_from_result(target)
    others = []
    targetUrl = "http://"+target_ip+":"+target_port

    r = requests.get(targetUrl+"/maximumLikelyhood", json={
        "nodes":nodes
    })

    return r.json()

def _get_address_from_result(result: Dict[str, Any]) -> Tuple[str, int]:
    address = result['ip']
    port = result['port']

    return address, port

def _getCentralIP(id):
    # somehow get only the IP of the node assigned to play the role of commodity server
    return ''



def _shareEndpoints(client, exclude_orgs, id):
    # share endpoints amongst the n2n setup
    task = client.post_task(
        name="urlCollector",
        image="docker build -t carrier-harbor2.carrier-mu.surf-hosted.nl/florian-project/urlCollector",
        collaboration_id=1,
        input_={'method': 'shareEndpoints', 'master': True,
                'kwargs': {"task_id": id, 'exclude_orgs': exclude_orgs}},
        organization_ids=[1]
    )


def _initEndpoints(client, exclude_orgs):
    #start the various java endpoints for n2n
    return client.post_task(
        name="vertiBayesSpring",
        image="docker build -t carrier-harbor2.carrier-mu.surf-hosted.nl/florian-project/vertibayes",
        collaboration_id=1,
        input_={'method': 'init', 'master': True,
                'kwargs': {'exclude_orgs': exclude_orgs}},
        organization_ids=[1]
    )

def _wait():
    time.sleep(WAIT)