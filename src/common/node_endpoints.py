from flask import Flask, request
import json
import requests

from common.node import json_node_is_valid
from common.settings import Node_Settings


def node_endpoints(app: Flask, settings: Node_Settings) -> None:

    @app.route('/', methods=['POST'])
    def initial_connection():
        json_node = request.get_json()

        if (json_node_is_valid(json_node)):

            # send request to local endpoint
            requests.post("http://" + settings.ip_address + ":" + str(settings.port) +
                          "/nodes/", json=json_node)

            return json_node
        else:
            return {}

    # Node Endpoints

    @app.route('/nodes/', methods=['GET'])
    def retrieve_nodes():
        json_nodes = json.load(open(settings.nodes_path, "r"))

        return json.dumps(json_nodes)

    @app.route('/nodes/', methods=['POST'])
    def add_node():
        json_nodes = json.load(open(settings.nodes_path, "r"))

        if request.get_json() not in json_nodes:
            json_nodes.append(request.get_json())

        json.dump(obj=json_nodes, fp=open(settings.nodes_path, "w"))

        return json.dumps(json_nodes)

    @app.route('/nodes/', methods=['DELETE'])
    def remove_node():
        json_nodes = json.load(open(settings.nodes_path, "r"))

        if request.get_json() in json_nodes:
            json_nodes.remove(request.get_json())

        json.dump(obj=json_nodes, fp=open(settings.nodes_path, "w"))

        return json.dumps(json_nodes)
