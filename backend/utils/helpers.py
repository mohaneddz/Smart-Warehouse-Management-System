from core.node import Node

def load_nodes_from_json(json_data):
    nodes = {}
    for name, data in json_data["nodes"].items():
        node = Node(
            x=data["x"],
            y=data["y"],
            neighbours=data["neighbours"],
            value=data["value"],
            parent=data["parent"],
            heuristic=data["heuristic"]
        )
        node.type = data.get("type", "normal")
        nodes[name] = node
    return nodes
