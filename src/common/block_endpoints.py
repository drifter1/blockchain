from flask import Flask, request
import json

from common.block import calculate_block_hash, json_block_is_valid, json_destruct_block
from client.settings import Client_Settings
from common.block_requests import local_retrieve_block, local_retrieve_block_transactions, local_retrieve_block_transaction, local_retrieve_block_transaction_inputs, local_retrieve_block_transaction_outputs


def block_endpoints(app: Flask, settings: Client_Settings) -> None:

    @app.route('/blocks/<int:bid>/', methods=['GET'])
    def retrieve_block(bid):
        try:
            json_block = json.load(
                open(settings.block_file_path + str(bid) + ".json", "r"))

            if json_block_is_valid(json_block):
                return json.dumps(json_block)
            else:
                return {}
        except:
            return {}

    @app.route('/blocks/<int:bid>/transactions/', methods=['GET'])
    def retrieve_block_transactions(bid):
        json_block: dict = local_retrieve_block(settings, bid)

        if json_block_is_valid(json_block):
            if "transactions" in json_block.keys():
                return json.dumps(json_block["transactions"])
            else:
                return {}
        else:
            return {}

    @app.route('/blocks/<int:bid>/transactions/<int:tid>/', methods=['GET'])
    def retrieve_block_transaction(bid, tid):
        json_transactions = local_retrieve_block_transactions(settings, bid)

        try:
            return json.dumps(json_transactions[tid])
        except:
            return {}

    @app.route('/blocks/<int:bid>/transactions/<int:tid>/inputs/', methods=['GET'])
    def retrieve_block_transaction_inputs(bid, tid):
        json_transaction = local_retrieve_block_transaction(settings, bid, tid)

        try:
            return json.dumps(json_transaction["inputs"])
        except:
            return {}

    @app.route('/blocks/<int:bid>/transactions/<int:tid>/inputs/<int:iid>/', methods=['GET'])
    def retrieve_block_transaction_input(bid, tid, iid):
        json_transaction_inputs = local_retrieve_block_transaction_inputs(
            settings, bid, tid)

        try:
            return json.dumps(json_transaction_inputs[iid])
        except:
            return {}

    @app.route('/blocks/<int:bid>/transactions/<int:tid>/outputs/', methods=['GET'])
    def retrieve_block_transaction_outputs(bid, tid):
        json_transaction = local_retrieve_block_transaction(settings, bid, tid)

        try:
            return json.dumps(json_transaction["outputs"])
        except:
            return {}

    @app.route('/blocks/<int:bid>/transactions/<int:tid>/outputs/<int:oid>/', methods=['GET'])
    def retrieve_block_transaction_output(bid, tid, oid):
        json_transaction_outputs = local_retrieve_block_transaction_outputs(
            settings, bid, tid)

        try:
            return json.dumps(json_transaction_outputs[oid])
        except:
            return {}

    @app.route('/blocks/', methods=['POST'])
    def create_block():
        json_block = request.get_json()

        # check JSON format
        if json_block_is_valid(json_block):

            # recalculate and check hash
            try:
                block = json_destruct_block(json_block)

                calculate_block_hash(block)

                if block.hash != json_block["hash"]:
                    return {}

            except:
                return {}

            # missing checks for validity, consensus etc.

            # create block
            json.dump(obj=json_block, fp=open(
                settings.block_file_path + str(json_block["height"]) + ".json", "w"))

            return json.dumps(json_block)

        else:
            return {}
