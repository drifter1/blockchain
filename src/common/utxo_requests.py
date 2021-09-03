import requests

from common.settings import Node_Settings
from common.node import json_destruct_node

# local requests


def local_retrieve_utxo_address(settings: Node_Settings, address: str):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/utxo/" + address + "/").json()


def local_retrieve_utxo_outputs_of_address(settings: Node_Settings, address: str):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/utxo/" + address + "/outputs/").json()


def local_retrieve_utxo_output_from_address_and_transaction_hash(settings: Node_Settings, address: str, transaction_hash: str):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/utxo/" + address + "/outputs/" + transaction_hash + "/").json()


def local_create_utxo(settings: Node_Settings, address: str, opt_json_utxo: dict = {}):
    return requests.post("http://" + str(json_destruct_node(settings.json_node)) + "/utxo/" + address + "/", json=opt_json_utxo).json()


def local_add_utxo_output(settings: Node_Settings, address: str, json_utxo_output: dict):
    return requests.post("http://" + str(json_destruct_node(settings.json_node)) + "/utxo/" + address + "/outputs/", json=json_utxo_output).json()


def local_remove_utxo_output(settings: Node_Settings, address: str, json_utxo_output: dict):
    return requests.delete("http://" + str(json_destruct_node(settings.json_node)) + "/utxo/" + address + "/outputs/", json=json_utxo_output).json()


# general requests

def general_retrieve_utxo_address(target_node: dict, address: str):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/utxo/" + address + "/").json()


def general_retrieve_utxo_outputs_of_address(target_node: dict, address: str):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/utxo/" + address + "/outputs/").json()


def general_retrieve_utxo_output_from_address_and_transaction_hash(target_node: dict, address: str, transaction_hash: str):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/utxo/" + address + "/outputs/" + transaction_hash + "/").json()


def general_create_utxo(target_node: dict, address: str, opt_json_utxo: dict = {}):
    return requests.post("http://" + str(json_destruct_node(target_node)) + "/utxo/" + address + "/", json=opt_json_utxo).json()


def general_add_utxo_output(target_node: dict, address: str, json_utxo_output: dict):
    return requests.post("http://" + str(json_destruct_node(target_node)) + "/utxo/" + address + "/outputs/", json=json_utxo_output).json()


def general_remove_utxo_output(target_node: dict, address: str, json_utxo_output: dict):
    return requests.delete("http://" + str(json_destruct_node(target_node)) + "/utxo/" + address + "/outputs/", json=json_utxo_output).json()
