from flask import Flask
import os
import _thread
import time
import json
from argparse import ArgumentParser

from client.settings import Client_Settings
from common.node import json_destruct_node
from common.node_endpoints import node_endpoints
from common.node_requests import general_connection_check, general_retrieve_nodes, local_add_node, local_remove_node, local_retrieve_nodes
from common.blockchain import Blockchain, json_construct_blockchain_info
from common.blockchain_endpoints import blockchain_endpoints
from common.transaction import Input, Output, Transaction, calculate_output_hash, calculate_transaction_hash, json_construct_transaction, sign_input
from common.transaction_endpoints import transaction_endpoints
from common.transaction_requests import local_post_transaction
from common.block import Block, calculate_block_hash, json_construct_block
from common.block_endpoints import block_endpoints
from common.block_requests import local_create_block
from common.wallet import Wallet, json_construct_wallet, json_retrieve_private_key, json_retrieve_address
from common.utxo import UTXO_Output, json_construct_utxo_output
from common.utxo_endpoints import utxo_endpoints
from common.utxo_requests import local_add_utxo_output, local_create_utxo, local_remove_utxo_output

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

# Update Nodes Routines


def check_known_nodes():
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
    try:
        json_nodes = general_retrieve_nodes(
            settings.main_dns_server_json_node, settings.json_node)

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

# '''


def testing():
    time.sleep(2)

    wallet_json = json.load(open(settings.wallet_path, "r"))

    address = json_retrieve_address(wallet_json)
    private_key = json_retrieve_private_key(wallet_json)

    # create reward transaction

    reward_input = Input(
        output_value=2.5
    )

    reward_output = Output(
        address=address,
        value=2.5
    )
    calculate_output_hash(reward_output)

    reward_transaction = Transaction(
        inputs=[reward_input],
        outputs=[reward_output],
        total_input=2.5,
        total_output=2.5,
        fee=0
    )
    calculate_transaction_hash(reward_transaction)

    # create block 0

    block0 = Block(height=0, creator=address, reward=2.5, fees=0,
                   nonce="abcdef", transactions=[reward_transaction])

    calculate_block_hash(block0)

    json_block0 = json_construct_block(block0)

    local_create_block(settings, json_block0)

    # create utxo for wallet address

    local_create_utxo(settings, address)

    # update utxo for wallet address based on block 0

    utxo_reward_output = UTXO_Output(
        block_height=block0.height,
        transaction_hash=reward_transaction.hash,
        transaction_index=0,
        output_index=0
    )

    json_utxo_reward_output = json_construct_utxo_output(utxo_reward_output)

    local_add_utxo_output(settings, address, json_utxo_reward_output)

    time.sleep(15)

    # create reward transaction 2

    reward_input2 = Input(
        output_value=2.5
    )

    reward_output2 = Output(
        address=address,
        value=2.5
    )
    calculate_output_hash(reward_output2)

    reward_transaction2 = Transaction(
        inputs=[reward_input2],
        outputs=[reward_output2],
        total_input=2.5,
        total_output=2.5,
        fee=0
    )
    calculate_transaction_hash(reward_transaction2)

    # create test transaction

    input0 = Input(
        transaction_hash=reward_transaction.hash,
        output_index=0,
        output_address=address,
        output_value=reward_output.value,
        output_hash=reward_output.hash,
    )
    sign_input(input0, private_key)

    output0 = Output(
        index=0,
        address="0x60a192daca0804e113d6e6d41852c611be5de0bf",
        value=1.2
    )
    calculate_output_hash(output0)

    output1 = Output(
        index=1,
        address="0xe23fc383c7007002ef08be610cef95a86ce44e26",
        value=0.3
    )
    calculate_output_hash(output1)

    output2 = Output(
        index=2,
        address=address,
        value=0.999
    )
    calculate_output_hash(output2)

    transaction = Transaction(
        inputs=[input0],
        outputs=[output0, output1, output2],
        total_input=2.5,
        total_output=2.499,
        fee=0.001
    )
    calculate_transaction_hash(transaction)

    json_transaction = json_construct_transaction(transaction)

    local_post_transaction(settings, json_transaction)

    # create block 1

    block1 = Block(height=1, creator=address, reward=2.5, fees=0.001,
                   nonce="123456", transactions=[reward_transaction2, transaction])

    calculate_block_hash(block1)

    json_block1 = json_construct_block(block1)

    local_create_block(settings, json_block1)

    # update utxo for wallet address based on block 1

    local_remove_utxo_output(settings, address, json_utxo_reward_output)

    utxo_output0 = UTXO_Output(
        block_height=block1.height,
        transaction_hash=reward_transaction2.hash,
        transaction_index=0,
        output_index=0
    )

    json_utxo_output0 = json_construct_utxo_output(utxo_output0)

    local_add_utxo_output(settings, address, json_utxo_output0)

    utxo_output1 = UTXO_Output(
        block_height=block1.height,
        transaction_hash=transaction.hash,
        transaction_index=1,
        output_index=2
    )

    json_utxo_output1 = json_construct_utxo_output(utxo_output1)

    local_add_utxo_output(settings, address, json_utxo_output1)


# '''

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

settings = Client_Settings(
    ip_address=args["ip"], port=args["port"], directory=args["dir"],
    nodes_filename=args["nodes"], blockchain_filename=args["blockchain"],
    blocks_foldername=args["blocks"], block_file_template=args["block_temp"],
    transactions_filename=args["transactions"], wallet_filename=args["wallet"],
    utxo_foldername=args["utxo"], utxo_file_template=args["utxo_file"],
    update_interval=args["upd_int"], known_nodes_limit=args["kn_limit"],
    main_dns_server_ip_address=args["dns_ip"], main_dns_server_port=args["dns_port"]
)

# main function

app = Flask(__name__)

node_endpoints(app, settings)
blockchain_endpoints(app, settings)
transaction_endpoints(app, settings)
block_endpoints(app, settings)
utxo_endpoints(app, settings)

setup_files()

_thread.start_new_thread(update_nodes, ())

# testing
_thread.start_new_thread(testing, ())

if __name__ == "__main__":
    app.run(host=settings.ip_address, port=settings.port)
