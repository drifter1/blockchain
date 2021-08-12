from flask import Flask, request
import json
import requests

from common.node import json_destruct_node
from common.transaction import json_transaction_is_valid
from client.settings import Client_Settings


def transaction_endpoints(app: Flask, settings: Client_Settings) -> None:

    @app.route('/transactions/', methods=['GET'])
    def retrieve_transactions():
        json_transactions = json.load(open(settings.transactions_path, "r"))

        return json.dumps(json_transactions)

    @app.route('/transactions/', methods=['POST'])
    def post_transaction():

        json_transaction = request.get_json()

        if json_transaction_is_valid(json_transaction):
            json_transactions = local_retrieve_transactions(settings)

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
            json_transactions = local_retrieve_transactions(settings)

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
