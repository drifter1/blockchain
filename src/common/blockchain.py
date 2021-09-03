import json


class AddressBalancePair:
    def __init__(self, address: str = None, balance: float = None):
        self.address = address
        self.balance = balance

    def __lt__(self, other):
        if (self.balance < other.balance):
            return True
        else:
            return False


def json_construct_address_balance_pair(address_balance_pair: AddressBalancePair):
    return{
        "address": address_balance_pair.address,
        "balance": address_balance_pair.balance
    }


def json_destruct_address_balance_pair(json_address_balance_pair: dict):
    address_balance_pair = AddressBalancePair()
    address_balance_pair.address = json_address_balance_pair["address"]
    address_balance_pair.balance = json_address_balance_pair["balance"]

    return address_balance_pair


def json_address_balance_pair_is_valid(json_address_balance_pair: dict):
    try:
        if len(json_address_balance_pair) == 2:
            keys = json_address_balance_pair.keys()
            if ("address" in keys) and ("balance" in keys):
                return True
            else:
                return False
        else:
            return False

    except:
        return False


class Blockchain:
    def __init__(self, name: str = None, height: int = None, total_transactions: int = None, total_addresses: int = None, block_time: int = None, block_reward: float = None, rich_list: list = None):

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

        self.rich_list = rich_list if (rich_list != None) else []


def json_construct_blockchain_info(blockchain: Blockchain):
    return {
        "name": blockchain.name,
        "height": blockchain.height,
        "total_transactions": blockchain.total_transactions,
        "total_addresses": blockchain.total_addresses,
        "block_time": blockchain.block_time,
        "block_reward": blockchain.block_reward,
        "rich_list": json_construct_rich_list(blockchain.rich_list)
    }


def json_destruct_blockchain_info(json_blockchain: dict):
    blockchain_info = Blockchain()
    blockchain_info.name = json_blockchain["name"]
    blockchain_info.height = json_blockchain["height"]
    blockchain_info.total_transactions = json_blockchain["total_transactions"]
    blockchain_info.total_addresses = json_blockchain["total_addresses"]
    blockchain_info.block_time = json_blockchain["block_time"]
    blockchain_info.block_reward = json_blockchain["block_reward"]
    json_rich_list = json_blockchain["rich_list"]
    blockchain_info.rich_list = json_destruct_rich_list(json_rich_list)

    return blockchain_info


def json_construct_rich_list(rich_list: list):
    json_rich_list = []

    for address_balance_pair in rich_list:
        json_address_balance_pair_input = json_construct_address_balance_pair(
            address_balance_pair)
        json_rich_list.append(json_address_balance_pair_input)

    return json_rich_list


def json_destruct_rich_list(json_rich_list: dict):
    rich_list = []

    for json_address_balance_pair_input in json_rich_list:
        address_balance_pair = json_destruct_address_balance_pair(
            json_address_balance_pair_input)
        rich_list.append(address_balance_pair)

    return rich_list


def json_blockchain_info_is_valid(json_blockchain: dict):
    try:
        if len(json_blockchain) == 7:
            keys = json_blockchain.keys()
            if ("name" in keys) and ("height" in keys) and ("total_transactions" in keys):
                if ("total_addresses" in keys) and ("block_time" in keys) and ("block_reward" in keys):
                    if ("rich_list" in keys):
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
