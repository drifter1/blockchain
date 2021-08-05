from flask import Flask
import os
import _thread
import time
from argparse import ArgumentParser

from client.settings import Client_Settings
from common.node import json_destruct_node
from common.node_endpoints import general_connection_check, general_retrieve_nodes, local_add_node, local_remove_node, local_retrieve_nodes, node_endpoints

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

    # blockchain file
    if not os.path.isfile(settings.blockchain_path):
        blockchain_file = open(settings.blockchain_path, "w")
        blockchain_file.write("[]")
        blockchain_file.close()
        print("File \"" + settings.blockchain_path + "\" created")
    else:
        print("File \"" + settings.blockchain_path + "\" already exists!")

    # transactions file
    if not os.path.isfile(settings.transactions_path):
        transactions_file = open(settings.transactions_path, "w")
        transactions_file.write("[]")
        transactions_file.close()
        print("File \"" + settings.transactions_path + "\" created")
    else:
        print("File \"" + settings.transactions_path + "\" already exists!")

    # wallets file
    if not os.path.isfile(settings.wallets_path):
        wallets_file = open(settings.wallets_path, "w")
        wallets_file.write("[]")
        wallets_file.close()
        print("File \"" + settings.wallets_path + "\" created")
    else:
        print("File \"" + settings.wallets_path + "\" already exists!")

# Update Nodes Routines


def check_known_nodes():
    json_nodes = local_retrieve_nodes(settings)

    for json_node in json_nodes:
        try:
            general_connection_check(settings, json_node)
        except:
            print("Node " + str(json_destruct_node(json_node)) + " is unreachable!")

            local_remove_node(settings, json_node)

    json_nodes = local_retrieve_nodes(settings)

    settings.known_nodes = len(json_nodes)

    if settings.known_nodes >= settings.known_nodes_limit:
        return True
    else:
        return False


def retrieve_known_nodes_connections():
    json_nodes = local_retrieve_nodes(settings)

    for json_node in json_nodes:
        try:
            known_nodes = general_retrieve_nodes(settings, json_node)

            for known_node in known_nodes:
                local_add_node(settings, known_node)

        except:
            pass

    json_nodes = local_retrieve_nodes(settings)

    settings.known_nodes = len(json_nodes)

    if settings.known_nodes >= settings.known_nodes_limit:
        return True
    else:
        return False


def contact_dns_server():
    try:
        json_nodes = general_retrieve_nodes(
            settings, settings.main_dns_server_json_node)

        for json_node in json_nodes:
            local_add_node(settings, json_node)

    except:
        print("DNS Server is unreachable!")


def update_nodes():
    time.sleep(1)

    while True:
        print("Updating nodes started!")

        # check known nodes
        print("Checking known nodes...")
        if check_known_nodes():
            print("Updating nodes finished!")
            continue

        # retrieve connections of known nodes
        print("Retrieve connections of known nodes...")
        if retrieve_known_nodes_connections():
            print("Updating nodes finished!")
            continue

        # contact dns server
        print("Contacting dns server...")
        contact_dns_server()

        print("Updating nodes finished!")

        # wait for a specific interval of time
        time.sleep(settings.update_interval)


# client arguments

parser = ArgumentParser()
parser.add_argument("-i", "--ip", default=None, type=str,
                    help="ip address (default : 127.0.0.1)")
parser.add_argument("-p", "--port", default=None, type=int,
                    help="port (default : random in [50000, 60000])")
parser.add_argument("-d", "--dir", default=None, type=str,
                    help="directory (default : ../.client)")
parser.add_argument("-n", "--nodes", default=None, type=str,
                    help="nodes filename (default : nodes.json)")
parser.add_argument("-b", "--blockchain", default=None, type=str,
                    help="blockchain filename (default : blockchain.json)")
parser.add_argument("-t", "--transactions", default=None, type=str,
                    help="transactions filename (default : transactions.json)")
parser.add_argument("-w", "--wallets", default=None, type=str,
                    help="wallets filename (default : wallets.json)")
parser.add_argument("-u", "--upd_int", default=None,
                    type=int, help="update interval (default : 60)")
parser.add_argument("-k", "--kn_limit", default=None, type=int,
                    help="known nodes limit (default : 10)")
parser.add_argument("-di", "--dns_ip", default=None, type=str,
                    help="main dns ip address (default : 127.0.0.1)")
parser.add_argument("-dp", "--dns_port", default=None, type=int,
                    help="main dns ip port (default : 42020)")
args = vars(parser.parse_args())

settings = Client_Settings(
    ip_address=args["ip"], port=args["port"], directory=args["dir"],
    nodes_filename=args["nodes"], blockchain_filename=args["blockchain"],
    transactions_filename=args["transactions"], wallets_filename=args["wallets"],
    update_interval=args["upd_int"], known_nodes_limit=args["kn_limit"],
    main_dns_server_ip_address=args["dns_ip"], main_dns_server_port=args["dns_port"]
)

# main function

app = Flask(__name__)

node_endpoints(app, settings)

setup_files()

_thread.start_new_thread(update_nodes, ())

if __name__ == "__main__":
    app.run(host=settings.ip_address, port=settings.port)
