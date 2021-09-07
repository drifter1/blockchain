from argparse import ArgumentParser
from flask import Flask
from flask_api import status
import os
import _thread
import time
import json

from full_node.settings import Full_Node_Settings

from full_node.block_endpoints import block_endpoints
from full_node.blockchain_endpoints import blockchain_endpoints
from full_node.transaction_endpoints import transaction_endpoints
from full_node.utxo_endpoints import utxo_endpoints

from common.blockchain import Blockchain, json_construct_blockchain_info, json_destruct_blockchain_info
from common.wallet import Wallet, json_construct_wallet

from common.node_endpoints import node_endpoints
from common.node_update import update_nodes
from common.node_requests import local_retrieve_nodes

from common.blockchain_requests import general_retrieve_blockchain_info, local_retrieve_blockchain_info
from common.block_requests import general_retrieve_block, local_create_block
from common.transaction_requests import general_retrieve_transactions, local_post_transaction


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


def network_sync():
    '''
        Contact first known node to check if local files are up-to-date.
        If not then retrieve all the missing blocks and
        replace all local unconfirmed transactions.
    '''
    time.sleep(2)

    json_nodes, status_code = local_retrieve_nodes(settings)

    if status_code != status.HTTP_200_OK:
        print("Error in local nodes retrieval!")
        exit()

    # retrieve local blockchain info
    json_local_blockchain_info, status_code = local_retrieve_blockchain_info(
        settings)

    if status_code != status.HTTP_200_OK:
        print("Error in local blockchain info retrieval!")
        exit()

    local_blockchain_info = json_destruct_blockchain_info(
        json_local_blockchain_info)

    # retrieve blockchain info from first known node
    try:
        json_node = json_nodes[0]

        json_blockchain_info, status_code = general_retrieve_blockchain_info(
            settings, json_node)

        if status_code != status.HTTP_200_OK:
            return
    except:
        return

    blockchain_info = json_destruct_blockchain_info(json_blockchain_info)

    # check if blockchain is up to date
    if local_blockchain_info.height != blockchain_info.height:
        for height in (local_blockchain_info.height + 1,  blockchain_info.height + 1):

            # retrieve block
            json_block, status_code = general_retrieve_block(
                settings, json_node, height)

            # post block
            local_create_block(settings, json_block)

            # retrieve transactions
            transactions_file = open(settings.transactions_path, "w")
            transactions_file.write("[]")
            transactions_file.close()
            json_transactions, status_code = general_retrieve_transactions(
                settings, json_node)

            for json_transaction in json_transactions:
                local_post_transaction(settings, json_transaction)


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
_thread.start_new_thread(update_nodes, (settings, settings.json_node))

# start thread for network synchronization
_thread.start_new_thread(network_sync, ())

# start flask app
if __name__ == "__main__":
    app.run(host=settings.ip_address, port=settings.port)
