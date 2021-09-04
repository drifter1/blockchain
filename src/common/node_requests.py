
from common.settings import Node_Settings
from common.requests import general_delete_request, general_get_request, general_post_request, local_delete_request, local_get_request, local_post_request


# local requests

def local_retrieve_nodes(settings: Node_Settings):
    return local_get_request(settings, "/nodes/", {})


def local_add_node(settings: Node_Settings, json_node: dict):
    return local_post_request(settings, "/nodes/", json_node)


def local_remove_node(settings: Node_Settings, json_node: dict):
    return local_delete_request(settings, "/nodes/", json_node)


# general requests

def general_connection_check(settings: Node_Settings, target_node: dict, opt_json_node: dict = {}):
    return general_post_request(settings, target_node, "/nodes/", opt_json_node)


def general_retrieve_nodes(settings: Node_Settings, target_node: dict, opt_json_node: dict = {}):
    return general_get_request(settings, target_node, "/nodes/", opt_json_node)


def general_add_node(settings: Node_Settings, target_node: dict, json_node: dict):
    return general_post_request(settings, target_node, "/nodes/", json_node)


def general_remove_node(settings: Node_Settings, target_node: dict, json_node: dict):
    return general_delete_request(settings, target_node, "/nodes/", json_node)
