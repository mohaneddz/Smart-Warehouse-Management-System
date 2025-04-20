# >>> IMPORTANT NOTE <<< 
# THIS IS AN EXAMPLE OF THE ALGORITHM IMPLEMENTATION.
# IT IS JUST AN EXAMPLE FOR HOW TO USE THE OTHER FILES IN THE BACKEND.

from typing import List, Optional
from core.node import Node
from math import inf

def greedy_algorithm(start: Node, goal: Node) -> Optional[List[Node]]:
    """Wrapper function for the Greedy Search algorithm.
    
    Args:
        start: The starting node
        goal: The goal node
        
    Returns:
        Optional[List[Node]]: The path from start to goal if one exists, None otherwise
    """
    search = GreedySearch(start, goal)
    return search.search()

class GreedySearch:
    def __init__(self, start: Node, goal: Node):
        self.start = start
        self.goal = goal
        self.visited = set()
        self.path = []

    def search(self) -> Optional[List[Node]]:
        """ Perform Greedy Search to find a path. """
        current = self.start
        self.visited.add(current)
        self.path.append(current)

        while current != self.goal:
            next_node = self._get_best_neighbor(current)
            if next_node is None:
                return None  # No path found
            current = next_node
            self.visited.add(current)
            self.path.append(current)

        return self.path

    def _get_best_neighbor(self, node: Node) -> Optional[Node]:
        """ Get the neighbor with the lowest heuristic value. """
        best_node = None
        best_heuristic = inf

        for neighbor in node.neighbours:
            if neighbor not in self.visited:
                heuristic = self._heuristic(neighbor)
                if heuristic < best_heuristic:
                    best_heuristic = heuristic
                    best_node = neighbor

        return best_node

    def _heuristic(self, node: Node) -> float:
        """ Calculate the heuristic value for a node. """
        return self.get_distance(node, self.goal)

    def get_distance(self, n1: Node, n2: Node) -> float:
        """ Calculate the Euclidean distance between two nodes. """
        return ((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2) ** 0.5
