import json
import random

from common.node import json_construct_node
from common.settings import Node_Settings


class Client_Settings(Node_Settings):
    def __init__(self, ip_address=None, port=None, directory=None, nodes_filename=None, blockchain_filename=None, blocks_foldername=None, block_file_template=None, transactions_filename=None, wallet_filename=None, utxo_foldername=None, utxo_file_template=None, update_interval=None, known_nodes_limit=None, main_dns_server_ip_address=None, main_dns_server_port=None):

        # load defaults
        f = open("../defaults/client_defaults.json")
        client_defaults = json.load(f)
        f.close()

        self.ip_address = ip_address if (
            ip_address != None) else client_defaults["default_ip_address"]
        self.port = port if (port != None) else random.randrange(
            client_defaults["port_min"], client_defaults["port_max"])
        self.json_node = json_construct_node(self.ip_address, self.port)
        self.directory = directory if (
            directory != None) else client_defaults["default_directory"]
        self.nodes_path = self.directory + "/" + nodes_filename if (
            nodes_filename != None) else self.directory + "/" + client_defaults["default_nodes_filename"]
        self.blockchain_path = self.directory + "/" + blockchain_filename if (
            blockchain_filename != None) else self.directory + "/" + client_defaults["default_blockchain_filename"]
        self.blocks_path = self.directory + "/" + blocks_foldername if (
            blocks_foldername != None) else self.directory + "/" + client_defaults["default_blocks_foldername"]
        self.block_file_path = self.blocks_path + "/" + block_file_template if (
            block_file_template != None) else self.blocks_path + "/" + client_defaults["default_block_file_template"]
        self.transactions_path = self.directory + "/" + transactions_filename if (
            transactions_filename != None) else self.directory + "/" + client_defaults["default_transactions_filename"]
        self.wallet_path = self.directory + "/" + wallet_filename if(
            wallet_filename != None) else self.directory + "/" + client_defaults["default_wallet_filename"]
        self.utxo_path = self.directory + "/" + utxo_foldername if (
            utxo_foldername != None) else self.directory + "/" + client_defaults["default_utxo_foldername"]
        self.utxo_file_path = self.utxo_path + "/" + utxo_file_template if(
            utxo_file_template != None) else self.utxo_path + "/" + client_defaults["default_utxo_file_template"]
        self.update_interval = update_interval if (
            update_interval != None) else client_defaults["default_update_interval"]
        self.known_nodes_limit = known_nodes_limit if(
            known_nodes_limit != None) else client_defaults["default_known_nodes_limit"]
        self.known_nodes = 0
        self.main_dns_server_ip_address = main_dns_server_ip_address if(
            main_dns_server_ip_address != None) else client_defaults["main_dns_server_ip_address"]
        self.main_dns_server_port = main_dns_server_port if (
            main_dns_server_port != None) else client_defaults["main_dns_server_port"]
        self.main_dns_server_json_node = json_construct_node(
            self.main_dns_server_ip_address, self.main_dns_server_port)
