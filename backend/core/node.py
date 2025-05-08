from typing import Dict, Optional, List
from enum import Enum, auto
from core.types import NodeType, INode, IAgent
from dataclasses import dataclass, field

@dataclass
class Node:
    """Represents a node in the warehouse grid.
    
    Attributes:
        x (int): X coordinate
        y (int): Y coordinate
        node_type (NodeType): Type of the node
        name (str): Name of the node (e.g., "A1", "B2")
        neighbours (Dict[Node, float]): Dictionary of neighboring nodes and their distances
        locked_by (Optional[str]): ID of the agent that has locked this node
    """
    x: int
    y: int
    node_type: NodeType
    name: str
    neighbours: Dict['Node', float] = field(default_factory=dict)
    locked_by: Optional[str] = None
    locked: bool = False
    is_goal: bool = False

    def add_neighbor(self, node: 'Node', distance: float = 1.0) -> None:
        """Adds a neighboring node with the given distance."""
        self.neighbours[node] = distance
        node.neighbours[self] = distance

    def is_locked(self) -> bool:
        """Returns whether the node is currently locked by an agent."""
        return self.locked

    def lock(self, agent_id: str) -> bool:
        """Attempts to lock the node for an agent.
        
        Args:
            agent_id (str): ID of the agent attempting to lock the node
            
        Returns:
            bool: True if the node was successfully locked, False otherwise
        """
        if not self.is_locked():
            self.locked = True
            self.locked_by = agent_id
            return True
        return False

    def unlock(self, agent_id: str) -> bool:
        """Attempts to unlock the node for an agent.
        
        Args:
            agent_id (str): ID of the agent attempting to unlock the node
            
        Returns:
            bool: True if the node was successfully unlocked, False otherwise
        """
        if self.locked and self.locked_by == agent_id:
            self.locked = False
            self.locked_by = None
            return True
        return False

    def __hash__(self) -> int:
        """Returns a hash value for the node."""
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        """Checks if two nodes are equal."""
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        """Returns a string representation of the node."""
        return f"{self.name} ({self.x}, {self.y})"

    def get_locking_agent(self) -> Optional[str]:
        """Gets the agent that currently has the node locked.

        Returns:
            Optional[str]: The agent that locked the node, or None if the node is not locked
        """
        return self.locked_by

    def set_type(self, node_type: NodeType) -> None:
        """Sets the type of the node.

        Args:
            node_type (NodeType): The new type for the node
        """
        self.node_type = node_type

    def set_goal(self, is_goal: bool = True) -> None:
        """Sets whether this node is a goal node.

        Args:
            is_goal (bool, optional): Whether this is a goal node. Defaults to True.
        """
        self.is_goal = is_goal
