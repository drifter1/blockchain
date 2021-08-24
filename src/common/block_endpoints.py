from flask import Flask, request
import json
import requests

from common.node import json_destruct_node
from common.block import calculate_block_hash, json_block_is_valid, json_destruct_block
from client.settings import Client_Settings


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
        json_block = local_retrieve_block(settings, bid)

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


# local requests


def local_retrieve_block(settings: Client_Settings, bid: int):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/blocks/" + str(bid) + "/").json()


def local_retrieve_block_transactions(settings: Client_Settings, bid: int):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/blocks/" + str(bid) + "/transactions/").json()


def local_retrieve_block_transaction(settings: Client_Settings, bid: int, tid: int):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/").json()


def local_create_block(settings: Client_Settings, json_block: dict):
    return requests.post("http://" + str(json_destruct_node(settings.json_node)) + "/blocks/", json=json_block).json()

# general requests


def general_retrieve_block(target_node: dict, bid: int):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/blocks/" + str(bid) + "/").json()


def general_retrieve_block_transactions(target_node: dict, bid: int):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/blocks/" + str(bid) + "/transactions/").json()


def general_retrieve_block_transaction(target_node: dict, bid: int, tid: int):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/blocks/" + str(bid) + "/transactions/" + str(tid) + "/").json()


def general_create_block(target_node: dict, json_block: dict):
    return requests.post("http://" + str(json_destruct_node(target_node)) + "/blocks/", json=json_block).json()
