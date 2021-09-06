import time
from binascii import hexlify
from hashlib import sha256
from common.transaction import Transaction, json_construct_transaction, json_destruct_transaction


class Block:
    def __init__(self, timestamp: int = None, height: int = None, creator: str = None, reward: float = None, fees: float = None, nonce: str = None, transaction_count: int = None, transactions: list = None, hash: str = None, prev_hash: str = None):

        self.timestamp = timestamp if (timestamp != None) else int(time.time())

        self.height = height if(height != None) else 0
        self.creator = creator if (
            creator != None) else "0x0000000000000000000000000000000000000000"
        self.reward = reward
        self.fees = fees
        self.nonce = nonce

        self.transaction_count = transaction_count
        self.transactions = transactions

        self.hash = hash if (
            hash != None) else "0000000000000000000000000000000000000000000000000000000000000000"
        self.prev_hash = prev_hash if (
            prev_hash != None) else "0000000000000000000000000000000000000000000000000000000000000000"


def json_construct_block(block: Block):
    return {
        "timestamp": block.timestamp,
        "height": block.height,
        "creator": block.creator,
        "reward": block.reward,
        "fees": block.fees,
        "nonce": block.nonce,
        "transaction_count": block.transaction_count,
        "transactions": json_construct_block_transactions(block.transactions),
        "hash": block.hash,
        "prev_hash": block.prev_hash
    }


def json_destruct_block(json_block: dict):
    block = Block()
    block.timestamp = json_block["timestamp"]
    block.height = json_block["height"]
    block.creator = json_block["creator"]
    block.reward = json_block["reward"]
    block.fees = json_block["fees"]
    block.nonce = json_block["nonce"]
    block.transaction_count = json_block["transaction_count"]
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
        if len(json_block) == 10:
            keys = json_block.keys()
            if ("timestamp" in keys) and ("height" in keys) and ("creator" in keys):
                if ("reward" in keys) and ("fees" in keys) and ("nonce" in keys):
                    if ("transaction_count" in keys) and ("transactions" in keys):
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
        else:
            return False
    except:
        return False


def calculate_block_hash(block: Block):
    block_bytes = hexlify(bytes(str(block.timestamp), 'ascii'))
    block_bytes += hexlify(bytes(str(block.height), 'ascii'))
    block_bytes += hexlify(bytes(block.creator, 'ascii'))
    block_bytes += hexlify(bytes(str(block.reward), 'ascii'))
    block_bytes += hexlify(bytes(str(block.fees), 'ascii'))
    block_bytes += hexlify(bytes(block.nonce, 'ascii'))
    block_bytes += hexlify(bytes(str(block.transaction_count), 'ascii'))
    transaction: Transaction
    for transaction in block.transactions:
        block_bytes += hexlify(bytes(transaction.hash, 'ascii'))
    block_bytes += hexlify(bytes(block.prev_hash, 'ascii'))

    hash = sha256(block_bytes).hexdigest()

    block.hash = hash
