from flask import Flask, request
import json
import random

from common.node import json_node_is_valid, json_compare_nodes
from common.settings import Node_Settings
from common.node_requests import local_add_node, local_retrieve_nodes


def node_endpoints(app: Flask, settings: Node_Settings) -> None:

    @app.route('/', methods=['POST'])
    def connection_check():
        json_node = request.get_json()

        if json_node_is_valid(json_node):

            # send request to local endpoint
            local_add_node(settings, json_node)

        return settings.json_node, 200

    # Node Endpoints

    @app.route('/nodes/', methods=['GET'])
    def retrieve_nodes():
        json_node = request.get_json()

        if json_node_is_valid(json_node):
            local_add_node(settings, json_node)

        json_nodes = json.load(open(settings.nodes_path, "r"))

        return json.dumps(json_nodes), 200

    @app.route('/nodes/<string:nid>/', methods=['GET'])
    def retrieve_node(nid):
        json_nodes, status_code = local_retrieve_nodes(settings)

        if status_code != 200:
            return {}, 400

        if json_nodes == []:
            return {}, 400

        if nid == "random":
            node_index = random.randint(0, len(json_nodes) - 1)
        else:
            try:
                node_index = int(nid)
            except:
                return {}, 400

        json_node = json_nodes[node_index]

        if json_node_is_valid(json_node):
            return json.dumps(json_node), 200
        else:
            return {}, 400

    @app.route('/nodes/', methods=['POST'])
    def add_node():
        json_nodes: list = json.load(open(settings.nodes_path, "r"))

        json_node = request.get_json()

        if json_node_is_valid(json_node):

            if (json_node not in json_nodes) and (not json_compare_nodes(json_node, settings.json_node)):
                json_nodes.append(request.get_json())

                json.dump(obj=json_nodes, fp=open(settings.nodes_path, "w"))

        return json.dumps(json_nodes), 200

    @app.route('/nodes/', methods=['DELETE'])
    def remove_node():
        json_nodes: list = json.load(open(settings.nodes_path, "r"))

        json_node = request.get_json()

        if json_node_is_valid(json_node):
            if json_node in json_nodes:
                json_nodes.remove(request.get_json())

            json.dump(obj=json_nodes, fp=open(settings.nodes_path, "w"))

        return json.dumps(json_nodes), 200
