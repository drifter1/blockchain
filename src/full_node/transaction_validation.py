from binascii import unhexlify

from full_node.settings import Full_Node_Settings

from common.transaction import Input, Output, json_destruct_input, json_destruct_output, json_destruct_transaction, calculate_transaction_hash, json_destruct_transaction_inputs
from common.utxo import json_destruct_utxo_output, json_utxo_output_is_valid
from common.wallet import verify_signature

from common.block_requests import local_retrieve_block_transaction_output
from common.utxo_requests import local_retrieve_utxo_output_from_address_and_transaction_hash


def check_transaction_input(settings: Full_Node_Settings, json_transaction_input: dict):
    '''
        Check the transaction input by retrieving the referenced UTXO output
        and its corresponding block transaction output.
        Finally, also check if the value referenced is the same.
    '''
    try:
        transaction_input = json_destruct_input(json_transaction_input)
    except:
        return False

    # retrieve utxo output
    json_utxo_output, status_code = local_retrieve_utxo_output_from_address_and_transaction_hash(
        settings, transaction_input.output_address, transaction_input.transaction_hash)

    if status_code != 200:
        return False

    if not json_utxo_output_is_valid(json_utxo_output):
        return False

    utxo_output = json_destruct_utxo_output(json_utxo_output)

    # retrieve block transaction output
    json_block_transaction_output, status_code = local_retrieve_block_transaction_output(
        settings, utxo_output.block_height, utxo_output.transaction_index, utxo_output.output_index)

    if status_code != 200:
        return False

    block_transaction_output = json_destruct_output(
        json_block_transaction_output)

    # check value coherence
    if transaction_input.output_value != block_transaction_output.value:
        return False

    # all OK
    return True


def check_transaction_inputs(settings: Full_Node_Settings, json_transaction_inputs: dict):
    '''
        Check all the transaction inputs by retrieving their referenced UTXO output
        and corresponding block transaction output.
        Finally, also check if the value referenced is the same.
    '''

    # check each transaction input
    for json_transaction_input in json_transaction_inputs:
        if not check_transaction_input(settings, json_transaction_input):
            return False

    # all OK
    return True


def recalculate_and_check_transaction_values(json_transaction: dict):
    '''
        Recalculate and check if the total input (value + fee) and
        total output (value) are balanced out correctly.
    '''
    transaction = json_destruct_transaction(json_transaction)

    # recalculate and check total input (value + fee)
    total_input = 0
    input: Input
    for input in transaction.inputs:
        total_input += input.output_value

    if total_input != transaction.value + transaction.fee:
        return False

    # recalculate and check total output (value)
    total_output = 0
    output: Output
    for output in transaction.outputs:
        total_output += output.value

    if total_output != transaction.value:
        return False

    # all OK
    return True


def recalculate_and_check_transaction_hash(json_transaction: dict):
    '''
        Recalculate and check if transaction hash is correct.
    '''
    try:
        transaction = json_destruct_transaction(json_transaction)
    except:
        return False

    calculate_transaction_hash(transaction)

    if transaction.hash != json_transaction["hash"]:
        return False

    # all OK
    return True


def verify_input_signatures(json_transaction_inputs: dict):
    '''
        Verify the input signatures by recovering the public keys from
        the signature-hash pair and checking if hashing either of them
        leads to the address referenced.
    '''
    try:
        inputs = json_destruct_transaction_inputs(json_transaction_inputs)
    except:
        return False

    input: Input
    for input in inputs:
        signature = unhexlify(input.signature)
        hash = unhexlify(input.output_hash)

        try:
            if not verify_signature(signature, hash, input.output_address):
                return False
        except:
            return False

    # all OK
    return True
