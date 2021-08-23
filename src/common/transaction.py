import time
from binascii import hexlify, unhexlify
from hashlib import sha256
from ecdsa.keys import SigningKey


class Transaction:
    def __init__(self, timestamp: int = None, sender: str = None, receiver: str = None, value: float = None, fee: float = None, hash: str = None, signature: str = None):

        self.timestamp = timestamp if (timestamp != None) else int(time.time())

        self.sender = sender
        self.receiver = receiver
        self.value = value
        self.fee = fee

        self.hash = hash
        self.signature = signature


def json_construct_transaction(transaction: Transaction):
    return {
        "timestamp": transaction.timestamp,
        "sender": transaction.sender,
        "receiver": transaction.receiver,
        "value": transaction.value,
        "fee": transaction.fee,
        "hash": transaction.hash,
        "signature": transaction.signature
    }


def json_destruct_transaction(json_transaction: dict):
    transaction = Transaction()
    transaction.timestamp = json_transaction["timestamp"]
    transaction.sender = json_transaction["sender"]
    transaction.receiver = json_transaction["receiver"]
    transaction.value = json_transaction["value"]
    transaction.fee = json_transaction["fee"]
    transaction.hash = json_transaction["hash"]
    transaction.signature = json_transaction["signature"]

    return transaction


def json_transaction_is_valid(json_transaction: dict):
    try:
        if len(json_transaction) == 7:
            keys = json_transaction.keys()
            if ("timestamp" in keys) and ("sender" in keys) and ("receiver" in keys):
                if ("value" in keys) and ("fee" in keys) and ("hash" in keys):
                    if ("signature" in keys):
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


def calculate_transaction_hash(transaction: Transaction):
    transaction_bytes = hexlify(bytes(str(transaction.timestamp), 'ascii'))
    transaction_bytes += hexlify(bytes(transaction.sender, 'ascii'))
    transaction_bytes += hexlify(bytes(transaction.receiver, 'ascii'))
    transaction_bytes += hexlify(bytes(str(transaction.value), 'ascii'))
    transaction_bytes += hexlify(bytes(str(transaction.fee), 'ascii'))

    hash = sha256(transaction_bytes).hexdigest()

    transaction.hash = hash


def sign_transaction(transaction: Transaction, private_key: SigningKey):
    signature = private_key.sign(unhexlify(transaction.hash))

    transaction.signature = hexlify(signature).decode('ascii')
