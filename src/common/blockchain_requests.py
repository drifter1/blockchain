import requests

from common.settings import Node_Settings
from common.node import json_destruct_node

# local requests


def local_retrieve_blockchain_info(settings: Node_Settings):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/blockchain/").json()


def local_update_blockchain_info(settings: Node_Settings, json_blockchain_info: dict):
    return requests.put("http://" + str(json_destruct_node(settings.json_node)) + "/blockchain/", json=json_blockchain_info).json()

# general requests


def global_retrieve_blockchain_info(target_node: dict):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/blockchain/").json()


def global_update_blockchain_info(target_node: dict, json_blockchain_info: dict):
    return requests.put("http://" + str(json_destruct_node(target_node)) + "/blockchain/", json=json_blockchain_info).json()
