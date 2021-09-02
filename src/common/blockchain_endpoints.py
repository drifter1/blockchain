from flask import Flask, request
import json

from full_node.settings import Full_Node_Settings
from common.blockchain import json_blockchain_info_is_valid


def blockchain_endpoints(app: Flask, settings: Full_Node_Settings) -> None:

    @app.route('/blockchain/', methods=['GET'])
    def retrieve_blockchain_info():
        json_blockchain = json.load(open(settings.blockchain_path, "r"))

        return json.dumps(json_blockchain)

    @app.route('/blockchain/', methods=['PUT'])
    def update_blockchain_info():
        json_blockchain_old = json.load(open(settings.blockchain_path, "r"))

        json_blockchain_new = request.get_json()

        if json_blockchain_info_is_valid(json_blockchain_new):

            json.dump(obj=json_blockchain_new, fp=open(
                settings.blockchain_path, "w"))

            return json.dumps(json_blockchain_new)

        return json.dumps(json_blockchain_old)
