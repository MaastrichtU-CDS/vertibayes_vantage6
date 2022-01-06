import requests
from typing import Any, Dict, Tuple

from vantage6.tools.util import info
from time import sleep
import traceback

RETRY = 10

def shareEndpoints(client, data, exclude_orgs=None, **kwargs):
    try:
        return _try_set_endpoints(client, exclude_orgs, kwargs.get("task_id"))
    except Exception as e:
        info('Exception!')
        info(traceback.format_exc())
        raise e

def killEndpoints(client, data, exclude_orgs=None, **kwargs):
    try:
        _try_kill_endpoints(client, exclude_orgs, kwargs.get("task_id"))
    except Exception as e:
        info('Excetpion!')
        info(traceback.format_exc())
        raise e

def getEndpoints(client, data, exclude_orgs=None, **kwargs):
    try:
        _try_get_endpoints(client, exclude_orgs, kwargs.get("task_id"))
    except Exception as e:
        info('Excetpion!')
        info(traceback.format_exc())
        raise e

def _try_get_endpoints(client, exclude_orgs, task_id):
    task = client.get_task(task_id)

    # Ip address and port of algorithm can be found in results model
    return _await_port_numbers(client, task.get('id'))


def _try_kill_endpoints(client, exclude_orgs, task_id):
    task = client.get_task(task_id)

    # Ip address and port of algorithm can be found in results model
    result_objects = _await_port_numbers(client, task.get('id'))

    for i in range(len(result_objects)):
        target = result_objects[i]
        _kill_endpoint(target)



def _try_set_endpoints(client, exclude_orgs, task_id):
    task = client.get_task(task_id)

    # Ip address and port of algorithm can be found in results model
    result_objects = _await_port_numbers(client, task.get('id'))

    for i in range(len(result_objects)):
        target = result_objects[i]
        others = result_objects[~i]

        info(f'Sending message')
        _set_endpoints(target, others)


def _await_port_numbers(client, task_id):
    result_objects = client.get_other_node_ip_and_port(task_id=task_id)

    c = 0
    while not _are_ports_available(result_objects):
        if c >= RETRY:
            raise Exception('Retried too many times')

        info('Polling results for port numbers...')
        result_objects = client.get_other_node_ip_and_port(task_id=task_id)
        c += 1
        sleep(4)

    return result_objects


def _are_ports_available(result_objects):
    for r in result_objects:
        _, port = _get_address_from_result(r)
        if not port:
            return False

    return True


def _get_address_from_result(result: Dict[str, Any]) -> Tuple[str, int]:
    address = result['ip']
    port = result['port']

    return address, port

def _set_endpoints(target, endpoints):
    target_ip, target_port = _get_address_from_result(target)
    others = []
    targetUrl = "http://"+target_ip+":"+target_port
    for e in endpoints:
        other_ip, other_port = _get_address_from_result(e)
        others.append("http://"+other_ip+":"+other_port)


    r = requests.put(targetUrl+"/setEndpoints", json={
        "servers":others
    })

    return r.json()

def _kill_endpoint(target):
    target_ip, target_port = _get_address_from_result(target)
    targetUrl = "http://"+target_ip+":"+target_port
    r = requests.put(targetUrl+"/kill")