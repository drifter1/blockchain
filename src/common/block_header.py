import time


class BlockHeader:
    def __init__(self, timestamp: int = None, height: int = None, creator: str = None, reward: float = None, fees: float = None, nonce: str = None, transaction_count: int = None, hash: str = None, prev_hash: str = None):

        self.timestamp = timestamp if (timestamp != None) else int(time.time())

        self.height = height if(height != None) else 0
        self.creator = creator if (
            creator != None) else "0x0000000000000000000000000000000000000000"
        self.reward = reward
        self.fees = fees
        self.nonce = nonce

        self.transaction_count = transaction_count

        self.hash = hash if (
            hash != None) else "0000000000000000000000000000000000000000000000000000000000000000"
        self.prev_hash = prev_hash if (
            prev_hash != None) else "0000000000000000000000000000000000000000000000000000000000000000"


def json_construct_block_header(block_header: BlockHeader):
    return {
        "timestamp": block_header.timestamp,
        "height": block_header.height,
        "creator": block_header.creator,
        "reward": block_header.reward,
        "fees": block_header.fees,
        "nonce": block_header.nonce,
        "transaction_count": block_header.transaction_count,
        "hash": block_header.hash,
        "prev_hash": block_header.prev_hash
    }


def json_destruct_block_header(json_block_header: dict):
    block_header = BlockHeader()
    block_header.timestamp = json_block_header["timestamp"]
    block_header.height = json_block_header["height"]
    block_header.creator = json_block_header["creator"]
    block_header.reward = json_block_header["reward"]
    block_header.fees = json_block_header["fees"]
    block_header.nonce = json_block_header["nonce"]
    block_header.transaction_count = json_block_header["transaction_count"]
    block_header.hash = json_block_header["hash"]
    block_header.prev_hash = json_block_header["prev_hash"]

    return block_header


def json_block_header_is_valid(json_block_header: dict):
    try:
        if len(json_block_header) == 9:
            keys = json_block_header.keys()
            if ("timestamp" in keys) and ("height" in keys) and ("creator" in keys):
                if ("reward" in keys) and ("fees" in keys) and ("nonce" in keys):
                    if ("transaction_count" in keys) and ("hash" in keys) and ("prev_hash" in keys):
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


def json_block_to_block_header(json_block: dict):
    return {
        "timestamp": json_block["timestamp"],
        "height": json_block["height"],
        "creator": json_block["creator"],
        "reward": json_block["reward"],
        "fees": json_block["fees"],
        "nonce": json_block["nonce"],
        "transaction_count": json_block["transaction_count"],
        "hash": json_block["hash"],
        "prev_hash": json_block["prev_hash"]
    }


def json_block_header_and_transactions_to_block(json_block_header: dict, json_block_transactions: dict):
    return {
        "timestamp": json_block_header["timestamp"],
        "height": json_block_header["height"],
        "creator": json_block_header["creator"],
        "reward": json_block_header["reward"],
        "fees": json_block_header["fees"],
        "nonce": json_block_header["nonce"],
        "transaction_count": json_block_header["transaction_count"],
        "transactions": json_block_transactions,
        "hash": json_block_header["hash"],
        "prev_hash": json_block_header["prev_hash"]
    }
