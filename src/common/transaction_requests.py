import requests

from common.settings import Node_Settings
from common.node import json_destruct_node


# local requests

def local_retrieve_transactions(settings: Node_Settings):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/transactions/").json()


def local_post_transaction(settings: Node_Settings, json_transaction: dict):
    return requests.post("http://" + str(json_destruct_node(settings.json_node)) + "/transactions/", json=json_transaction).json()


def local_remove_transaction(settings: Node_Settings, json_transaction: dict):
    return requests.delete("http://" + str(json_destruct_node(settings.json_node)) + "/transactions/", json=json_transaction).json()

# general requests


def general_retrieve_transactions(target_node: dict):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/transactions/").json()


def general_post_transaction(target_node: dict, json_transaction: dict):
    return requests.post("http://" + str(json_destruct_node(target_node)) + "/transactions/", json=json_transaction).json()


def general_remove_transaction(target_node: dict, json_transaction: dict):
    return requests.delete("http://" + str(json_destruct_node(target_node)) + "/transactions/", json=json_transaction).json()
