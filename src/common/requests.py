import requests

from common.settings import Node_Settings
from common.node import json_destruct_node

# local requests


def local_get_request(settings: Node_Settings, url_path: str, json_data: dict):

    return general_get_request(settings, settings.json_node, url_path, json_data)


def local_post_request(settings: Node_Settings, url_path: str, json_data: dict):

    return general_post_request(settings, settings.json_node, url_path, json_data)


def local_put_request(settings: Node_Settings, url_path: str, json_data: dict):

    return general_put_request(settings, settings.json_node, url_path, json_data)


def local_delete_request(settings: Node_Settings, url_path: str, json_data: dict):

    return general_delete_request(settings, settings.json_node, url_path, json_data)

# general requests


def general_get_request(settings: Node_Settings, target_node: dict, url_path: str, json_data: dict) -> tuple[dict, int]:
    endpoint_url = "http://" + str(json_destruct_node(target_node)) + url_path

    try:
        response = requests.get(url=endpoint_url, json=json_data,
                                timeout=settings.request_timeout)
    except:
        return {}, 400

    return response.json(), response.status_code


def general_post_request(settings: Node_Settings, target_node: dict, url_path: str, json_data: dict) -> tuple[dict, int]:
    endpoint_url = "http://" + str(json_destruct_node(target_node)) + url_path

    try:
        response = requests.post(url=endpoint_url, json=json_data,
                                 timeout=settings.request_timeout)
    except:
        return {}, 400

    return response.json(), response.status_code


def general_put_request(settings: Node_Settings, target_node: dict, url_path: str, json_data: dict) -> tuple[dict, int]:
    endpoint_url = "http://" + str(json_destruct_node(target_node)) + url_path

    try:
        response = requests.put(url=endpoint_url, json=json_data,
                                timeout=settings.request_timeout)
    except:
        return {}, 400

    return response.json(), response.status_code


def general_delete_request(settings: Node_Settings, target_node: dict, url_path: str, json_data: dict) -> tuple[dict, int]:
    endpoint_url = "http://" + str(json_destruct_node(target_node)) + url_path

    try:
        response = requests.delete(url=endpoint_url, json=json_data,
                                   timeout=settings.request_timeout)
    except:
        return {}, 400

    return response.json(), response.status_code
