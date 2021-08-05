
class Node:
    def __init__(self, ip_address: str, port: int):
        self.ip_address = ip_address
        self.port = port

    def __repr__(self) -> str:
        return self.ip_address + ":" + str(self.port)


def json_construct_node(ip_address: str, port: int):
    return {
        "ip_address": ip_address,
        "port": port
    }


def json_destruct_node(json_node: dict):
    if json_node_is_valid(json_node):

        ip_address = json_node["ip_address"]
        port = json_node["port"]

        return Node(ip_address=ip_address, port=port)


def json_compare_nodes(json_node1: dict, json_node2: dict):
    if json_node_is_valid(json_node1) and json_node_is_valid(json_node2):
        if (json_node1["ip_address"] == json_node2["ip_address"]) and (json_node1["port"] == json_node2["port"]):
            return True
        else:
            return False
    else:
        return False


def json_node_is_valid(json_node: dict):
    try:
        if len(json_node) == 2:
            keys = json_node.keys()
            if ("ip_address" in keys) and ("port" in keys):
                return True
            else:
                return False
        else:
            return False
    except:
        return False
