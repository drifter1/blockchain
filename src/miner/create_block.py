
import time

from miner.settings import Miner_Settings

from common.block import Block, calculate_block_hash
from common.transaction import Input, Output, Transaction, calculate_output_hash, calculate_transaction_hash

from common.transaction_requests import general_retrieve_transaction, general_retrieve_transactions_header


def retrieve_unconfirmed_transactions(settings: Miner_Settings, target_node: dict):
    '''
        Retrieve unconfirmed transactions from target node one-by-one.
    '''
    # retrieve unconfirmed transactions header
    json_transactions_header, status_code = general_retrieve_transactions_header(
        settings, target_node)

    if status_code != 200:
        return []

    transaction_count = json_transactions_header["transaction_count"]

    # retrieve unconfirmed transactions one-by-one
    json_transactions = []
    for tid in range(0, transaction_count):
        json_transaction, status_code = general_retrieve_transaction(
            settings, target_node, tid)

        if status_code != 200:
            continue

        json_transactions.append(json_transaction)

    return json_transactions


def create_reward_transaction(settings: Miner_Settings, block_reward: float, block_fees: float):
    '''
        Create reward transaction with a value equal to the block reward plus the fees.
    '''
    transaction_value = block_reward + block_fees

    reward_input = Input(
        output_value=transaction_value
    )

    reward_output = Output(
        address=settings.reward_address,
        value=transaction_value
    )
    calculate_output_hash(reward_output)

    reward_transaction = Transaction(
        inputs=[reward_input],
        outputs=[reward_output],
        value=transaction_value,
        fee=0
    )
    calculate_transaction_hash(reward_transaction)

    return reward_transaction


def solve_block(block: Block, target_hash: str):
    '''
        Find the solution nonce for the block.
    '''
    while True:
        block.timestamp = int(time.time())

        for nonce in range(0, 1 << 32):
            block.nonce = "{:08x}".format(nonce)

            if (nonce != 0) and (nonce % (1 << 20) == 0):
                print("Tried", nonce, "nonces...")

            # calculate hash
            calculate_block_hash(block)

            # check if smaller then target_hash
            if int(block.hash, 16) < int(target_hash, 16):
                return
