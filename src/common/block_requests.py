import requests

from common.settings import Node_Settings
from common.node import json_destruct_node

# local requests


def local_retrieve_block(settings: Node_Settings, bid: int):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/blocks/" + str(bid) + "/").json()


def local_retrieve_block_transactions(settings: Node_Settings, bid: int):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/blocks/" + str(bid) + "/transactions/").json()


def local_retrieve_block_transaction(settings: Node_Settings, bid: int, tid: int):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/").json()


def local_retrieve_block_transaction_inputs(settings: Node_Settings, bid: int, tid: int):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/inputs/").json()


def local_retrieve_block_transaction_input(settings: Node_Settings, bid: int, tid: int, iid: int):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/inputs/" + str(iid) + "/").json()


def local_retrieve_block_transaction_outputs(settings: Node_Settings, bid: int, tid: int):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/outputs/").json()


def local_retrieve_block_transaction_output(settings: Node_Settings, bid: int, tid: int, oid: int):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/outputs/" + str(oid) + "/").json()


def local_create_block(settings: Node_Settings, json_block: dict):
    return requests.post("http://" + str(json_destruct_node(settings.json_node)) + "/blocks/", json=json_block).json()

# general requests


def general_retrieve_block(target_node: dict, bid: int):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/blocks/" + str(bid) + "/").json()


def general_retrieve_block_transactions(target_node: dict, bid: int):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/blocks/" + str(bid) + "/transactions/").json()


def general_retrieve_block_transaction(target_node: dict, bid: int, tid: int):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/").json()


def general_retrieve_block_transaction_inputs(target_node: dict, bid: int, tid: int):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/inputs/").json()


def general_retrieve_block_transaction_input(target_node: dict, bid: int, tid: int, iid: int):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/inputs/" + str(iid) + "/").json()


def general_retrieve_block_transaction_outputs(target_node: dict, bid: int, tid: int):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/outputs/").json()


def general_retrieve_block_transaction_output(target_node: dict, bid: int, tid: int, oid: int):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/outputs/" + str(oid) + "/").json()


def general_create_block(target_node: dict, json_block: dict):
    return requests.post("http://" + str(json_destruct_node(target_node)) + "/blocks/", json=json_block).json()
