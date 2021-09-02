from argparse import ArgumentParser
from flask import Flask
import os
import _thread
import time
import json

from full_node.settings import Full_Node_Settings

from common.node import json_destruct_node
from common.node_endpoints import node_endpoints
from common.node_requests import general_connection_check, general_retrieve_nodes, local_add_node, local_remove_node, local_retrieve_nodes
from common.blockchain import Blockchain, json_construct_blockchain_info
from common.blockchain_endpoints import blockchain_endpoints
from common.transaction_endpoints import transaction_endpoints
from common.block_endpoints import block_endpoints
from common.wallet import Wallet, json_construct_wallet
from common.utxo_endpoints import utxo_endpoints


def setup_files():
    '''
        Create the full_node directory and remainder files and sub-folders (if they don't exist already).
    '''
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

    # blockchain info file
    if not os.path.isfile(settings.blockchain_path):
        blockchain_file = open(settings.blockchain_path, "w")
        json.dump(obj=json_construct_blockchain_info(
            Blockchain()), fp=blockchain_file)
        blockchain_file.close()
        print("File \"" + settings.blockchain_path + "\" created")
    else:
        print("File \"" + settings.blockchain_path + "\" already exists!")

    # blocks folder
    if not os.path.isdir(settings.blocks_path):
        os.mkdir(settings.blocks_path)
        print("Folder \"" + settings.blocks_path + "\" created")
    else:
        print("Folder \"" + settings.blocks_path + "\" already exists!")

    # transactions file
    if not os.path.isfile(settings.transactions_path):
        transactions_file = open(settings.transactions_path, "w")
        transactions_file.write("[]")
        transactions_file.close()
        print("File \"" + settings.transactions_path + "\" created")
    else:
        print("File \"" + settings.transactions_path + "\" already exists!")

    # wallet file
    if not os.path.isfile(settings.wallet_path):
        wallet_file = open(settings.wallet_path, "w")
        json.dump(obj=json_construct_wallet(Wallet()), fp=wallet_file)
        wallet_file.close()
        print("File \"" + settings.wallet_path + "\" created")
    else:
        print("File \"" + settings.wallet_path + "\" already exists!")

    # utxo folder
    if not os.path.isdir(settings.utxo_path):
        os.mkdir(settings.utxo_path)
        print("Folder \"" + settings.utxo_path + "\" created")
    else:
        print("Folder \"" + settings.utxo_path + "\" already exists!")


def check_known_nodes():
    '''
        Check if known nodes are reachable using a connection check request,
        remove off-line nodes accordingly and check if the number of known nodes
        exceeds the required limit.
    '''
    json_nodes = local_retrieve_nodes(settings)

    for json_node in json_nodes:
        try:
            general_connection_check(json_node, settings.json_node)
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
    '''
        Retrieve the known nodes's connections and add them to the known nodes.
        Afterwards, check if the number of known nodes exceeds the required limit.
    '''
    json_nodes = local_retrieve_nodes(settings)

    for json_node in json_nodes:
        try:
            known_nodes = general_retrieve_nodes(json_node, settings.json_node)

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
    '''
        As a last resort, and also as an initial connection mechanism,
        contact the DNS Server in order to retrieve its known nodes.
    '''
    try:
        json_nodes = general_retrieve_nodes(
            settings.main_dns_server_json_node, settings.json_node)

        for json_node in json_nodes:
            local_add_node(settings, json_node)

    except:
        print("DNS Server is unreachable!")


def update_nodes():
    '''
        Periodically, check if the known nodes are reachable by removing off-line ones.
        If the number of known nodes is not exceeding the required limit, then retrieve
        the known nodes's connections and add them to the known nodes.
        Lastly, as a last resort if the number of known nodes is still not sufficient,
        contact the DNS server in order to retrieve all of its known nodes.
    '''
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
                    help="directory (default : ../.full_node)")
parser.add_argument("-n", "--nodes", default=None, type=str,
                    help="nodes filename (default : nodes.json)")
parser.add_argument("-b", "--blockchain", default=None, type=str,
                    help="blockchain filename (default : blockchain.json)")
parser.add_argument("-bf", "--blocks", default=None, type=str,
                    help="blocks foldername (default : blocks)")
parser.add_argument("-bt", "--block_temp", default=None, type=str,
                    help="block filename template (default : block)")
parser.add_argument("-t", "--transactions", default=None, type=str,
                    help="transactions filename (default : transactions.json)")
parser.add_argument("-w", "--wallet", default=None, type=str,
                    help="wallet filename (default : wallet.json)")
parser.add_argument("-ut", "--utxo", default=None, type=str,
                    help="utxo foldername (default : utxo)")
parser.add_argument("-utf", "--utxo_file", default=None, type=str,
                    help="utxo filename template (default : utxo_)")
parser.add_argument("-u", "--upd_int", default=None,
                    type=int, help="update interval (default : 60)")
parser.add_argument("-k", "--kn_limit", default=None, type=int,
                    help="known nodes limit (default : 10)")
parser.add_argument("-di", "--dns_ip", default=None, type=str,
                    help="main dns ip address (default : 127.0.0.1)")
parser.add_argument("-dp", "--dns_port", default=None, type=int,
                    help="main dns ip port (default : 42020)")
args = vars(parser.parse_args())

settings = Full_Node_Settings(
    ip_address=args["ip"], port=args["port"], directory=args["dir"],
    nodes_filename=args["nodes"], blockchain_filename=args["blockchain"],
    blocks_foldername=args["blocks"], block_file_template=args["block_temp"],
    transactions_filename=args["transactions"], wallet_filename=args["wallet"],
    utxo_foldername=args["utxo"], utxo_file_template=args["utxo_file"],
    update_interval=args["upd_int"], known_nodes_limit=args["kn_limit"],
    main_dns_server_ip_address=args["dns_ip"], main_dns_server_port=args["dns_port"]
)

# setup directory and files
setup_files()

# flask app
app = Flask(__name__)

# add endpoints
node_endpoints(app, settings)
blockchain_endpoints(app, settings)
transaction_endpoints(app, settings)
block_endpoints(app, settings)
utxo_endpoints(app, settings)

# start thread for regularly updating nodes
_thread.start_new_thread(update_nodes, ())

# start flask app
if __name__ == "__main__":
    app.run(host=settings.ip_address, port=settings.port)
