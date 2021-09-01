
import requests

from common.settings import Node_Settings
from common.node import json_destruct_node

# local requests


def local_retrieve_nodes(settings: Node_Settings):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/nodes/", json=settings.json_node).json()


def local_add_node(settings: Node_Settings, json_node: dict):
    return requests.post("http://" + str(json_destruct_node(settings.json_node)) + "/nodes/", json=json_node).json()


def local_remove_node(settings: Node_Settings, json_node: dict):
    return requests.delete("http://" + str(json_destruct_node(settings.json_node)) + "/nodes/", json=json_node).json()

# general requests


def general_connection_check(target_node: dict, opt_json_node: dict = {}):
    return requests.post("http://" + str(json_destruct_node(target_node)) + "/", json=opt_json_node).json()


def general_retrieve_nodes(target_node: dict, opt_json_node: dict = {}):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/nodes/", json=opt_json_node).json()


def general_add_node(target_node: dict, json_node: dict):
    return requests.post("http://" + str(json_destruct_node(target_node)) + "/nodes/", json=json_node).json()


def general_remove_node(target_node: dict, json_node: dict):
    return requests.delete("http://" + json_destruct_node(target_node) + "/nodes/", json=json_node).json()
