from full_node.settings import Full_Node_Settings
from full_node.transaction_validation import check_transaction_input

from common.block import json_destruct_block, calculate_block_hash
from common.transaction_requests import local_retrieve_transactions


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
        Check if transactions are in unconfirmed transaction array (except coinbase transaction),
        if their inputs are in the UTXO and keep track of checked inputs to prevent double-spending. 
    '''
    # retrieve unconfirmed transactions
    json_unconfirmed_transactions = local_retrieve_transactions(settings)

    # keep track of referenced outputs
    json_checked_inputs = []

    # for each transaction
    for json_transaction in json_transactions:

        # don't check coinbase transaction
        if json_transaction["inputs"][0]["output_address"] == "0x0000000000000000000000000000000000000000":
            continue

        # check if transaction in unconfirmed transactions array
        if json_transaction not in json_unconfirmed_transactions:
            return False

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
