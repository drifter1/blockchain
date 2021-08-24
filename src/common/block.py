import time
from binascii import hexlify
from hashlib import sha256
from common.transaction import json_construct_transaction, json_destruct_transaction


class Block:
    def __init__(self, timestamp: int = None, height: int = None, reward: float = None, reward_address: str = None, nonce: str = None, transactions: list = None, hash: str = None, prev_hash: str = None):

        self.timestamp = timestamp if (timestamp != None) else int(time.time())

        self.height = height
        self.reward = reward
        self.reward_address = reward_address
        self.nonce = nonce

        self.transactions = transactions

        self.hash = hash
        self.prev_hash = prev_hash


def json_construct_block(block: Block):
    return {
        "timestamp": block.timestamp,
        "height": block.height,
        "reward": block.reward,
        "reward_address": block.reward_address,
        "nonce": block.nonce,
        "transactions": json_construct_block_transactions(block.transactions),
        "hash": block.hash,
        "prev_hash": block.prev_hash
    }


def json_destruct_block(json_block: dict):
    block = Block()
    block.timestamp = json_block["timestamp"]
    block.height = json_block["height"]
    block.reward = json_block["reward"]
    block.reward_address = json_block["reward_address"]
    block.nonce = json_block["nonce"]
    json_transactions = json_block["transactions"]
    block.transactions = json_destruct_block_transactions(json_transactions)
    block.hash = json_block["hash"]
    block.prev_hash = json_block["prev_hash"]

    return block


def json_construct_block_transactions(transactions: list):
    json_transactions = []

    for transaction in transactions:
        json_transaction = json_construct_transaction(transaction)
        json_transactions.append(json_transaction)

    return json_transactions


def json_destruct_block_transactions(json_transactions: dict):
    transactions = []

    for json_transaction in json_transactions:
        transaction = json_destruct_transaction(json_transaction)
        transactions.append(transaction)

    return transactions


def json_block_is_valid(json_block: dict):
    try:
        if len(json_block) == 8:
            keys = json_block.keys()
            if ("timestamp" in keys) and ("height" in keys) and ("reward" in keys):
                if ("reward_address" in keys) and ("nonce" in keys) and ("transactions" in keys):
                    if ("hash" in keys) and ("prev_hash" in keys):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    except:
        return False


def calculate_block_hash(block: Block):
    block_bytes = hexlify(bytes(str(block.timestamp), 'ascii'))
    block_bytes += hexlify(bytes(str(block.height), 'ascii'))
    block_bytes += hexlify(bytes(str(block.reward), 'ascii'))
    block_bytes += hexlify(bytes(block.reward_address, 'ascii'))
    block_bytes += hexlify(bytes(block.nonce, 'ascii'))
    for transaction in block.transactions:
        block_bytes += hexlify(bytes(transaction.hash, 'ascii'))
    block_bytes += hexlify(bytes(block.prev_hash, 'ascii'))

    hash = sha256(block_bytes).hexdigest()

    block.hash = hash
