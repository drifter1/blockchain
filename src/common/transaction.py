import time
from binascii import hexlify, unhexlify
from hashlib import sha256
from ecdsa.keys import SigningKey


# Transaction Output

class Output:
    def __init__(self, index: int = None, address: str = None, value: float = None, hash: str = None):
        self.index = index if (index != None) else 0
        self.address = address if (
            address != None) else "0x0000000000000000000000000000000000000000"
        self.value = value if (value != None) else 0
        self.hash = hash if (
            hash != None) else "0000000000000000000000000000000000000000000000000000000000000000"


def json_construct_output(output: Output):
    return {
        "index": output.index,
        "address": output.address,
        "value": output.value,
        "hash": output.hash
    }


def json_destruct_output(json_output: dict):
    output = Output()
    output.index = json_output["index"]
    output.address = json_output["address"]
    output.value = json_output["value"]
    output.hash = json_output["hash"]

    return output


def calculate_output_hash(output: Output):
    output_bytes = hexlify(bytes(str(output.index), 'ascii'))
    output_bytes += hexlify(bytes(output.address, 'ascii'))
    output_bytes += hexlify(bytes(str(output.value), 'ascii'))

    hash = sha256(output_bytes).hexdigest()
    output.hash = hash

# Transaction Input


class Input:
    def __init__(self, transaction_hash: str = None, output_index: int = None, output_address: str = None, output_value: float = None, output_hash: str = None, signature: str = None):
        self.transaction_hash = transaction_hash if (
            transaction_hash != None) else "0000000000000000000000000000000000000000000000000000000000000000"
        self.output_index = output_index if(output_index != None) else 0
        self.output_address = output_address if (
            output_address != None) else "0x0000000000000000000000000000000000000000"
        self.output_value = output_value if (output_value != None) else 0
        self.output_hash = output_hash if (
            output_hash != None) else "0000000000000000000000000000000000000000000000000000000000000000"
        self.signature = signature if (
            signature != None) else "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"


def json_construct_input(input: Input):
    return {
        "transaction_hash": input.transaction_hash,
        "output_index": input.output_index,
        "output_address": input.output_address,
        "output_value": input.output_value,
        "output_hash": input.output_hash,
        "signature": input.signature
    }


def json_destruct_input(json_input: dict):
    input = Input()
    input.transaction_hash = json_input["transaction_hash"]
    input.output_index = json_input["output_index"]
    input.output_address = json_input["output_address"]
    input.output_value = json_input["output_value"]
    input.output_hash = json_input["output_hash"]
    input.signature = json_input["signature"]

    return input


def sign_input(input: Input, private_key: SigningKey):
    signature = private_key.sign(unhexlify(input.output_hash))

    input.signature = hexlify(signature).decode('ascii')


# Transaction

class Transaction:
    def __init__(self, timestamp: int = None, inputs: list = None, outputs: list = None, value: float = None, fee: float = None, hash: str = None):

        self.timestamp = timestamp if (timestamp != None) else int(time.time())

        self.inputs = inputs
        self.outputs = outputs

        self.value = value if (value != None) else 0
        self.fee = fee if(fee != None) else 0

        self.hash = hash if (
            hash != None) else "0000000000000000000000000000000000000000000000000000000000000000"


def json_construct_transaction(transaction: Transaction):
    return {
        "timestamp": transaction.timestamp,
        "inputs": json_construct_transaction_inputs(transaction.inputs),
        "outputs": json_construct_transaction_outputs(transaction.outputs),
        "value": transaction.value,
        "fee": transaction.fee,
        "hash": transaction.hash
    }


def json_destruct_transaction(json_transaction: dict):
    transaction = Transaction()
    transaction.timestamp = json_transaction["timestamp"]
    json_inputs = json_transaction["inputs"]
    transaction.inputs = json_destruct_transaction_inputs(json_inputs)
    json_outputs = json_transaction["outputs"]
    transaction.outputs = json_destruct_transaction_outputs(json_outputs)
    transaction.value = json_transaction["value"]
    transaction.fee = json_transaction["fee"]
    transaction.hash = json_transaction["hash"]

    return transaction


def json_construct_transaction_inputs(inputs: list):
    json_inputs = []

    for input in inputs:
        json_input = json_construct_input(input)
        json_inputs.append(json_input)

    return json_inputs


def json_destruct_transaction_inputs(json_inputs: dict):
    inputs = []

    for json_input in json_inputs:
        input = json_destruct_input(json_input)
        inputs.append(input)

    return inputs


def json_construct_transaction_outputs(outputs: list):
    json_outputs = []

    for output in outputs:
        json_output = json_construct_output(output)
        json_outputs.append(json_output)

    return json_outputs


def json_destruct_transaction_outputs(json_outputs: dict):
    outputs = []

    for json_output in json_outputs:
        output = json_destruct_output(json_output)
        outputs.append(output)

    return outputs


def json_transaction_is_valid(json_transaction: dict):
    try:
        if len(json_transaction) == 6:
            keys = json_transaction.keys()
            if ("timestamp" in keys) and ("inputs" in keys) and ("outputs" in keys):
                if ("value" in keys) and ("fee" in keys) and ("hash" in keys):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except:
        return False


def calculate_transaction_hash(transaction: Transaction):
    transaction_bytes = hexlify(bytes(str(transaction.timestamp), 'ascii'))
    input: Input
    for input in transaction.inputs:
        transaction_bytes += hexlify(bytes(input.transaction_hash, 'ascii'))
        transaction_bytes += hexlify(bytes(str(input.output_index), 'ascii'))
        transaction_bytes += hexlify(bytes(input.output_address, 'ascii'))
        transaction_bytes += hexlify(bytes(str(input.output_value), 'ascii'))
        transaction_bytes += hexlify(bytes(input.output_hash, 'ascii'))
        transaction_bytes += hexlify(bytes(input.signature, 'ascii'))
    output: Output
    for output in transaction.outputs:
        transaction_bytes += hexlify(bytes(str(output.index), 'ascii'))
        transaction_bytes += hexlify(bytes(output.address, 'ascii'))
        transaction_bytes += hexlify(bytes(str(output.value), 'ascii'))
        transaction_bytes += hexlify(bytes(output.hash, 'ascii'))
    transaction_bytes += hexlify(bytes(str(transaction.value), 'ascii'))
    transaction_bytes += hexlify(bytes(str(transaction.fee), 'ascii'))

    hash = sha256(transaction_bytes).hexdigest()

    transaction.hash = hash
