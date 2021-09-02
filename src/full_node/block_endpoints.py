from flask import Flask, request
import json

from full_node.settings import Full_Node_Settings
from full_node.transaction_endpoints import check_transaction_input

from common.block import calculate_block_hash, json_block_is_valid, json_destruct_block
from common.utxo import UTXO_Output, json_construct_utxo_output

from common.block_requests import local_retrieve_block, local_retrieve_block_transactions, local_retrieve_block_transaction, local_retrieve_block_transaction_inputs, local_retrieve_block_transaction_outputs, local_retrieve_block_transaction_output
from common.transaction_requests import local_remove_transaction, local_retrieve_transactions
from common.utxo_requests import local_remove_utxo_output, local_retrieve_utxo_output_from_address_and_transaction_hash, local_add_utxo_output


def block_endpoints(app: Flask, settings: Full_Node_Settings) -> None:

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

            # check transactions
            json_transactions = json_block["transactions"]

            json_unconfirmed_transactions = local_retrieve_transactions(
                settings)

            for json_transaction in json_transactions:

                # don't check coinbase transaction
                if json_transaction["inputs"][0]["output_address"] == "0x0000000000000000000000000000000000000000":
                    continue

                # check if transaction in unconfirmed transactions array
                if json_transaction not in json_unconfirmed_transactions:
                    return {}

                json_inputs = json_transaction["inputs"]

                # keep track of referenced outputs
                json_checked_inputs = []

                # check if inputs are in utxo
                for json_input in json_inputs:

                    if not check_transaction_input(settings, json_input):
                        return {}

                    if json_input in json_checked_inputs:
                        return {}

                    json_checked_inputs.append(json_input)

            # missing consensus

            # create block
            json.dump(obj=json_block, fp=open(
                settings.block_file_path + str(json_block["height"]) + ".json", "w"))

            # remove included transactions from unconfirmed transactions
            for json_transaction in json_block["transactions"]:

                # skip coinbase transaction
                if json_transaction["inputs"][0]["output_address"] == "0x0000000000000000000000000000000000000000":
                    continue

                local_remove_transaction(settings, json_transaction)

            # update utxo's
            transaction_index = 0
            for json_transaction in json_block["transactions"]:

                # coinbase transaction
                if transaction_index == 0:
                    utxo_reward_output = UTXO_Output(
                        block_height=json_block["height"],
                        transaction_hash=json_transaction["hash"],
                        transaction_index=0,
                        output_index=0
                    )

                    json_utxo_reward_output = json_construct_utxo_output(
                        utxo_reward_output)

                    local_add_utxo_output(
                        settings, json_transaction["outputs"][0]["address"], json_utxo_reward_output)

                    transaction_index += 1
                    continue

                # remove spent outputs

                for json_input in json_transaction["inputs"]:
                    json_utxo_output = local_retrieve_utxo_output_from_address_and_transaction_hash(
                        settings, json_input["output_address"], json_input["transaction_hash"])

                    local_remove_utxo_output(
                        settings, json_input["output_address"], json_utxo_output)

                # add spendable outputs

                for json_output in json_transaction["outputs"]:
                    utxo_output = UTXO_Output(
                        block_height=json_block["height"],
                        transaction_hash=json_transaction["hash"],
                        transaction_index=transaction_index,
                        output_index=json_output["index"]
                    )

                    json_utxo_output = json_construct_utxo_output(utxo_output)

                    local_add_utxo_output(
                        settings, json_output["address"], json_utxo_output)

                transaction_index += 1

            return json.dumps(json_block)

        else:
            return {}
