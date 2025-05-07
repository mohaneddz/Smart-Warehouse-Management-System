#
from typing import List, Optional
from core.node import Node  # Assuming you have a Node class with x, y, neighbours, locked, etc.
from math import inf

def a_star_algorithm(start: Node, goal: Node) -> Optional[List[Node]]:
    """Wrapper function for the A* search algorithm.
    
    Args:
        start: The starting node.
        goal: The goal node.
        
    Returns:
        A list of nodes representing the shortest path from start to goal if found, None otherwise.
    """
    search = AStarSearch(start, goal)
    return search.search()


class AStarSearch:
    def __init__(self, start: Node, goal: Node):
        self.start = start
        self.goal = goal
        self.open_list = [start]
        self.closed_list = []
        self.came_from = {}

        self.g_scores = {start: 0}
        self.f_scores = {start: self._heuristic(start)}

    def search(self) -> Optional[List[Node]]:
        while self.open_list:
            current_node = self._get_lowest_f_score_node()

            if current_node == self.goal:
                return self._reconstruct_path(current_node)

            self.open_list.remove(current_node)
            self.closed_list.append(current_node)

            for neighbor, cost in current_node.neighbours.items():
                if neighbor.locked or neighbor in self.closed_list:
                    continue

                tentative_g = self.g_scores[current_node] + cost

                if neighbor not in self.open_list:
                    self.open_list.append(neighbor)
                elif tentative_g >= self.g_scores.get(neighbor, inf):
                    continue

                # This path is the best so far
                self.came_from[neighbor] = current_node
                self.g_scores[neighbor] = tentative_g # type: ignore
                self.f_scores[neighbor] = tentative_g + self._heuristic(neighbor)

        return None  # No path found

    def _get_lowest_f_score_node(self) -> Node:
        return min(self.open_list, key=lambda node: self.f_scores.get(node, inf))

    def _reconstruct_path(self, current_node: Node) -> List[Node]:
        path = [current_node]
        while current_node in self.came_from:
            current_node = self.came_from[current_node]
            path.append(current_node)
        return path[::-1]

    def _heuristic(self, node: Node) -> float:
        return self.get_distance(node, self.goal)

    def get_distance(self, n1: Node, n2: Node) -> float:
        return ((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2) ** 0.5
