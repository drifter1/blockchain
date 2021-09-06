
from common.settings import Node_Settings
from common.requests import local_get_request, local_put_request, general_get_request, general_put_request

# local requests


def local_retrieve_blockchain_info(settings: Node_Settings):
    return local_get_request(settings, "/blockchain/", {})


def local_update_blockchain_info(settings: Node_Settings, json_blockchain_info: dict):
    return local_put_request(settings, "/blockchain/", json_blockchain_info)

# general requests


def general_retrieve_blockchain_info(settings: Node_Settings, target_node: dict):
    return general_get_request(settings, target_node, "/blockchain/", {})


def general_update_blockchain_info(settings: Node_Settings, target_node: dict, json_blockchain_info: dict):
    return general_put_request(settings, target_node, "/blockchain/", json_blockchain_info)
