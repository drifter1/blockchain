import json
import random

from common.node import json_construct_node
from common.settings import Node_Settings


class Full_Node_Settings(Node_Settings):
    def __init__(self, ip_address: str = None, port: int = None, directory: str = None, nodes_filename: str = None, blockchain_filename: str = None, blocks_foldername: str = None, block_file_template: str = None, transactions_filename: str = None, wallet_filename: str = None, utxo_foldername: str = None, utxo_file_template: str = None, update_interval: int = None, sync_interval: int = None, request_timeout: float = None, known_nodes_limit: int = None, main_dns_server_ip_address: str = None, main_dns_server_port: int = None):

        # load defaults
        f = open("../defaults/full_node_defaults.json")
        full_node_defaults = json.load(f)
        f.close()

        self.ip_address = ip_address if (
            ip_address != None) else full_node_defaults["default_ip_address"]
        self.port = port if (port != None) else random.randrange(
            full_node_defaults["port_min"], full_node_defaults["port_max"])
        self.json_node = json_construct_node(self.ip_address, self.port)
        self.directory = directory if (
            directory != None) else full_node_defaults["default_directory"]
        self.nodes_path = self.directory + "/" + nodes_filename if (
            nodes_filename != None) else self.directory + "/" + full_node_defaults["default_nodes_filename"]
        self.blockchain_path = self.directory + "/" + blockchain_filename if (
            blockchain_filename != None) else self.directory + "/" + full_node_defaults["default_blockchain_filename"]
        self.blocks_path = self.directory + "/" + blocks_foldername if (
            blocks_foldername != None) else self.directory + "/" + full_node_defaults["default_blocks_foldername"]
        self.block_file_path = self.blocks_path + "/" + block_file_template if (
            block_file_template != None) else self.blocks_path + "/" + full_node_defaults["default_block_file_template"]
        self.transactions_path = self.directory + "/" + transactions_filename if (
            transactions_filename != None) else self.directory + "/" + full_node_defaults["default_transactions_filename"]
        self.wallet_path = self.directory + "/" + wallet_filename if(
            wallet_filename != None) else self.directory + "/" + full_node_defaults["default_wallet_filename"]
        self.utxo_path = self.directory + "/" + utxo_foldername if (
            utxo_foldername != None) else self.directory + "/" + full_node_defaults["default_utxo_foldername"]
        self.utxo_file_path = self.utxo_path + "/" + utxo_file_template if(
            utxo_file_template != None) else self.utxo_path + "/" + full_node_defaults["default_utxo_file_template"]
        self.update_interval = update_interval if (
            update_interval != None) else full_node_defaults["default_update_interval"]
        self.sync_interval = sync_interval if (
            sync_interval != None) else full_node_defaults["default_sync_interval"]
        self.request_timeout = request_timeout if (
            request_timeout != None) else full_node_defaults["default_request_timeout"]
        self.known_nodes_limit = known_nodes_limit if(
            known_nodes_limit != None) else full_node_defaults["default_known_nodes_limit"]
        self.known_nodes = 0
        self.main_dns_server_ip_address = main_dns_server_ip_address if(
            main_dns_server_ip_address != None) else full_node_defaults["main_dns_server_ip_address"]
        self.main_dns_server_port = main_dns_server_port if (
            main_dns_server_port != None) else full_node_defaults["main_dns_server_port"]
        self.main_dns_server_json_node = json_construct_node(
            self.main_dns_server_ip_address, self.main_dns_server_port)
