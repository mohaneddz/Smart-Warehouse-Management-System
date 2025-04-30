from typing import Dict, Optional

class Node:
<<<<<<< HEAD
    """Represents a location in the warehouse layout with coordinates, neighbors, and associated value."""
    
    def __init__(self, x: float, y: float, neighbours: Dict['Node', float], value: float = 0.0):
        """Initializes a Node with coordinates, neighboring nodes, and an optional associated value.
=======
    """Represents a location in the warehouse layout with coordinates, neighbors, and value."""
    def __init__(self, x: float, y: float, hash: str, neighbours: Dict['Node', float], value: float = 0.0):
        """Initializes a Node with coordinates, neighbors, and an optional value.
>>>>>>> 44f3fed3189b8acefe8f743d628efdc4045e9242

        Args:
            x (float): X-coordinate of the node.
            y (float): Y-coordinate of the node.
            neighbours (Dict[Node, float]): Neighboring nodes and their distances.
            value (float, optional): Value associated with the node, defaults to 0.0.
        """
        self.x = x
        self.y = y
        self.neighbours = neighbours
        self.hash = hash
        self.heuristic = 0.0
        self.type = "normal"
        self.locked = False
        self.locked_by = None  # Reference to the agent that locked this node

    def lock(self, agent: 'Agent') -> bool:
        """Locks the node for a specific agent.

        Args:
            agent (Agent): The agent attempting to lock the node.

        Returns:
            bool: True if the node was successfully locked, False if it was already locked.
        """
        if not self.locked:
            self.locked = True
            self.locked_by = agent
            return True
        return False

    def unlock(self, agent: 'Agent') -> bool:
        """Unlocks the node if it was locked by the specified agent.

        Args:
            agent (Agent): The agent attempting to unlock the node.

        Returns:
            bool: True if the node was successfully unlocked, False if it was locked by a different agent.
        """
        if self.locked and self.locked_by == agent:
            self.locked = False
            self.locked_by = None
            return True
        return False

    def is_locked(self) -> bool:
        """Checks if the node is currently locked.

        Returns:
            bool: True if the node is locked, False otherwise.
        """
        return self.locked

    def get_locking_agent(self) -> Optional['Agent']:
        """Gets the agent that currently has the node locked.

        Returns:
            Optional[Agent]: The agent that locked the node, or None if the node is not locked.
        """
        return self.locked_by

    def set_heuristic(self, h: float):
        """Sets the heuristic value for this node.

        Args:
            h (float): The heuristic value to set.
        """
        self.heuristic = h

    def __eq__(self, other: object) -> bool:
        """Checks if two nodes are equal based on their coordinates.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the nodes are equal based on their coordinates, False otherwise.
        """
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y

    def __gt__(self, other: object) -> bool:
        """Compares nodes based on their value for priority queues.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the current node's value is greater than the other node's value.
        """
        if not isinstance(other, Node):
            return NotImplemented
        return self.value > other.value

    def __str__(self) -> str:
        """Returns a string representation of the node.

        Returns:
            str: A string representation of the node in the format "Node(x, y)".
        """
        return f"Node({self.x}, {self.y})"

    def __hash__(self) -> int:
        """Returns a hash based on the node's coordinates.

        Returns:
            int: A hash value computed from the node's coordinates.
        """
        return hash((self.x, self.y))
