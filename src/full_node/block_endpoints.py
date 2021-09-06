from flask import Flask, request
from flask_api import status
import json
import os

from full_node.settings import Full_Node_Settings
from full_node.block_validation import check_previous_block, recalculate_and_check_block_hash, check_block_transactions
from full_node.network_relay import create_block_network_relay

from common.block import json_block_is_valid
from common.blockchain import AddressBalancePair, json_blockchain_info_is_valid, json_destruct_blockchain_info, json_construct_blockchain_info
from common.utxo import UTXO_Output, json_construct_utxo_output

from common.block_requests import local_retrieve_block, local_retrieve_block_transactions, local_retrieve_block_transaction, local_retrieve_block_transaction_inputs, local_retrieve_block_transaction_outputs
from common.blockchain_requests import local_retrieve_blockchain_info, local_update_blockchain_info
from common.transaction_requests import local_remove_transaction
from common.utxo_requests import local_remove_utxo_output, local_retrieve_utxo_address, local_retrieve_utxo_output_from_address_and_transaction_hash, local_add_utxo_output


def block_endpoints(app: Flask, settings: Full_Node_Settings) -> None:

    @app.route('/blocks/<int:bid>/', methods=['GET'])
    def retrieve_block(bid):
        try:
            json_block = json.load(
                open(settings.block_file_path + str(bid) + ".json", "r"))

            if json_block_is_valid(json_block):
                return json.dumps(json_block), status.HTTP_200_OK
            else:
                return {}, status.HTTP_400_BAD_REQUEST
        except:
            return {}, status.HTTP_400_BAD_REQUEST

    @app.route('/blocks/last/', methods=['GET'])
    def retrieve_last_block():
        # retrieve blockchain info
        json_blockchain_info, status_code = local_retrieve_blockchain_info(
            settings)

        if status_code != status.HTTP_200_OK:
            return {}, status.HTTP_400_BAD_REQUEST

        if not json_blockchain_info_is_valid(json_blockchain_info):
            return {}, status.HTTP_400_BAD_REQUEST

        # blockchain height
        height = json_blockchain_info["height"]

        # load last block
        try:
            json_block = json.load(
                open(settings.block_file_path + str(height) + ".json", "r"))

            if json_block_is_valid(json_block):
                return json.dumps(json_block), status.HTTP_200_OK
            else:
                return {}, status.HTTP_400_BAD_REQUEST
        except:
            return {}, status.HTTP_400_BAD_REQUEST

    @app.route('/blocks/<int:bid>/transactions/', methods=['GET'])
    def retrieve_block_transactions(bid):
        json_block, status_code = local_retrieve_block(settings, bid)

        if status_code != status.HTTP_200_OK:
            return {}, status.HTTP_400_BAD_REQUEST

        if json_block_is_valid(json_block):
            if "transactions" in json_block.keys():
                return json.dumps(json_block["transactions"]), status.HTTP_200_OK
            else:
                return {}, status.HTTP_400_BAD_REQUEST
        else:
            return {}, status.HTTP_400_BAD_REQUEST

    @app.route('/blocks/<int:bid>/transactions/<int:tid>/', methods=['GET'])
    def retrieve_block_transaction(bid, tid):
        json_transactions, status_code = local_retrieve_block_transactions(
            settings, bid)

        if status_code != status.HTTP_200_OK:
            return {}, status.HTTP_400_BAD_REQUEST

        try:
            return json.dumps(json_transactions[tid]), status.HTTP_200_OK
        except:
            return {}, status.HTTP_400_BAD_REQUEST

    @app.route('/blocks/<int:bid>/transactions/<int:tid>/inputs/', methods=['GET'])
    def retrieve_block_transaction_inputs(bid, tid):
        json_transaction, status_code = local_retrieve_block_transaction(
            settings, bid, tid)

        if status_code != status.HTTP_200_OK:
            return {}, status.HTTP_400_BAD_REQUEST

        try:
            return json.dumps(json_transaction["inputs"]), status.HTTP_200_OK
        except:
            return {}, status.HTTP_400_BAD_REQUEST

    @app.route('/blocks/<int:bid>/transactions/<int:tid>/inputs/<int:iid>/', methods=['GET'])
    def retrieve_block_transaction_input(bid, tid, iid):
        json_transaction_inputs, status_code = local_retrieve_block_transaction_inputs(
            settings, bid, tid)

        if status_code != status.HTTP_200_OK:
            return {}, status.HTTP_400_BAD_REQUEST

        try:
            return json.dumps(json_transaction_inputs[iid]), status.HTTP_200_OK
        except:
            return {}, status.HTTP_400_BAD_REQUEST

    @app.route('/blocks/<int:bid>/transactions/<int:tid>/outputs/', methods=['GET'])
    def retrieve_block_transaction_outputs(bid, tid):
        json_transaction, status_code = local_retrieve_block_transaction(
            settings, bid, tid)

        if status_code != status.HTTP_200_OK:
            return {}, status.HTTP_400_BAD_REQUEST

        try:
            return json.dumps(json_transaction["outputs"]), status.HTTP_200_OK
        except:
            return {}, status.HTTP_400_BAD_REQUEST

    @app.route('/blocks/<int:bid>/transactions/<int:tid>/outputs/<int:oid>/', methods=['GET'])
    def retrieve_block_transaction_output(bid, tid, oid):
        json_transaction_outputs, status_code = local_retrieve_block_transaction_outputs(
            settings, bid, tid)

        if status_code != status.HTTP_200_OK:
            return {}, status.HTTP_400_BAD_REQUEST

        try:
            return json.dumps(json_transaction_outputs[oid]), status.HTTP_200_OK
        except:
            return {}, status.HTTP_400_BAD_REQUEST

    @app.route('/blocks/', methods=['POST'])
    def create_block():
        json_block = request.get_json()

        # check JSON format
        if json_block_is_valid(json_block):

            # check if block already exists
            json_block_local, status_code = local_retrieve_block(
                settings, json_block["height"])

            if status_code == status.HTTP_200_OK:
                if json_block_is_valid(json_block_local):
                    return {}, status.HTTP_200_OK

            # check previous block hash and height
            if not check_previous_block(settings, json_block):
                return {}, status.HTTP_400_BAD_REQUEST

            # recalculate and check hash
            if not recalculate_and_check_block_hash(json_block):
                return {}, status.HTTP_400_BAD_REQUEST

            # check transactions
            if not check_block_transactions(settings, json_block["transactions"]):
                return {}, status.HTTP_400_BAD_REQUEST

            # missing consensus

            # create block
            json.dump(obj=json_block, fp=open(
                settings.block_file_path + str(json_block["height"]) + ".json", "w"))

            # network relay
            create_block_network_relay(settings, json_block)

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
                    json_utxo_output, status_code = local_retrieve_utxo_output_from_address_and_transaction_hash(
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
            json_blockchain_info, status_code = local_retrieve_blockchain_info(
                settings)
            blockchain_info = json_destruct_blockchain_info(
                json_blockchain_info)

            blockchain_info.height = json_block["height"]
            blockchain_info.total_addresses = len(
                os.listdir(settings.utxo_path))
            blockchain_info.total_transactions += len(
                json_block["transactions"])

            # rich list calculation (currently inefficient)
            blockchain_info.rich_list = []
            for utxo_file in os.listdir(settings.utxo_path):
                address = utxo_file[5:47]
                utxo_address, status_code = local_retrieve_utxo_address(
                    settings, address)
                balance = utxo_address["balance"]
                address_balance_pair = AddressBalancePair(address, balance)
                blockchain_info.rich_list.append(address_balance_pair)
            blockchain_info.rich_list.sort(reverse=True)
            while len(blockchain_info.rich_list) > 10:
                blockchain_info.rich_list.pop()

            json_blockchain_info = json_construct_blockchain_info(
                blockchain_info)
            local_update_blockchain_info(settings, json_blockchain_info)

            return json.dumps(json_block), status.HTTP_200_OK

        else:
            return {}, status.HTTP_400_BAD_REQUEST
