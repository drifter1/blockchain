from argparse import ArgumentParser
from flask import Flask
import os
import _thread
import time
import json

from full_node.settings import Full_Node_Settings

from full_node.block_endpoints import block_endpoints
from full_node.blockchain_endpoints import blockchain_endpoints
from full_node.transaction_endpoints import transaction_endpoints
from full_node.utxo_endpoints import utxo_endpoints

from common.block_header import json_block_header_and_transactions_to_block
from common.blockchain import Blockchain, AddressBalancePair, json_construct_blockchain_info, json_destruct_blockchain_info
from common.wallet import Wallet, json_construct_wallet
from common.utxo import UTXO_Output, json_construct_utxo_output

from common.node_endpoints import node_endpoints
from common.node_update import update_nodes
from common.node_requests import local_retrieve_node

from common.blockchain_requests import general_retrieve_blockchain_info, local_retrieve_blockchain_info, local_update_blockchain_info
from common.block_requests import general_retrieve_block_header, general_retrieve_block_transactions_header, general_retrieve_block_transaction
from common.utxo_requests import local_add_utxo_output, local_remove_utxo_output, local_retrieve_utxo_output_from_address_and_transaction_hash, local_retrieve_utxo_address
from common.transaction_requests import general_retrieve_transactions_header, general_retrieve_transaction


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
        Contact random known node to check if local files are up-to-date.
        If not then retrieve all the missing blocks and
        replace all local unconfirmed transactions.
    '''
    time.sleep(2)

    # random known node
    json_node, status_code = local_retrieve_node(settings, "random")

    if status_code != 200:
        return

    # retrieve local blockchain info
    json_local_blockchain_info, status_code = local_retrieve_blockchain_info(
        settings)

    if status_code != 200:
        print("Error in local blockchain info retrieval!")
        exit()

    local_blockchain_info = json_destruct_blockchain_info(
        json_local_blockchain_info)

    # retrieve blockchain info from first known node
    try:
        json_blockchain_info, status_code = general_retrieve_blockchain_info(
            settings, json_node)

        if status_code != 200:
            return
    except:
        return
    
    blockchain_info = json_destruct_blockchain_info(json_blockchain_info)

    # check if blockchain is up to date
    if local_blockchain_info.height != blockchain_info.height:
        for height in range(local_blockchain_info.height + 1,  blockchain_info.height + 1):

            # retrieve block header
            json_block_header, status_code = general_retrieve_block_header(
                settings, json_node, height)

            transaction_count = json_block_header["transaction_count"]

            # retrieve transactions one-by-one
            json_block_transactions = []
            for tid in range(0, transaction_count):
                json_transaction, status_code = general_retrieve_block_transaction(
                    settings, json_node, height, tid)

                json_block_transactions.append(json_transaction)

            # construct block
            json_block = json_block_header_and_transactions_to_block(
                json_block_header, json_block_transactions)

            # create block file
            json.dump(obj=json_block, fp=open(
                settings.block_file_path + str(json_block["height"]) + ".json", "w"))

            # update utxo's
            transaction_index = 0
            for json_transaction in json_block["transactions"]:

                # coinbase transaction
                if transaction_index == 0:
                    utxo_reward_output = UTXO_Output(
                        block_height=json_block["height"],
                        transaction_hash=json_transaction["hash"],
                        transaction_index=0,
                        output_index=0
                    )

                    json_utxo_reward_output = json_construct_utxo_output(
                        utxo_reward_output)

                    local_add_utxo_output(
                        settings, json_transaction["outputs"][0]["address"], json_utxo_reward_output)

                    transaction_index += 1
                    continue

                # remove spent outputs

                for json_input in json_transaction["inputs"]:
                    json_utxo_output, status_code = local_retrieve_utxo_output_from_address_and_transaction_hash(
                        settings, json_input["output_address"], json_input["transaction_hash"])

                    local_remove_utxo_output(
                        settings, json_input["output_address"], json_utxo_output)

                # add spendable outputs

                for json_output in json_transaction["outputs"]:
                    utxo_output = UTXO_Output(
                        block_height=json_block["height"],
                        transaction_hash=json_transaction["hash"],
                        transaction_index=transaction_index,
                        output_index=json_output["index"]
                    )

                    json_utxo_output = json_construct_utxo_output(utxo_output)

                    local_add_utxo_output(
                        settings, json_output["address"], json_utxo_output)

                transaction_index += 1

            # update blockchain info
            json_blockchain_info, status_code = local_retrieve_blockchain_info(
                settings)
            blockchain_info = json_destruct_blockchain_info(
                json_blockchain_info)

            blockchain_info.height = json_block["height"]
            blockchain_info.total_addresses = len(
                os.listdir(settings.utxo_path))
            blockchain_info.total_transactions += len(
                json_block["transactions"])

            # rich list calculation (currently inefficient)
            blockchain_info.rich_list = []
            for utxo_file in os.listdir(settings.utxo_path):
                address = utxo_file[5:47]
                utxo_address, status_code = local_retrieve_utxo_address(
                    settings, address)
                balance = utxo_address["balance"]
                address_balance_pair = AddressBalancePair(address, balance)
                blockchain_info.rich_list.append(address_balance_pair)
            blockchain_info.rich_list.sort(reverse=True)
            while len(blockchain_info.rich_list) > 10:
                blockchain_info.rich_list.pop()

            json_blockchain_info = json_construct_blockchain_info(
                blockchain_info)
            local_update_blockchain_info(settings, json_blockchain_info)

        # retrieve unconfirmed transactions header
        json_transactions_header, status_code = general_retrieve_transactions_header(
            settings, json_node)

        transaction_count = json_transactions_header["transaction_count"]

        # retrieve unconfirmed transactions one-by-one
        json_transactions = []
        for tid in range(0, transaction_count):
            json_transaction, status_code = general_retrieve_transaction(
                settings, json_node, tid)

            json_transactions.append(json_transaction)

        # update local file
        json.dump(obj=json_transactions, fp=open(
            settings.transactions_path, "w"))


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
