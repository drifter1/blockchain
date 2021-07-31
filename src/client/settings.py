import json
import random

from common.node import json_construct_node
from common.settings import Node_Settings

class Client_Settings(Node_Settings):
    def __init__(self, ip_address=None, port=None, directory=None, nodes_filename=None, blockchain_filename=None, transactions_filename=None, wallets_filename=None, update_interval=None, known_nodes_limit=None, main_dns_server_ip_address=None, main_dns_server_port=None):

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
        self.transactions_path = self.directory + "/" + transactions_filename if (
            transactions_filename != None) else self.directory + "/" + client_defaults["default_transactions_filename"]
        self.wallets_path = self.directory + "/" + wallets_filename if(
            wallets_filename != None) else self.directory + "/" + client_defaults["default_wallets_filename"]
        self.update_interval = update_interval if (
            update_interval != None) else client_defaults["default_update_interval"]
        self.known_nodes_limit = known_nodes_limit if(
            known_nodes_limit != None) else client_defaults["default_known_nodes_limit"]
        self.known_nodes = 0
        self.main_dns_server_ip_address = main_dns_server_ip_address if(
            main_dns_server_ip_address != None) else client_defaults["main_dns_server_ip_address"]
        self.main_dns_server_port = main_dns_server_port if (
            main_dns_server_port != None) else client_defaults["main_dns_server_port"]
