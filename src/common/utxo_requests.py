
from common.settings import Node_Settings
from common.requests import local_get_request, local_post_request, local_delete_request, general_get_request, general_post_request, general_delete_request

# local requests


def local_retrieve_utxo_address(settings: Node_Settings, address: str):
    url_path = "/utxo/" + address + "/"
    return local_get_request(settings, url_path, {})


def local_retrieve_utxo_outputs_of_address(settings: Node_Settings, address: str):
    url_path = "/utxo/" + address + "/outputs/"
    return local_get_request(settings, url_path, {})


def local_retrieve_utxo_output_from_address_and_transaction_hash(settings: Node_Settings, address: str, transaction_hash: str):
    url_path = "/utxo/" + address + "/outputs/" + transaction_hash + "/"
    return local_get_request(settings, url_path, {})


def local_create_utxo(settings: Node_Settings, address: str, opt_json_utxo: dict = {}):
    url_path = "/utxo/" + address + "/"
    return local_post_request(settings, url_path, opt_json_utxo)


def local_add_utxo_output(settings: Node_Settings, address: str, json_utxo_output: dict):
    url_path = "/utxo/" + address + "/outputs/"
    return local_post_request(settings, url_path, json_utxo_output)


def local_remove_utxo_output(settings: Node_Settings, address: str, json_utxo_output: dict):
    url_path = "/utxo/" + address + "/outputs/"
    return local_delete_request(settings, url_path, json_utxo_output)

# general requests


def general_retrieve_utxo_address(settings: Node_Settings, target_node: dict, address: str):
    url_path = "/utxo/" + address + "/"
    return general_get_request(settings, target_node, url_path, {})


def general_retrieve_utxo_outputs_of_address(settings: Node_Settings, target_node: dict, address: str):
    url_path = "/utxo/" + address + "/outputs/"
    return general_get_request(settings, target_node, url_path, {})


def general_retrieve_utxo_output_from_address_and_transaction_hash(settings: Node_Settings, target_node: dict, address: str, transaction_hash: str):
    url_path = "/utxo/" + address + "/outputs/" + transaction_hash + "/"
    return general_get_request(settings, target_node, url_path, {})


def general_create_utxo(settings: Node_Settings, target_node: dict, address: str, opt_json_utxo: dict = {}):
    url_path = "/utxo/" + address + "/"
    return general_post_request(settings, target_node, url_path, opt_json_utxo)


def general_add_utxo_output(settings: Node_Settings, target_node: dict, address: str, json_utxo_output: dict):
    url_path = "/utxo/" + address + "/outputs/"
    return general_post_request(settings, target_node, url_path, json_utxo_output)


def general_remove_utxo_output(settings: Node_Settings, target_node: dict, address: str, json_utxo_output: dict):
    url_path = "/utxo/" + address + "/outputs/"
    return general_delete_request(settings, target_node, url_path, json_utxo_output)
