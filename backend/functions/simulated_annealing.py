import json
import random
from typing import List, Optional
from core.node import Node

def simulated_annealing_algorithm(start: Node, goal: Node, temperature: float = 100, cooling_rate: float = 0.99) -> Optional[List[Node]]:
    """Wrapper function for the Simulated Annealing algorithm.
    
    Args:
        start: The starting node
        goal: The goal node
        temperature: Initial temperature
        cooling_rate: Rate at which temperature decreases
        
    Returns:
        Optional[List[Node]]: The best path found
    """
    search = SimulatedAnnealing(start, goal, temperature, cooling_rate)
    best_path = search.search()
    
    if best_path:
        # Update lookup table with best path
        update_lookup_table(best_path)
        
    return best_path


class SimulatedAnnealing:
    def __init__(self, start: Node, goal: Node, temperature: float = 100, cooling_rate: float = 0.99):
        self.start = start
        self.goal = goal
        self.temperature = temperature
        self.cooling_rate = cooling_rate
        self.best_path = []

    def search(self) -> Optional[List[Node]]:
        """ Perform the Simulated Annealing algorithm. """
        current_node = self.start
        while self.temperature > 1:
            neighbors = self._get_neighbors(current_node)
            next_node = self._choose_next_node(current_node, neighbors)

            if self._accept_move(current_node, next_node):
                current_node = next_node
                self.best_path.append(current_node)

            self.temperature *= self.cooling_rate  # Cool down

        return self.best_path

    def _get_neighbors(self, node: Node) -> List[Node]:
        """ Get the neighboring nodes. """
        return list(node.neighbours.keys())  # Return the actual neighbor nodes

    def _choose_next_node(self, current_node: Node, neighbors: List[Node]) -> Node:
        """ Choose the next node based on probability. """
        return random.choice(neighbors)

    def _accept_move(self, current_node: Node, next_node: Node) -> bool:
        """ Accept a move based on temperature and heuristic cost. """
        current_cost = self._calculate_cost(current_node)
        next_cost = self._calculate_cost(next_node)
        
        if next_cost < current_cost:
            return True
        
        # Calculate acceptance probability
        probability = 2.71828 ** ((current_cost - next_cost) / self.temperature)
        return random.random() < probability

    def _calculate_cost(self, node: Node) -> float:
        """ Calculate the cost of a node (distance to goal). """
        return ((node.x - self.goal.x) ** 2 + (node.y - self.goal.y) ** 2) ** 0.5

def update_lookup_table(best_path: List[Node]):
    """ Update the lookup table with the best path found from Simulated Annealing. """
    lookup_table_file = 'path_to_your_lookup_table.json'  # Change this to your actual lookup table path

    # Load the existing lookup table data
    try:
        with open(lookup_table_file, 'r') as file:
            lookup_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        lookup_data = {}

    # Assuming the path consists of node IDs or relevant information
    # You can customize this part depending on how you want to store the data
    path_ids = [node.id for node in best_path]  # Example: storing node IDs
    # Update lookup table with the best path (or any relevant info)
    for node in best_path:
        lookup_data[node.id] = {
            'goal_node': node.id,  # Example field, you can add more
            'path': path_ids
        }

    # Write the updated lookup table back to the file
    with open(lookup_table_file, 'w') as file:
        json.dump(lookup_data, file, indent=4)
