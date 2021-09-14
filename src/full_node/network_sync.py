import os
import time
import json

from full_node.settings import Full_Node_Settings

from common.block_header import json_block_header_and_transactions_to_block
from common.blockchain import AddressBalancePair, json_construct_blockchain_info, json_destruct_blockchain_info
from common.utxo import UTXO_Output, json_construct_utxo_output

from common.node_requests import local_retrieve_node

from common.blockchain_requests import general_retrieve_blockchain_info, local_retrieve_blockchain_info, local_update_blockchain_info
from common.block_requests import general_retrieve_block_header, general_retrieve_block_transaction
from common.utxo_requests import local_add_utxo_output, local_remove_utxo_output, local_retrieve_utxo_output_from_address_and_transaction_hash, local_retrieve_utxo_address
from common.transaction_requests import general_retrieve_transactions_header, general_retrieve_transaction


def retrieve_blockchain_info(settings: Full_Node_Settings, json_node: dict):
    '''
        Retrieve blockchain info structures from the local endpoint and json_node.
    '''
    # retrieve local blockchain info
    json_local_blockchain_info, status_code = local_retrieve_blockchain_info(
        settings)

    if status_code != 200:
        print("Error in local blockchain info retrieval!")
        exit()

    local_blockchain_info = json_destruct_blockchain_info(
        json_local_blockchain_info)

    # retrieve blockchain info from first known node
    json_blockchain_info, status_code = general_retrieve_blockchain_info(
        settings, json_node)

    blockchain_info = json_destruct_blockchain_info(json_blockchain_info)

    return local_blockchain_info, blockchain_info


def retrieve_and_create_block(settings: Full_Node_Settings, json_node: dict, height: int):
    '''
        Retrieve the block header of the corresponding block height from the json_node
        and its transactions one-by-one. Afterwards, reconstruct the original block
        and create the local block file for it.
    '''
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

    return json_block


def update_utxo(settings: Full_Node_Settings, json_block: dict):
    '''
        Using the new block's transactions update the utxo's.
    '''
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

            json_utxo_output = json_construct_utxo_output(
                utxo_output)

            local_add_utxo_output(
                settings, json_output["address"], json_utxo_output)

        transaction_index += 1


def update_blockchain_info(settings: Full_Node_Settings, json_block: dict):
    '''
        Update the lcoal blockchain info structure using the new block information.
    '''
    # retrieve blockchain info
    json_blockchain_info, status_code = local_retrieve_blockchain_info(
        settings)
    blockchain_info = json_destruct_blockchain_info(
        json_blockchain_info)

    # update using block info
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

    # store new blockchain info
    json_blockchain_info = json_construct_blockchain_info(
        blockchain_info)
    local_update_blockchain_info(settings, json_blockchain_info)


def retrieve_unconfirmed_transactions(settings: Full_Node_Settings, json_node: dict):
    '''
        Replace local unconfirmed transactions with unconfirmed transacitons of json_node.
        The transactions are retrieve one-by-one and stored in the local file.
    '''
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


def network_sync(settings: Full_Node_Settings):
    '''
        Periodically, contact random known node to check if local files are up-to-date.
        If not then retrieve all the missing blocks and
        replace all local unconfirmed transactions.
    '''
    time.sleep(2)

    while True:

        print("Network Synchronization Started!")

        # random known node
        json_node, status_code = local_retrieve_node(settings, "random")

        if status_code == 200:
            # retrieve blockchain info structures
            local_blockchain_info, blockchain_info = retrieve_blockchain_info(
                settings, json_node)

            # check if blockchain is up to date
            if local_blockchain_info.height != blockchain_info.height:
                for height in range(local_blockchain_info.height + 1,  blockchain_info.height + 1):

                    # retrieve block and create block file
                    json_block = retrieve_and_create_block(
                        settings, json_node, height)

                    # update utxo
                    update_utxo(settings, json_block)

                    # update blockchain info
                    update_blockchain_info(settings, json_block)

                retrieve_unconfirmed_transactions(settings, json_node)

        print("Network Synchronization Finished!")

        # wait for a specific interval of time
        time.sleep(settings.sync_interval)
