from flask import Flask, request
import json
import _thread

from full_node.settings import Full_Node_Settings
from full_node.transaction_validation import check_transaction_inputs, recalculate_and_check_transaction_hash, recalculate_and_check_transaction_values, verify_input_signatures
from full_node.network_relay import post_transaction_network_relay, remove_transaction_network_relay

from common.transaction import json_transaction_is_valid
from common.transactions_header import json_transactions_to_transactions_header

def transaction_endpoints(app: Flask, settings: Full_Node_Settings) -> None:

    @app.route('/transactions/', methods=['GET'])
    def retrieve_transactions_header():
        try:
            json_transactions = json.load(
                open(settings.transactions_path, "r"))

            json_transaction_header = json_transactions_to_transactions_header(
                json_transactions)

            return json.dumps(json_transaction_header), 200
        except:
            return {}, 400

    @app.route('/transactions/<string:tid>/', methods=['GET'])
    def retrieve_transaction(tid):
        try:
            json_transactions = json.load(
                open(settings.transactions_path, "r"))
        except:
            return {}, 400

        # if transaction index
        try:
            transaction_index = int(tid)

            return json.dumps(json_transactions[transaction_index]), 200
        except:
            pass

        # if transaction hash
        for json_transaction in json_transactions:
            transaction_hash = json_transaction["hash"]

            if transaction_hash == tid:
                return json.dumps(json_transaction), 200

        return {}, 400

    @app.route('/transactions/', methods=['POST'])
    def post_transaction():

        json_transaction = request.get_json()

        # check JSON format
        if json_transaction_is_valid(json_transaction):

            # check transaction inputs
            if not check_transaction_inputs(settings, json_transaction["inputs"]):
                return {}, 400

            # recalculate and check the transaction input and output values and fee balancing
            if not recalculate_and_check_transaction_values(json_transaction):
                return {}, 400

            # recalculate and check hash
            if not recalculate_and_check_transaction_hash(json_transaction):
                return {}, 400

            # check input signatures
            if not verify_input_signatures(json_transaction["inputs"]):
                return {}, 400

            # add transaction if not already in transactions
            try:
                json_transactions: list = json.load(
                    open(settings.transactions_path, "r"))
            except:
                return {}, 400

            if json_transaction not in json_transactions:
                json_transactions.append(json_transaction)

                json.dump(obj=json_transactions, fp=open(
                    settings.transactions_path, "w"))
            else:
                return {}, 200

            # network relay
            _thread.start_new_thread(
                post_transaction_network_relay, (settings, json_transaction))

            return json.dumps(json_transaction), 200

        else:
            return {}, 400

    @app.route('/transactions/',  methods=['DELETE'])
    def remove_transaction():

        json_transaction = request.get_json()

        if json_transaction_is_valid(json_transaction):
            try:
                json_transactions: list = json.load(
                    open(settings.transactions_path, "r"))
            except:
                return {}, 400

            if json_transaction in json_transactions:
                json_transactions.remove(json_transaction)

                json.dump(obj=json_transactions, fp=open(
                    settings.transactions_path, "w"))

            else:
                return {}, 200

            # network relay
            _thread.start_new_thread(
                remove_transaction_network_relay, (settings, json_transaction))

            return json.dumps(json_transaction), 200

        else:
            return {}, 400
