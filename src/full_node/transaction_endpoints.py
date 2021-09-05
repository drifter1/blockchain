from flask import Flask, request
from flask_api import status
import json

from full_node.settings import Full_Node_Settings
from full_node.transaction_validation import check_transaction_inputs, recalculate_and_check_transaction_hash, recalculate_and_check_transaction_values, verify_input_signatures
from full_node.network_relay import post_transaction_network_relay, remove_transaction_network_relay

from common.transaction import json_transaction_is_valid
from common.transaction_requests import local_retrieve_transactions


def transaction_endpoints(app: Flask, settings: Full_Node_Settings) -> None:

    @app.route('/transactions/', methods=['GET'])
    def retrieve_transactions():
        json_transactions = json.load(open(settings.transactions_path, "r"))

        return json.dumps(json_transactions), status.HTTP_200_OK

    @app.route('/transactions/', methods=['POST'])
    def post_transaction():

        json_transaction = request.get_json()

        # check JSON format
        if json_transaction_is_valid(json_transaction):

            # check transaction inputs
            if not check_transaction_inputs(settings, json_transaction["inputs"]):
                return {}, status.HTTP_400_BAD_REQUEST

            # recalculate and check the transaction input and output values and fee balancing
            if not recalculate_and_check_transaction_values(json_transaction):
                return {}, status.HTTP_400_BAD_REQUEST

            # recalculate and check hash
            if not recalculate_and_check_transaction_hash(json_transaction):
                return {}, status.HTTP_400_BAD_REQUEST

            # check input signatures
            if not verify_input_signatures(json_transaction["inputs"]):
                return {}, status.HTTP_400_BAD_REQUEST

            # add transaction if not already in transactions
            json_transactions, status_code = local_retrieve_transactions(
                settings)

            if json_transaction not in json_transactions:
                json_transactions.append(json_transaction)

                json.dump(obj=json_transactions, fp=open(
                    settings.transactions_path, "w"))
            else:
                return {}, status.HTTP_200_OK

            # network relay
            post_transaction_network_relay(settings, json_transaction)

            return json.dumps(json_transaction), status.HTTP_200_OK

        else:
            return {}, status.HTTP_400_BAD_REQUEST

    @app.route('/transactions/',  methods=['DELETE'])
    def remove_transaction():

        json_transaction = request.get_json()

        if json_transaction_is_valid(json_transaction):
            json_transactions, status_code = local_retrieve_transactions(
                settings)

            if json_transaction in json_transactions:
                json_transactions.remove(json_transaction)

                json.dump(obj=json_transactions, fp=open(
                    settings.transactions_path, "w"))

            else:
                return {}, status.HTTP_200_OK

            # network relay
            remove_transaction_network_relay(settings, json_transaction)

            return json.dumps(json_transaction), status.HTTP_200_OK

        else:
            return {}, status.HTTP_400_BAD_REQUEST
