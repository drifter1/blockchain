
# UTXO Output

class UTXO_Output:
    def __init__(self, block_height: int = None, transaction_hash: str = None, transaction_index: int = None, output_index: int = None):

        self.block_height = block_height
        self.transaction_hash = transaction_hash
        self.transaction_index = transaction_index
        self.output_index = output_index


def json_construct_utxo_output(utxo_output: UTXO_Output):
    return {
        "block_height": utxo_output.block_height,
        "transaction_hash": utxo_output.transaction_hash,
        "transaction_index": utxo_output.transaction_index,
        "output_index": utxo_output.output_index
    }


def json_destruct_utxo_output(json_utxo_output: dict):
    utxo_output = UTXO_Output()
    utxo_output.block_height = json_utxo_output["block_height"]
    utxo_output.transaction_hash = json_utxo_output["transaction_hash"]
    utxo_output.transaction_index = json_utxo_output["transaction_index"]
    utxo_output.output_index = json_utxo_output["output_index"]

    return utxo_output


def json_utxo_output_is_valid(json_utxo_output: dict):
    try:
        if len(json_utxo_output) == 4:
            keys = json_utxo_output.keys()
            if ("block_height" in keys) and ("transaction_hash" in keys):
                if ("transaction_index" in keys) and ("output_index" in keys):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except:
        return False


# Main UTXO

class UTXO:
    def __init__(self, utxo_outputs: list = None, balance: float = None):

        self.utxo_outputs = utxo_outputs if(utxo_outputs != None) else []
        self.balance = balance if(balance != None) else 0


def json_construct_utxo(utxo: UTXO):
    return{
        "utxo_outputs": json_construct_utxo_outputs(utxo.utxo_outputs),
        "balance": utxo.balance
    }


def json_destruct_utxo(json_utxo: dict):
    utxo = UTXO()
    json_utxo_outputs = json_utxo["utxo_outputs"]
    utxo.utxo_outputs = json_destruct_utxo_outputs(json_utxo_outputs)
    utxo.balance = json_utxo["balance"]

    return utxo


def json_construct_utxo_outputs(utxo_outputs: list):
    json_utxo_outputs = []

    for utxo_output in utxo_outputs:
        json_utxo_output = json_construct_utxo_output(utxo_output)
        json_utxo_outputs.append(json_utxo_output)

    return json_utxo_outputs


def json_destruct_utxo_outputs(json_utxo_outputs: dict):
    utxo_outputs = []

    for json_utxo_output in json_utxo_outputs:
        utxo_output = json_destruct_utxo_output(json_utxo_output)
        utxo_outputs.append(utxo_output)

    return json_utxo_outputs


def json_utxo_is_valid(json_utxo: dict):
    try:
        if len(json_utxo) == 2:
            keys = json_utxo.keys()
            if ("utxo_outputs" in keys) and ("balance" in keys):
                json_utxo_outputs = json_utxo["utxo_outputs"]
                for json_utxo_output in json_utxo_outputs:
                    if not json_utxo_output_is_valid(json_utxo_output):
                        return False
                return True
            else:
                return False
        else:
            return False
    except:
        return False

# UTXO Info


class UTXO_Info:
    def __init__(self, last_block_included: int = None, total_address_count: int = None):
        self.last_block_included = last_block_included if (
            last_block_included != None) else -1
        self.total_address_count = total_address_count if (
            total_address_count != None) else 0


def json_construct_utxo_info(utxo_info: UTXO_Info):
    return{
        "last_block_included": utxo_info.last_block_included,
        "total_address_count": utxo_info.total_address_count
    }


def json_destruct_utxo_info(json_utxo_info: dict):
    utxo_info = UTXO_Info()
    utxo_info.last_block_included = json_utxo_info["last_block_included"]
    utxo_info.total_address_count = json_utxo_info["total_address_count"]

    return utxo_info


def json_utxo_info_is_valid(json_utxo_info: dict):
    try:
        if len(json_utxo_info) == 2:
            keys = json_utxo_info.keys()
            if ("last_block_included" in keys) and ("total_address_count" in keys):
                return True
            else:
                return False
        else:
            return False
    except:
        return False
