from argparse import ArgumentParser
from flask import Flask

import os
import time
import _thread

from miner.settings import Miner_Settings
from miner.create_block import retrieve_unconfirmed_transactions, create_reward_transaction, solve_block

from common.node_endpoints import node_endpoints
from common.node_update import update_nodes

from common.block import Block, json_construct_block
from common.block_header import json_block_to_block_header
from common.transaction import json_destruct_transaction

from common.blockchain_requests import general_retrieve_blockchain_info
from common.block_requests import general_retrieve_last_block_header, general_create_block
from common.node_requests import local_retrieve_node, local_retrieve_nodes


def setup_files():
    '''
        Create the miner directory and nodes file (if they don't exist already).
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


def create_and_post_blocks():
    '''
        Creating, solving and posting blocks.
    '''
    time.sleep(2)

    while True:
        # retrieve random known node
        json_node, status_code = local_retrieve_node(settings, "random")

        if status_code != 200:
            exit()

        print("Retrieving Information...")

        # retrieve blockchain info
        json_blockchain_info, status_code = general_retrieve_blockchain_info(
            settings, json_node)

        # retrieve unconfirmed transactions
        json_transactions = retrieve_unconfirmed_transactions(
            settings, json_node)

        # retrieve last block header
        json_last_block_header, status_code = general_retrieve_last_block_header(
            settings, json_node)

        # create block
        print("Creating block...")
        block = Block()

        # if not first block
        if status_code == 200:
            block.height = json_last_block_header["height"] + 1
            block.prev_hash = json_last_block_header["hash"]
            block.reward = json_last_block_header["reward"]
        else:
            block.reward = json_blockchain_info["block_reward"]

        # headers
        block.creator = settings.reward_address
        block.transaction_count = len(json_transactions) + 1
        block.fees = 0
        try:
            if len(json_transactions) >= 0:
                for json_transaction in json_transactions:
                    block.fees += json_transaction["fee"]
        except:
            pass

        # reward transaction
        reward_transaction = create_reward_transaction(
            settings, block.timestamp, block.reward, block.fees)

        # add remaining transactions
        block.transactions = []
        block.transactions.append(reward_transaction)
        for json_transaction in json_transactions:
            transaction = json_destruct_transaction(json_transaction)
            block.transactions.append(transaction)

        # solve block
        print("Solving block...")
        solve_block(
            block, "00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")

        print("Found solution", block.nonce, "giving", block.hash)

        # construct JSON block
        json_block = json_construct_block(block)

        # construct JSON block header
        json_block_header = json_block_to_block_header(json_block)

        # send block to all known nodes
        print("Sending solution...")
        json_nodes, status_code = local_retrieve_nodes(settings)

        if status_code != 200:
            exit()

        for json_node in json_nodes:
            json_ret, status_code = general_create_block(
                settings, json_node, json_block_header)

            if status_code == 200:
                print("Solution accepted!")
            else:
                print("Solution declined!")

        time.sleep(5)


# client arguments
parser = ArgumentParser()
parser.add_argument("-i", "--ip", default=None, type=str,
                    help="ip address (default : 127.0.0.1)")
parser.add_argument("-p", "--port", default=None, type=int,
                    help="port (default : random in [50000, 60000])")
parser.add_argument("-d", "--dir", default=None, type=str,
                    help="directory (default : ../.miner)")
parser.add_argument("-n", "--nodes", default=None, type=str,
                    help="nodes filename (default : nodes.json)")
parser.add_argument("-u", "--upd_int", default=None,
                    type=int, help="update interval (default : 60)")
parser.add_argument("-k", "--kn_limit", default=None, type=int,
                    help="known nodes limit (default : 10)")
parser.add_argument("-di", "--dns_ip", default=None, type=str,
                    help="main dns ip address (default : 127.0.0.1)")
parser.add_argument("-dp", "--dns_port", default=None, type=int,
                    help="main dns ip port (default : 42020)")
parser.add_argument("-ra", "--rew_addr", default=None, type=str,
                    help="rewarding address (default : 0x0000000000000000000000000000000000000000)")
args = vars(parser.parse_args())

settings = Miner_Settings(
    ip_address=args["ip"], port=args["port"],
    directory=args["dir"], nodes_filename=args["nodes"],
    update_interval=args["upd_int"], known_nodes_limit=args["kn_limit"],
    main_dns_server_ip_address=args["dns_ip"], main_dns_server_port=args["dns_port"],
    reward_address=args["rew_addr"]
)

# setup directory and files
setup_files()

# flask app
app = Flask(__name__)

# add endpoints
node_endpoints(app, settings)

# start thread for regularly updating nodes
_thread.start_new_thread(update_nodes, (settings,))

# start thread for creating and posting blocks
_thread.start_new_thread(create_and_post_blocks, ())

# start flask app
if __name__ == "__main__":
    app.run(host=settings.ip_address, port=settings.port)
