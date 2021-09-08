
from common.settings import Node_Settings
from common.requests import general_delete_request, general_get_request, general_post_request, local_get_request, local_post_request, local_delete_request


# local requests

def local_retrieve_transactions_header(settings: Node_Settings):
    return local_get_request(settings, "/transactions/", {})


def local_retrieve_transaction(settings: Node_Settings, tid: str):
    url_path = "/transactions/" + str(tid) + "/"
    return local_get_request(settings, url_path, {})


def local_post_transaction(settings: Node_Settings, json_transaction: dict):
    return local_post_request(settings, "/transactions/", json_transaction)


def local_remove_transaction(settings: Node_Settings, json_transaction: dict):
    return local_delete_request(settings, "/transactions/", json_transaction)

# general requests


def general_retrieve_transactions_header(settings: Node_Settings, target_node: dict):
    return general_get_request(settings, target_node, "/transactions/", {})


def general_retrieve_transaction(settings: Node_Settings, target_node: dict, tid: str):
    url_path = "/transactions/" + str(tid) + "/"
    return general_get_request(settings, target_node, url_path, {})


def general_post_transaction(settings: Node_Settings, target_node: dict, json_transaction: dict):
    return general_post_request(settings, target_node, "/transactions/", json_transaction)


def general_remove_transaction(settings: Node_Settings, target_node: dict, json_transaction: dict):
    return general_delete_request(settings, target_node, "/transactions/", json_transaction)
