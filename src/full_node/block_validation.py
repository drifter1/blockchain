
from full_node.settings import Full_Node_Settings
from full_node.transaction_validation import check_transaction_input

from common.block import json_destruct_block, calculate_block_hash
from common.block_header import json_destruct_block_header
from common.transaction import Input, Output, Transaction, calculate_transaction_hash, calculate_output_hash, json_construct_transaction
from common.transactions_header import TransactionHeader, json_destruct_transactions_header

from common.block_requests import local_retrieve_last_block_header
from common.transaction_requests import local_retrieve_transaction


def rebuild_block_transactions(settings: Full_Node_Settings, json_block_header: dict, json_transactions_header: dict):
    '''
        Rebuild block transactions from the block header and unconfirmed transactions.
    '''
    json_block_transactions = []

    block_header = json_destruct_block_header(json_block_header)
    transactions_header = json_destruct_transactions_header(
        json_transactions_header)

    # check if unconfirmed transactions are sufficient
    if block_header.transaction_count > transactions_header.transaction_count + 1:
        return [], False

    # rebuild reward transaction
    reward_transaction_value = block_header.reward + block_header.fees

    reward_input = Input(
        output_value=reward_transaction_value
    )

    reward_output = Output(
        address=block_header.creator,
        value=reward_transaction_value
    )
    calculate_output_hash(reward_output)

    reward_transaction = Transaction(
        timestamp=block_header.timestamp,
        inputs=[reward_input],
        outputs=[reward_output],
        value=reward_transaction_value,
        fee=0
    )
    calculate_transaction_hash(reward_transaction)

    # add reward transaction first
    json_reward_transaction = json_construct_transaction(reward_transaction)

    json_block_transactions.append(json_reward_transaction)

    # retrieve remaining transactions
    transaction_headers = block_header.transaction_headers

    for tid in range(1, block_header.transaction_count):
        transaction_header: TransactionHeader = transaction_headers[tid]
        transaction_hash = transaction_header.hash

        json_transaction, status_code = local_retrieve_transaction(
            settings, transaction_hash)

        if status_code != 200:
            return [], False

        json_block_transactions.append(json_transaction)

    return json_block_transactions, True


def check_previous_block(settings: Full_Node_Settings, json_block: dict):
    '''
        Check previous block hash is correct and height is +1.
    '''
    try:
        block = json_destruct_block(json_block)

        json_last_block_header, status_code = local_retrieve_last_block_header(
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
