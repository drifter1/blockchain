import json
import random

from common.node import json_construct_node


class Node_Settings:
    def __init__(self, ip_address: str = None, port: int = None, directory: str = None, nodes_filename: str = None, update_interval: int = None, request_timeout: float = None, known_nodes_limit: int = None, main_dns_server_ip_address: str = None, main_dns_server_port: int = None):

        # load defaults
        f = open("../defaults/node_defaults.json")
        node_defaults = json.load(f)
        f.close()

        self.ip_address = ip_address if (
            ip_address != None) else node_defaults["default_ip_address"]
        self.port = port if (port != None) else random.randrange(
            node_defaults["port_min"], node_defaults["port_max"])
        self.json_node = json_construct_node(self.ip_address, self.port)
        self.directory = directory if (
            directory != None) else node_defaults["default_directory"]
        self.nodes_path = self.directory + "/" + nodes_filename if (
            nodes_filename != None) else self.directory + "/" + node_defaults["default_nodes_filename"]
        self.update_interval = update_interval if (
            update_interval != None) else node_defaults["default_update_interval"]
        self.request_timeout = request_timeout if (
            request_timeout != None) else node_defaults["default_request_timeout"]
        self.known_nodes_limit = known_nodes_limit if(
            known_nodes_limit != None) else node_defaults["default_known_nodes_limit"]
        self.known_nodes = 0
        self.main_dns_server_ip_address = main_dns_server_ip_address if(
            main_dns_server_ip_address != None) else node_defaults["main_dns_server_ip_address"]
        self.main_dns_server_port = main_dns_server_port if (
            main_dns_server_port != None) else node_defaults["main_dns_server_port"]
        self.main_dns_server_json_node = json_construct_node(
            self.main_dns_server_ip_address, self.main_dns_server_port)
