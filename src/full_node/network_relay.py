
import _thread

from common.settings import Node_Settings
from common.node_requests import local_retrieve_nodes
from common.block_requests import general_create_block
from common.transaction_requests import general_post_transaction, general_remove_transaction


def general_network_relay(settings: Node_Settings, function: exec, json_data: dict):
    json_nodes, status_code = local_retrieve_nodes(settings)

    if status_code != 200:
        return

    for json_node in json_nodes:
        try:
            _thread.start_new_thread(
                function, (settings, json_node, json_data))
        except:
            pass


def create_block_network_relay(settings: Node_Settings, json_block: dict):
    general_network_relay(settings, general_create_block, json_block)


def post_transaction_network_relay(settings: Node_Settings, json_transaction: dict):
    general_network_relay(settings, general_post_transaction, json_transaction)


def remove_transaction_network_relay(settings: Node_Settings, json_transaction: dict):
    general_network_relay(
        settings, general_remove_transaction, json_transaction)
