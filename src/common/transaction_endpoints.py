from flask import Flask, request
import json
import requests
from binascii import unhexlify

from common.node import json_destruct_node
from common.transaction import Input, Output, json_destruct_transaction, json_transaction_is_valid, calculate_transaction_hash
from common.wallet import verify_signature
from client.settings import Client_Settings


def transaction_endpoints(app: Flask, settings: Client_Settings) -> None:

    @app.route('/transactions/', methods=['GET'])
    def retrieve_transactions():
        json_transactions = json.load(open(settings.transactions_path, "r"))

        return json.dumps(json_transactions)

    @app.route('/transactions/', methods=['POST'])
    def post_transaction():

        json_transaction = request.get_json()

        # check JSON format
        if json_transaction_is_valid(json_transaction):

            transaction = json_destruct_transaction(json_transaction)

            # recalculate and check total_input
            total_input = 0
            input: Input
            for input in transaction.inputs:
                total_input += input.output_value

            if total_input != transaction.total_input:
                return {}

            # recalculate and check total_output
            total_output = 0
            output: Output
            for output in transaction.outputs:
                total_output += output.value

            if total_output != transaction.total_output:
                return {}

            # check if total_input - fee == total_output
            if transaction.total_input - transaction.fee != transaction.total_output:
                return {}

            # recalculate and check hash
            try:
                calculate_transaction_hash(transaction)

                if transaction.hash != json_transaction["hash"]:
                    return {}
            except:
                return {}

            # check input signatures
            input: Input
            for input in transaction.inputs:
                signature = unhexlify(input.signature)
                hash = unhexlify(input.output_hash)

                try:
                    if not verify_signature(signature, hash, input.output_address):
                        return{}
                except:
                    return{}

            # add transaction if not already in transactions
            json_transactions: list = local_retrieve_transactions(settings)

            if json_transaction not in json_transactions:
                json_transactions.append(json_transaction)

                json.dump(obj=json_transactions, fp=open(
                    settings.transactions_path, "w"))

                return json.dumps(json_transaction)
            else:
                return {}

        else:
            return {}

    @app.route('/transactions/',  methods=['DELETE'])
    def cancel_transaction():

        json_transaction = request.get_json()

        if json_transaction_is_valid(json_transaction):
            json_transactions: list = local_retrieve_transactions(settings)

            if json_transaction in json_transactions:
                json_transactions.remove(json_transaction)

                json.dump(obj=json_transactions, fp=open(
                    settings.transactions_path, "w"))

                return json.dumps(json_transaction)

            else:
                return {}
        else:
            return {}


# local requests


def local_retrieve_transactions(settings: Client_Settings):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/transactions/").json()


def local_post_transaction(settings: Client_Settings, json_transaction: dict):
    return requests.post("http://" + str(json_destruct_node(settings.json_node)) + "/transactions/", json=json_transaction).json()


def local_cancel_transaction(settings: Client_Settings, json_transaction: dict):
    return requests.delete("http://" + str(json_destruct_node(settings.json_node)) + "/transactions/", json=json_transaction).json()

# general requests


def general_retrieve_transactions(target_node: dict):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/transactions/").json()


def general_post_transaction(target_node: dict, json_transaction: dict):
    return requests.post("http://" + str(json_destruct_node(target_node)) + "/transactions/", json=json_transaction).json()


def general_cancel_transaction(target_node: dict, json_transaction: dict):
    return requests.delete("http://" + str(json_destruct_node(target_node)) + "/transactions/", json=json_transaction).json()
