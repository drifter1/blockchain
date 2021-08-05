from flask import Flask
import os
import _thread
import time
from argparse import ArgumentParser

from dns_server.settings import DNS_Server_Settings
from common.node import json_destruct_node
from common.node_endpoints import general_connection_check, local_remove_node, local_retrieve_nodes, node_endpoints

# Setup Files Routine


def setup_files():
    # directory management
    if not os.path.exists(settings.directory):
        os.mkdir(settings.directory)
        print("Directory \"" + settings.directory + "\" created")
    else:
        print("Directory \"" + settings.directory + "\" already exists!")

    # nodes file
    if not os.path.isfile(settings.nodes_path):
        nodes_file = open(settings.nodes_path, "w")
        nodes_file.write("[]")
        nodes_file.close()
        print("File \"" + settings.nodes_path + "\" created")
    else:
        print("File \"" + settings.nodes_path + "\" already exists!")

# Update Nodes Routine

def update_nodes():
    time.sleep(1)

    while True:
        # check if nodes are reachable
        print("Updating nodes started!")

        json_nodes = local_retrieve_nodes(settings)

        for json_node in json_nodes:
            try:
                general_connection_check(settings, json_node)
            except:
                print("Node " + str(json_destruct_node(json_node)) + " is unreachable!")

                local_remove_node(settings, json_node)

        print("Updating nodes finished!")

        # wait for a specific interval of time
        time.sleep(settings.update_interval)

# dns server arguments


parser = ArgumentParser()
parser.add_argument("-i", "--ip", default=None, type=str,
                    help="ip address (default : 127.0.0.1)")
parser.add_argument("-p", "--port", default=None, type=int,
                    help="port (default : 42020)")
parser.add_argument("-d", "--dir", default=None, type=str,
                    help="directory (default : ../.dns_server)")
parser.add_argument("-n", "--nodes", default=None, type=str,
                    help="nodes filename (default : nodes.json)")
parser.add_argument("-u", "--upd_int", default=None,
                    type=int, help="update interval (default : 60)")
args = vars(parser.parse_args())

settings = DNS_Server_Settings(
    ip_address=args["ip"], port=args["port"], directory=args["dir"],
    nodes_filename=args["nodes"], update_interval=args["upd_int"]
)

# main function

app = Flask(__name__)

node_endpoints(app, settings)

setup_files()

_thread.start_new_thread(update_nodes, ())

if __name__ == "__main__":
    app.run(host=settings.ip_address, port=settings.port)
