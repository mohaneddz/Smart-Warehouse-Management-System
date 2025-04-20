# >>> IMPORTANT NOTE <<< 
# THIS IS AN EXAMPLE OF THE ALGORITHM IMPLEMENTATION.
# IT IS JUST AN EXAMPLE FOR HOW TO USE THE OTHER FILES IN THE BACKEND.

from typing import List, Optional
from core.node import Node
from math import inf

def a_star_algorithm(start: Node, goal: Node) -> Optional[List[Node]]:
    """Wrapper function for the A* search algorithm.
    
    Args:
        start: The starting node
        goal: The goal node
        
    Returns:
        Optional[List[Node]]: The path from start to goal if one exists, None otherwise
    """
    search = AStarSearch(start, goal)
    return search.search()

class AStarSearch:
    def __init__(self, start: Node, goal: Node):
        self.start = start
        self.goal = goal
        self.open_list = []
        self.closed_list = []
        self.came_from = {}
        self.g_scores = {start: 0}  # Store g-scores separately
        self.f_scores = {start: self._heuristic(start)}  # Store f-scores separately

    def search(self) -> Optional[List[Node]]:
        """ Perform the A* search algorithm. """
        self.open_list.append(self.start)
        while self.open_list:
            current_node = self._get_lowest_f_score_node()
            if current_node == self.goal:
                return self._reconstruct_path(current_node)

            self.open_list.remove(current_node)
            self.closed_list.append(current_node)

            for neighbor, cost in current_node.neighbours.items():
                if neighbor in self.closed_list:
                    continue
                tentative_g_score = self.g_scores[current_node] + cost
                if neighbor not in self.open_list:
                    self.open_list.append(neighbor)
                elif tentative_g_score >= self.g_scores.get(neighbor, inf):
                    continue

                self.came_from[neighbor] = current_node
                self.g_scores[neighbor] = int(tentative_g_score)
                self.f_scores[neighbor] = tentative_g_score + self._heuristic(neighbor)

        return None  # No path found

    def _get_lowest_f_score_node(self) -> Node:
        """ Get the node with the lowest f-score (g + h). """
        return min(self.open_list, key=lambda node: self.f_scores.get(node, inf))

    def _reconstruct_path(self, current_node: Node) -> List[Node]:
        """ Reconstruct the path from start to goal. """
        path = [current_node]
        while current_node in self.came_from:
            current_node = self.came_from[current_node]
            path.append(current_node)
        return path[::-1]  # Reverse to get the path from start to goal

    def _heuristic(self, node: Node) -> float:
        """ Calculate the heuristic value for a node. """
        return self.get_distance(node, self.goal)

    def get_distance(self, n1: Node, n2: Node) -> float:
        """ Calculate the Euclidean distance between two nodes. """
        return ((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2) ** 0.5
