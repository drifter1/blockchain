import os
import time
import json
from argparse import ArgumentParser

from full_node.settings import Full_Node_Settings
from common.node_requests import general_retrieve_nodes
from common.block import Block, calculate_block_hash, json_construct_block
from common.block_requests import general_create_block
from common.transaction import Input, Output, Transaction, calculate_output_hash, calculate_transaction_hash, json_construct_transaction, sign_input
from common.transaction_requests import general_post_transaction
from common.utxo_requests import general_retrieve_utxo_address
from common.wallet import Wallet, json_construct_wallet, json_retrieve_address, json_retrieve_private_key

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

    # wallet file
    if not os.path.isfile(settings.wallet_path):
        wallet_file = open(settings.wallet_path, "w")
        json.dump(obj=json_construct_wallet(Wallet()), fp=wallet_file)
        wallet_file.close()
        print("File \"" + settings.wallet_path + "\" created")
    else:
        print("File \"" + settings.wallet_path + "\" already exists!")


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
parser.add_argument("-w", "--wallet", default=None, type=str,
                    help="wallet filename (default : wallet.json)")
parser.add_argument("-u", "--upd_int", default=None,
                    type=int, help="update interval (default : 60)")
parser.add_argument("-k", "--kn_limit", default=None, type=int,
                    help="known nodes limit (default : 10)")
parser.add_argument("-di", "--dns_ip", default=None, type=str,
                    help="main dns ip address (default : 127.0.0.1)")
parser.add_argument("-dp", "--dns_port", default=None, type=int,
                    help="main dns ip port (default : 42020)")
args = vars(parser.parse_args())

args["dir"] = "../.testing"

settings = Full_Node_Settings(
    ip_address=args["ip"], port=args["port"], directory=args["dir"],
    nodes_filename=args["nodes"], wallet_filename=args["wallet"],
    update_interval=args["upd_int"], known_nodes_limit=args["kn_limit"],
    main_dns_server_ip_address=args["dns_ip"], main_dns_server_port=args["dns_port"]
)

setup_files()

# retrieve first known node from dns server
json_nodes, status_code = general_retrieve_nodes(
    settings, settings.main_dns_server_json_node)
json_node = json_nodes[0]

# load wallet information

wallet_json = json.load(open(settings.wallet_path, "r"))

address = json_retrieve_address(wallet_json)
private_key = json_retrieve_private_key(wallet_json)

print(address)

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

general_create_block(settings, json_node, json_block0)

# retrieve utxo for the wallet address

json_utxo, status_code = general_retrieve_utxo_address(
    settings, json_node, address)

print(json_utxo)

time.sleep(10)

# create and post test transaction

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

general_post_transaction(settings, json_node, json_transaction)

time.sleep(10)

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

# create block 1

block1 = Block(height=1, creator=address, reward=2.5, fees=0.001,
               nonce="123456", transactions=[reward_transaction2, transaction])

calculate_block_hash(block1)

json_block1 = json_construct_block(block1)

general_create_block(settings, json_node, json_block1)

# retrieve utxo for the wallet address

json_utxo, status_code = general_retrieve_utxo_address(
    settings, json_node, address)

print(json_utxo)
