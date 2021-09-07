from flask_api import status
import time

from common.settings import Node_Settings

from common.node import json_destruct_node
from common.node_requests import general_connection_check, general_retrieve_nodes, local_add_node, local_remove_node, local_retrieve_nodes


def check_known_nodes(settings: Node_Settings, opt_json_node: dict):
    '''
        Check if known nodes are reachable using a connection check request,
        remove off-line nodes accordingly and check if the number of known nodes
        exceeds the required limit.
    '''
    json_nodes, status_code = local_retrieve_nodes(settings)

    if status_code != status.HTTP_200_OK:
        print("Error in local nodes retrieval!")
        exit()

    for json_node in json_nodes:
        try:
            general_connection_check(settings, json_node, opt_json_node)
        except:
            print("Node " + str(json_destruct_node(json_node)) + " is unreachable!")

            local_remove_node(settings, json_node)

    json_nodes, status_code = local_retrieve_nodes(settings)

    if status_code != status.HTTP_200_OK:
        print("Error in local nodes retrieval!")
        exit()

    settings.known_nodes = len(json_nodes)

    if settings.known_nodes >= settings.known_nodes_limit:
        return True
    else:
        return False


def retrieve_known_nodes_connections(settings: Node_Settings, opt_json_node: dict):
    '''
        Retrieve the known nodes's connections and add them to the known nodes.
        Afterwards, check if the number of known nodes exceeds the required limit.
    '''
    json_nodes, status_code = local_retrieve_nodes(settings)

    if status_code != status.HTTP_200_OK:
        print("Error in local nodes retrieval!")
        exit()

    for json_node in json_nodes:
        try:
            known_nodes, status_code = general_retrieve_nodes(
                settings, json_node, opt_json_node)

            if status_code != status.HTTP_200_OK:
                continue

            for known_node in known_nodes:
                local_add_node(settings, known_node)

        except:
            pass

    json_nodes, status_code = local_retrieve_nodes(settings)

    if status_code != status.HTTP_200_OK:
        print("Error in local nodes retrieval!")
        exit()

    settings.known_nodes = len(json_nodes)

    if settings.known_nodes >= settings.known_nodes_limit:
        return True
    else:
        return False


def contact_dns_server(settings: Node_Settings, opt_json_node: dict):
    '''
        As a last resort, and also as an initial connection mechanism,
        contact the DNS Server in order to retrieve its known nodes.
    '''
    try:
        json_nodes, status_code = general_retrieve_nodes(
            settings, settings.main_dns_server_json_node, opt_json_node)

        if status_code != status.HTTP_200_OK:
            print("DNS Server is unreachable!")
            return

        for json_node in json_nodes:
            local_add_node(settings, json_node)

    except:
        print("DNS Server is unreachable!")


def update_nodes(settings: Node_Settings, opt_json_node: dict = {}):
    '''
        Periodically, check if the known nodes are reachable by removing off-line ones.
        If the number of known nodes is not exceeding the required limit, then retrieve
        the known nodes's connections and add them to the known nodes.
        Lastly, as a last resort if the number of known nodes is still not sufficient,
        contact the DNS server in order to retrieve all of its known nodes.
    '''
    time.sleep(1)

    while True:
        print("Updating nodes started!")

        # check known nodes
        print("Checking known nodes...")
        if check_known_nodes(settings, opt_json_node):
            print("Updating nodes finished!")
            continue

        # retrieve connections of known nodes
        print("Retrieve connections of known nodes...")
        if retrieve_known_nodes_connections(settings, opt_json_node):
            print("Updating nodes finished!")
            continue

        # contact dns server
        print("Contacting dns server...")
        contact_dns_server(settings, opt_json_node)

        print("Updating nodes finished!")

        # wait for a specific interval of time
        time.sleep(settings.update_interval)
