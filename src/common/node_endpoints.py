from flask import Flask, request
import json
import requests

from common.node import json_node_is_valid, json_destruct_node, json_compare_nodes
from common.settings import Node_Settings


def node_endpoints(app: Flask, settings: Node_Settings) -> None:

    @app.route('/', methods=['POST'])
    def connection_check():
        json_node = request.get_json()

        if json_node_is_valid(json_node):

            # send request to local endpoint
            local_add_node(settings, json_node)

        return settings.json_node

    # Node Endpoints

    @app.route('/nodes/', methods=['GET'])
    def retrieve_nodes():
        json_node = request.get_json()

        if json_node_is_valid(json_node):
            local_add_node(settings, json_node)

        json_nodes = json.load(open(settings.nodes_path, "r"))

        return json.dumps(json_nodes)

    @app.route('/nodes/', methods=['POST'])
    def add_node():
        json_nodes: list = json.load(open(settings.nodes_path, "r"))

        json_node = request.get_json()

        if json_node_is_valid(json_node):

            if (json_node not in json_nodes) and (not json_compare_nodes(json_node, settings.json_node)):
                json_nodes.append(request.get_json())

                json.dump(obj=json_nodes, fp=open(settings.nodes_path, "w"))

        return json.dumps(json_nodes)

    @app.route('/nodes/', methods=['DELETE'])
    def remove_node():
        json_nodes: list = json.load(open(settings.nodes_path, "r"))

        json_node = request.get_json()

        if json_node_is_valid(json_node):
            if json_node in json_nodes:
                json_nodes.remove(request.get_json())

            json.dump(obj=json_nodes, fp=open(settings.nodes_path, "w"))

        return json.dumps(json_nodes)

# local requests


def local_retrieve_nodes(settings: Node_Settings):
    return requests.get("http://" + str(json_destruct_node(settings.json_node)) + "/nodes/", json=settings.json_node).json()


def local_add_node(settings: Node_Settings, json_node: dict):
    return requests.post("http://" + str(json_destruct_node(settings.json_node)) + "/nodes/", json=json_node).json()


def local_remove_node(settings: Node_Settings, json_node: dict):
    return requests.delete("http://" + str(json_destruct_node(settings.json_node)) + "/nodes/", json=json_node).json()

# general requests


def general_connection_check(target_node: dict, opt_json_node: dict = {}):
    return requests.post("http://" + str(json_destruct_node(target_node)) + "/", json=opt_json_node).json()


def general_retrieve_nodes(target_node: dict, opt_json_node: dict = {}):
    return requests.get("http://" + str(json_destruct_node(target_node)) + "/nodes/", json=opt_json_node).json()


def general_add_node(target_node: dict, json_node: dict):
    return requests.post("http://" + str(json_destruct_node(target_node)) + "/nodes/", json=json_node).json()


def general_remove_node(target_node: dict, json_node: dict):
    return requests.delete("http://" + json_destruct_node(target_node) + "/nodes/", json=json_node).json()
