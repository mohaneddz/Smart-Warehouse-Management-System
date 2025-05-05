""" This module loads nodes from the JSON file made by Cilia and constructs Node objects.
    Returns a dictionary of Node objects with their IDs as keys.
    also contains 2 functions to calculate distances between 2 points , if you want you can implement other distances.
"""

import json
from core.node import Node

def load_nodes_from_json(file_path: str,distance = "Euclidean") -> dict:
    with open(file_path, 'r') as f:
        data = json.load(f)

    raw_nodes = data["nodes"]

    # First pass: Create Node objects
    nodes = {}
    for node_id, info in raw_nodes.items():
        node = Node(
            x=info["x"],
            y=info["y"],
            hash=node_id,
            neighbours={},  # Temporary
            value=0.0
        )
        node.locked = info.get("locked", False)
        node.heuristic = info.get("heuristic", 0)
        node.type = info.get("type", "normal")
        nodes[node_id] = node

    # Second pass: Assign neighbors with distance
    for node_id, info in raw_nodes.items():
        node = nodes[node_id]
        for neighbor_id in info["neighbours"]:
            if neighbor_id in nodes:
                neighbor = nodes[neighbor_id]
                if distance == "Euclidean":
                    dist = node.get_distance(neighbor)
                elif distance == "Manhattan":
                    dist = manhattan_distance(node.x, neighbor.x, node.y, neighbor.y)
                else:
                    raise ValueError("Unsupported distance metric. Use 'Euclidean' or 'Manhattan'.")
                node.neighbours[neighbor] = dist

    return nodes



def manhattan_distance(x1 : float , x2 : float , y1 : float, y2 : float) -> float:
    """Calculate the Manhattan distance between two nodes."""
    return abs(x1 - x2) + abs(y1 - y2)

def euclidean_distance(x1 : float , x2 : float , y1 : float, y2 : float) -> float:
    """Calculate the Euclidean distance between two nodes."""
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5