import time


class Block:
    def __init__(self, timestamp=None, height=None, reward=None, reward_address=None, nonce=None, transactions=None, hash=None, prev_hash=None):

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
        "transactions": block.transactions,
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
    block.transactions = json_block["transactions"]
    block.hash = json_block["hash"]
    block.prev_hash = json_block["prev_hash"]

    return block


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
