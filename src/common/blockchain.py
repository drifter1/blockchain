import json


class Blockchain:
    def __init__(self, name=None, height=None, total_transactions=None, total_addresses=None, block_time=None, block_reward=None):

        # load defaults
        f = open("../defaults/blockchain_defaults.json")
        blockchain_defaults = json.load(f)
        f.close()

        self.name = name if (name != None) else blockchain_defaults["name"]
        self.height = height if (
            height != None) else blockchain_defaults["height"]
        self.total_transactions = total_transactions if (
            total_transactions != None) else blockchain_defaults["total_transactions"]
        self.total_addresses = total_addresses if (
            total_addresses != None) else blockchain_defaults["total_addresses"]
        self.block_time = block_time if (
            block_time != None) else blockchain_defaults["block_time"]
        self.block_reward = block_reward if (
            block_reward != None) else blockchain_defaults["block_reward"]


def json_construct_blockchain_info(blockchain: Blockchain):
    return {
        "name": blockchain.name,
        "height": blockchain.height,
        "total_transactions": blockchain.total_transactions,
        "total_addresses": blockchain.total_addresses,
        "block_time": blockchain.block_time,
        "block_reward": blockchain.block_reward
    }


def json_destruct_blockchain_info(json_blockchain: dict):
    blockchain_info = Blockchain()
    blockchain_info.name = json_blockchain["name"]
    blockchain_info.height = json_blockchain["height"]
    blockchain_info.total_transactions = json_blockchain["total_transactions"]
    blockchain_info.total_addresses = json_blockchain["total_addresses"]
    blockchain_info.block_time = json_blockchain["block_time"]
    blockchain_info.block_reward = json_blockchain["block_reward"]

    return blockchain_info


def json_blockchain_info_is_valid(json_blockchain: dict):
    try:
        if len(json_blockchain) == 6:
            keys = json_blockchain.keys()
            if ("name" in keys) and ("height" in keys) and ("total_transactions" in keys):
                if ("total_addresses" in keys) and ("block_time" in keys) and ("block_reward" in keys):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    except:
        return False
