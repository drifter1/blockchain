import os
import time
import json
from argparse import ArgumentParser

from full_node.settings import Full_Node_Settings

from common.transaction import Input, Output, Transaction, calculate_output_hash, calculate_transaction_hash, json_construct_transaction, json_destruct_output, sign_input
from common.utxo import json_destruct_utxo_output
from common.wallet import Wallet, json_construct_wallet, json_retrieve_address, json_retrieve_private_key

from common.block_requests import general_retrieve_block_transaction_output
from common.transaction_requests import general_post_transaction
from common.node_requests import general_retrieve_node
from common.utxo_requests import general_retrieve_utxo_address

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

# load wallet information

wallet_json = json.load(open(settings.wallet_path, "r"))

address = json_retrieve_address(wallet_json)
private_key = json_retrieve_private_key(wallet_json)

print(address)

# retrieve random node from dns server
json_node, status_code = general_retrieve_node(
    settings, settings.main_dns_server_json_node, "random")

if status_code != 200:
    exit()

# retrieve utxo for the wallet address

time.sleep(1)

json_utxo, status_code = general_retrieve_utxo_address(
    settings, json_node, address)

if status_code != 200:
    exit()

print(json_utxo)

# retrieve first UTXO output
try:
    json_utxo_output = json_utxo["utxo_outputs"][0]
    utxo_output = json_destruct_utxo_output(json_utxo_output)
except:
    exit()

# retrieve corresponding transaction output in block
json_block_transaction_output, status_code = general_retrieve_block_transaction_output(
    settings, json_node, utxo_output.block_height, utxo_output.transaction_index, utxo_output.output_index)

if status_code != 200:
    exit()

print(json_block_transaction_output)

block_transaction_output = json_destruct_output(json_block_transaction_output)

# create and post test transaction

input0 = Input(
    transaction_hash=utxo_output.transaction_hash,
    output_index=0,
    output_address=address,
    output_value=block_transaction_output.value,
    output_hash=block_transaction_output.hash,
)
sign_input(input0, private_key)

output0 = Output(
    index=0,
    address="0x60a192daca0804e113d6e6d41852c611be5de0bf",
    value=0.3
)
calculate_output_hash(output0)

output1 = Output(
    index=1,
    address="0xb24e0a3dbf9095d62418a86462792855aa24ba16",
    value=0.2
)
calculate_output_hash(output0)

output2 = Output(
    index=2,
    address=address,
    value=input0.output_value - output0.value - output1.value - 0.001
)
calculate_output_hash(output0)

transaction = Transaction(
    inputs=[input0],
    outputs=[output0, output1, output2],
    value=input0.output_value - 0.001,
    fee=0.001
)
calculate_transaction_hash(transaction)

json_transaction = json_construct_transaction(transaction)

general_post_transaction(settings, json_node, json_transaction)
