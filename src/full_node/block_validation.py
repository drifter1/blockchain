
from full_node.settings import Full_Node_Settings
from full_node.transaction_validation import check_transaction_input

from common.block import json_destruct_block, calculate_block_hash
from common.block_requests import local_retrieve_last_block


def check_previous_block(settings: Full_Node_Settings, json_block: dict):
    '''
        Check previous block hash is correct and height is +1.
    '''
    try:
        block = json_destruct_block(json_block)

        json_last_block_header, status_code = local_retrieve_last_block(
            settings)

        # block is first block if no block was returned
        if status_code != 200:
            if not block.height == 0:
                return False

            if not block.prev_hash == "0000000000000000000000000000000000000000000000000000000000000000":
                return False

        # previous block exists
        else:
            if not json_last_block_header["hash"] == block.prev_hash:
                return False

            if not json_last_block_header["height"] + 1 == block.height:
                return False
    except:
        return False

    # all OK
    return True


def recalculate_and_check_block_hash(json_block: dict):
    '''
        Recalculate and check if block hash is correct.
    '''
    try:
        block = json_destruct_block(json_block)

        calculate_block_hash(block)

        if block.hash != json_block["hash"]:
            return False

    except:
        return False

    # all OK
    return True


def check_block_transactions(settings: Full_Node_Settings, json_transactions: dict):
    '''
        Check if the transaction inputs are in the UTXO and
        keep track of checked inputs to prevent double-spending. 
    '''

    # keep track of referenced outputs
    json_checked_inputs = []

    # for each transaction
    for json_transaction in json_transactions:

        # don't check coinbase transaction
        if json_transaction["inputs"][0]["output_address"] == "0x0000000000000000000000000000000000000000":
            continue

        json_inputs = json_transaction["inputs"]

        # check if inputs are in utxo, and also prevent double-spending
        for json_input in json_inputs:

            if not check_transaction_input(settings, json_input):
                return False

            if json_input in json_checked_inputs:
                return False

            json_checked_inputs.append(json_input)

    # all OK
    return True
