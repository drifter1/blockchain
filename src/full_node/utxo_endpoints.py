from flask import Flask, request
import json

from full_node.settings import Full_Node_Settings

from common.utxo import UTXO, json_construct_utxo, json_destruct_utxo_output, json_utxo_is_valid, json_utxo_output_is_valid
from common.transaction import json_destruct_output

from common.block_requests import local_retrieve_block_transaction_output
from common.utxo_requests import local_retrieve_utxo_address, local_retrieve_utxo_outputs_of_address, local_create_utxo


def utxo_endpoints(app: Flask, settings: Full_Node_Settings) -> None:

    @app.route('/utxo/<string:address>/', methods=['GET'])
    def retrieve_utxo_of_address(address):
        try:
            json_utxo = json.load(
                open(settings.utxo_file_path + address + ".json", "r"))

            if json_utxo_is_valid(json_utxo):
                return json.dumps(json_utxo)
            else:
                return {}
        except:
            return {}

    @app.route('/utxo/<string:address>/outputs/', methods=['GET'])
    def retrieve_utxo_outputs_of_address(address):
        try:
            json_utxo = local_retrieve_utxo_address(settings, address)

            json_utxo_outputs = json_utxo["utxo_outputs"]

            return json.dumps(json_utxo_outputs)

        except:
            return {}

    @app.route('/utxo/<string:address>/outputs/<string:transaction_hash>/', methods=['GET'])
    def retrieve_utxo_output_from_address_transaction_hash_pair(address, transaction_hash):
        try:
            json_utxo_outputs = local_retrieve_utxo_outputs_of_address(
                settings, address)

            for json_utxo_output in json_utxo_outputs:
                if json_utxo_output_is_valid(json_utxo_output):
                    if json_utxo_output["transaction_hash"] == transaction_hash:
                        return json.dumps(json_utxo_output)

            # if transaction_hash doesn't occur return nothing
            return {}
        except:
            return {}

    @app.route('/utxo/<string:address>/', methods=['POST'])
    def create_utxo_of_address(address):

        json_utxo = request.get_json()

        if not json_utxo_is_valid(json_utxo):

            # create new blank UTXO
            utxo = UTXO()
            json_utxo = json_construct_utxo(utxo)

        # check if outputs truly exist
        json_utxo_outputs = json_utxo["utxo_outputs"]

        for json_utxo_output in json_utxo_outputs:
            if json_utxo_output_is_valid(json_utxo_output):
                if not check_utxo_output_in_block(settings, address, json_utxo_output):
                    return {}

        try:
            # create utxo
            json.dump(obj=json_utxo, fp=open(
                settings.utxo_file_path + address + ".json", "w"))

            return json.dumps(json_utxo)

        except:
            return {}

    @app.route('/utxo/<string:address>/outputs/', methods=['POST'])
    def add_utxo_output_to_utxo_of_address(address):

        json_utxo_output = request.get_json()

        if json_utxo_output_is_valid(json_utxo_output):

            # check if output truly exists
            output_exists, transaction_output = check_utxo_output_in_block(
                settings, address, json_utxo_output)

            if not output_exists:
                return {}

            # retrieve utxo for address
            json_utxo = local_retrieve_utxo_address(settings, address)

            if not json_utxo_is_valid(json_utxo):
                utxo = UTXO()
                json_utxo = json_construct_utxo(utxo)

            # add utxo output
            json_utxo_outputs: list = json_utxo["utxo_outputs"]

            if json_utxo_output not in json_utxo_outputs:
                json_utxo_outputs.append(json_utxo_output)

                json_utxo["utxo_outputs"] = json_utxo_outputs
                json_utxo["last_block_included"] = json_utxo_output["block_height"]
                json_utxo["balance"] += transaction_output.value

                local_create_utxo(settings, address, json_utxo)

                return json.dumps(json_utxo_output)

            return {}
        else:
            return {}

    @app.route('/utxo/<string:address>/outputs/', methods=['DELETE'])
    def remove_utxo_output_from_utxo_of_address(address):

        json_utxo_output = request.get_json()

        if json_utxo_output_is_valid(json_utxo_output):
            json_utxo = local_retrieve_utxo_address(settings, address)

            if not json_utxo_is_valid(json_utxo):
                return {}

            output_exists, transaction_output = check_utxo_output_in_block(
                settings, address, json_utxo_output)

            if not output_exists:
                return {}

            json_utxo_outputs: list = json_utxo["utxo_outputs"]

            if json_utxo_output in json_utxo_outputs:
                json_utxo_outputs.remove(json_utxo_output)

                json_utxo["utxo_outputs"] = json_utxo_outputs
                json_utxo["balance"] -= transaction_output.value

                local_create_utxo(settings, address, json_utxo)

                return json.dumps(json_utxo_output)

            return {}
        else:
            return {}


# check if utxo output is valid using block transaction output retrieval request

def check_utxo_output_in_block(settings: Full_Node_Settings, address: str, json_utxo_output: dict):
    utxo_output = json_destruct_utxo_output(json_utxo_output)

    json_transaction_output = local_retrieve_block_transaction_output(
        settings, utxo_output.block_height, utxo_output.transaction_index, utxo_output.output_index)

    if json_transaction_output == {}:
        return False, None

    transaction_output = json_destruct_output(json_transaction_output)

    if transaction_output.address == address:
        return True, transaction_output
