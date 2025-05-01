from core.node import Node
from typing import Dict, List

def create_example_map() -> Dict[str, Node]:
    """Creates an example warehouse map with 20 nodes.
    
    Returns:
        Dict[str, Node]: A dictionary mapping node hashes to Node objects
    """
    # Define node positions in a grid-like layout
    positions = [
        (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),  # Row 1
        (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),  # Row 2
        (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),  # Row 3
        (0, 3), (1, 3), (2, 3), (3, 3), (4, 3)   # Row 4
    ]
    
    # Create nodes
    nodes: Dict[str, Node] = {}
    for i, (x, y) in enumerate(positions):
        node_hash = f"node_{i+1}"
        nodes[node_hash] = Node(x, y, node_hash, {}, 0.0)
    
    # Connect nodes (create neighbors)
    for i, (x, y) in enumerate(positions):
        current_node = nodes[f"node_{i+1}"]
        neighbors = {}
        
        # Connect to adjacent nodes (up, down, left, right)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            # Find the node at this position
            for j, (nx, ny) in enumerate(positions):
                if (nx, ny) == (new_x, new_y):
                    neighbor_hash = f"node_{j+1}"
                    # Calculate distance (1 for adjacent nodes)
                    distance = 1.0
                    neighbors[nodes[neighbor_hash]] = distance
                    break
        
        current_node.neighbours = neighbors
    
    # Add some special nodes
    # Entry point
    nodes["node_1"].type = "entry"
    # Exit point
    nodes["node_20"].type = "exit"
    # Storage areas
    nodes["node_6"].type = "storage"
    nodes["node_7"].type = "storage"
    nodes["node_8"].type = "storage"
    nodes["node_16"].type = "storage"
    nodes["node_17"].type = "storage"
    nodes["node_18"].type = "storage"
    
    return nodes

if __name__ == "__main__":
    # Example usage
    warehouse_map = create_example_map()
    print(f"Created warehouse map with {len(warehouse_map)} nodes")
    for node_hash, node in warehouse_map.items():
        print(f"{node_hash}: {node} (Type: {node.type}, Neighbors: {len(node.neighbours)})") 