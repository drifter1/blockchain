from flask import Flask, request
import json
import os

from full_node.settings import Full_Node_Settings
from full_node.block_validation import recalculate_and_check_block_hash, check_block_transactions

from common.block import json_block_is_valid
from common.blockchain import json_destruct_blockchain_info, json_construct_blockchain_info
from common.utxo import UTXO_Output, json_construct_utxo_output

from common.block_requests import local_retrieve_block, local_retrieve_block_transactions, local_retrieve_block_transaction, local_retrieve_block_transaction_inputs, local_retrieve_block_transaction_outputs
from common.blockchain_requests import local_retrieve_blockchain_info, local_update_blockchain_info
from common.transaction_requests import local_remove_transaction
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
            if not recalculate_and_check_block_hash(json_block):
                return {}

            # check transactions
            if not check_block_transactions(settings, json_block["transactions"]):
                return {}

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

            # update blockchain info
            json_blockchain_info = local_retrieve_blockchain_info(settings)
            blockchain_info = json_destruct_blockchain_info(
                json_blockchain_info)

            blockchain_info.height = json_block["height"]
            blockchain_info.total_addresses = len(
                os.listdir(settings.utxo_path))
            blockchain_info.total_transactions += len(
                json_block["transactions"])

            json_blockchain_info = json_construct_blockchain_info(
                blockchain_info)
            local_update_blockchain_info(settings, json_blockchain_info)

            return json.dumps(json_block)

        else:
            return {}
