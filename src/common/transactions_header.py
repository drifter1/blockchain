
class TransactionsHeader:
    def __init__(self, transaction_count: int = None, transaction_headers: list = None):

        self.transaction_count = transaction_count if (
            transaction_count != None) else 0
        self.transaction_headers = transaction_headers if (
            transaction_headers != None) else []


def json_construct_transactions_header(transactions_header: TransactionsHeader):
    return{
        "transaction_count": transactions_header.transaction_count,
        "transaction_headers": json_construct_transaction_headers(transactions_header.transaction_headers)
    }


def json_destruct_transactions_header(json_transactions_header: dict):
    transactions_header = TransactionsHeader()
    transactions_header.transaction_count = json_transactions_header["transaction_count"]
    json_transaction_headers = json_transactions_header["transaction_headers"]
    transactions_header.transaction_headers = json_destruct_transaction_headers(
        json_transaction_headers)

    return transactions_header


def json_construct_transaction_headers(transaction_headers: list):
    json_transaction_headers = []

    for transaction_header in transaction_headers:
        json_transaction_header = json_construct_transaction_header(
            transaction_header)
        json_transaction_headers.append(json_transaction_header)

    return json_transaction_headers


def json_destruct_transaction_headers(json_transaction_headers: dict):
    transaction_headers = []

    for json_transaction_header in json_transaction_headers:
        transaction_header = json_destruct_transaction_header(
            json_transaction_header)
        transaction_headers.append(transaction_header)

    return transaction_headers


def json_transactions_header_is_valid(json_transactions_header: dict):
    try:
        if len(json_transactions_header) == 2:
            keys = json_transactions_header.keys()
            if ("transaction_count" in keys) and ("transaction_headers" in keys):
                return True
            else:
                return False
        else:
            return False
    except:
        return False


class TransactionHeader:
    def __init__(self, timestamp: int = None, value: float = None, fee: float = None, hash: str = None):
        self.timestamp = timestamp
        self.value = value
        self.fee = fee
        self.hash = hash


def json_construct_transaction_header(transaction_header: TransactionHeader):
    return{
        "timestamp": transaction_header.timestamp,
        "value": transaction_header.value,
        "fee": transaction_header.fee,
        "hash": transaction_header.hash
    }


def json_destruct_transaction_header(json_transaction_header: dict):
    transaction_header = TransactionHeader()
    transaction_header.timestamp = json_transaction_header["timestamp"]
    transaction_header.value = json_transaction_header["value"]
    transaction_header.fee = json_transaction_header["fee"]
    transaction_header.hash = json_transaction_header["hash"]

    return transaction_header


def json_transaction_header_is_valid(json_transaction_header: dict):
    try:
        if len(json_transaction_header) == 4:
            keys = json_transaction_header.keys()
            if ("timestamp" in keys) and ("value" in keys):
                if ("fee" in keys) and ("hash" in keys):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except:
        return False


def json_transaction_to_transaction_header(json_transaction: dict):
    return{
        "timestamp": json_transaction["timestamp"],
        "value": json_transaction["value"],
        "fee": json_transaction["fee"],
        "hash": json_transaction["hash"]
    }


def json_transactions_to_transaction_headers(json_transactions: dict):
    json_transaction_headers = []

    for json_transaction in json_transactions:
        json_transaction_header = json_transaction_to_transaction_header(
            json_transaction)
        json_transaction_headers.append(json_transaction_header)

    return json_transaction_headers


def json_transactions_to_transactions_header(json_transactions: dict):
    return{
        "transaction_count": len(json_transactions),
        "transaction_headers": json_transactions_to_transaction_headers(json_transactions)
    }
