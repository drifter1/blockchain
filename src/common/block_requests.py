
from common.settings import Node_Settings
from common.requests import local_get_request, local_post_request, general_get_request, general_post_request

# local requests


def local_retrieve_block_header(settings: Node_Settings, bid: int):
    url_path = "/blocks/" + str(bid) + "/"
    return local_get_request(settings, url_path, {})


def local_retrieve_last_block_header(settings: Node_Settings):
    return local_get_request(settings, "/blocks/last/", {})


def local_retrieve_block_transactions_header(settings: Node_Settings, bid: int):
    url_path = "/blocks/" + str(bid) + "/transactions/"
    return local_get_request(settings, url_path, {})


def local_retrieve_block_transaction(settings: Node_Settings, bid: int, tid: int):
    url_path = "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/"
    return local_get_request(settings, url_path, {})


def local_retrieve_block_transaction_inputs(settings: Node_Settings, bid: int, tid: int):
    url_path = "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/inputs/"
    return local_get_request(settings, url_path, {})


def local_retrieve_block_transaction_input(settings: Node_Settings, bid: int, tid: int, iid: int):
    url_path = "/blocks/" + str(bid) + "/transactions/" + \
        str(tid) + "/inputs/" + str(iid) + "/"
    return local_get_request(settings, url_path, {})


def local_retrieve_block_transaction_outputs(settings: Node_Settings, bid: int, tid: int):
    url_path = "/blocks/" + \
        str(bid) + "/transactions/" + str(tid) + "/outputs/"
    return local_get_request(settings, url_path, {})


def local_retrieve_block_transaction_output(settings: Node_Settings, bid: int, tid: int, oid: int):
    url_path = "/blocks/" + str(bid) + "/transactions/" + \
        str(tid) + "/outputs/" + str(oid) + "/"
    return local_get_request(settings, url_path, {})


def local_create_block(settings: Node_Settings, json_block: dict):
    return local_post_request(settings, "/blocks/", json_block)

# general requests


def general_retrieve_block_header(settings: Node_Settings, target_node: dict, bid: int):
    url_path = "/blocks/" + str(bid) + "/"
    return general_get_request(settings, target_node, url_path, {})


def general_retrieve_last_block_header(settings: Node_Settings, target_node: dict):
    return general_get_request(settings, target_node, "/blocks/last/", {})


def general_retrieve_block_transactions_header(settings: Node_Settings, target_node: dict, bid: int):
    url_path = "/blocks/" + str(bid) + "/transactions/"
    return general_get_request(settings, target_node, url_path, {})


def general_retrieve_block_transaction(settings: Node_Settings, target_node: dict, bid: int, tid: int):
    url_path = "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/"
    return general_get_request(settings, target_node, url_path, {})


def general_retrieve_block_transaction_inputs(settings: Node_Settings, target_node: dict, bid: int, tid: int):
    url_path = "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/inputs/"
    return general_get_request(settings, target_node, url_path, {})


def general_retrieve_block_transaction_input(settings: Node_Settings, target_node: dict, bid: int, tid: int, iid: int):
    url_path = "/blocks/" + str(bid) + "/transactions/" + \
        str(tid) + "/inputs/" + str(iid) + "/"
    return general_get_request(settings, target_node, url_path, {})


def general_retrieve_block_transaction_outputs(settings: Node_Settings, target_node: dict, bid: int, tid: int):
    url_path = "/blocks/" + \
        str(bid) + "/transactions/" + str(tid) + "/outputs/"
    return general_get_request(settings, target_node, url_path, {})


def general_retrieve_block_transaction_output(settings: Node_Settings, target_node: dict, bid: int, tid: int, oid: int):
    url_path = "/blocks/" + str(bid) + "/transactions/" + \
        str(tid) + "/outputs/" + str(oid) + "/"
    return general_get_request(settings, target_node, url_path, {})


def general_create_block(settings: Node_Settings, target_node: dict, json_block: dict):
    return general_post_request(settings, target_node, "/blocks/", json_block)
