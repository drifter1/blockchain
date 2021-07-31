import json

from common.node import json_construct_node
from common.settings import Node_Settings


class DNS_Server_Settings(Node_Settings):
    def __init__(self, ip_address=None, port=None, directory=None, nodes_filename=None, update_interval=None):

        # load defaults
        f = open("../defaults/dns_server_defaults.json")
        server_defaults = json.load(f)
        f.close()

        self.ip_address = ip_address if (
            ip_address != None) else server_defaults["default_ip_address"]
        self.port = port if (port != None) else server_defaults["default_port"]
        self.json_node = json_construct_node(self.ip_address, self.port)
        self.directory = directory if (
            directory != None) else server_defaults["default_directory"]
        self.nodes_path = self.directory + "/" + nodes_filename if (
            nodes_filename != None) else self.directory + "/" + server_defaults["default_nodes_filename"]
        self.update_interval = update_interval if (
            update_interval != None) else server_defaults["default_update_interval"]
