from typing import Dict, Optional

class Node:
    """Represents a location in the warehouse layout with coordinates, neighbors, and value."""
    def __init__(self, x: float, y: float, hash: str, neighbours: Dict['Node', float], value: float = 0.0):
        """Initializes a Node with coordinates, neighbors, and an optional value.

        Args:
            x (float): X-coordinate of the node.
            y (float): Y-coordinate of the node.
            neighbours (Dict[Node, float]): Neighboring nodes and their distances.
            value (float, optional): Value associated with the node. Defaults to 0.0.
        """
        self.x = x
        self.y = y
        self.neighbours = neighbours
        self.hash = hash
        self.heuristic = 0.0
        self.type = "normal"

    def set_heuristic(self, h: float):
        """Set the heuristic value for this node.

        Args:
            h (float): The heuristic value to set.
        """
        self.heuristic = h

    def __eq__(self, other):
        """Check if two nodes are equal based on their coordinates."""
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y

    def __gt__(self, other):
        """Compare nodes based on their value for priority queues."""
        if not isinstance(other, Node):
            return NotImplemented
        return self.value > other.value

    def __str__(self):
        """Return a string representation of the node."""
        return f"Node({self.x}, {self.y})"

    def __hash__(self):
        """Return a hash based on the node's coordinates."""
        return hash((self.x, self.y))