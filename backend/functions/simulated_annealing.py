import json
import random
from typing import List, Optional
from core.node import Node

# Function to load JSON data
def load_json_file(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return {}

# Function to save updated data to JSON file
def save_json_file(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

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
    return search.search()

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


def update_lookup_table(task_id: str, goal_node_id: str, lookup_table_path: str):
    """ Updates the lookup table with the task ID and its goal node. """
    lookup_table_data = load_json_file(lookup_table_path)
    
    if task_id in lookup_table_data:
        print(f"Warning: Task ID '{task_id}' already exists in the lookup table. Updating goal node.")
    
    lookup_table_data[task_id] = {"goal_node": goal_node_id}
    
    save_json_file(lookup_table_path, lookup_table_data)
    print(f"Updated lookup table with task '{task_id}' and goal node '{goal_node_id}'.")

# Example of using the algorithm and updating the lookup table
def main():
    # Load or define your start and goal nodes here
    start_node = Node("N2-4", x=468, y=203)  # Example start node
    goal_node = Node("N2-5", x=488, y=203)   # Example goal node

    # Run Simulated Annealing to find the best path
    path = simulated_annealing_algorithm(start_node, goal_node)
    if path:
        print(f"Simulated Annealing path found: {[node.id for node in path]}")
        # After finding the goal node for a task, update the lookup table
        task_id = "task_001"  # Example task ID
        update_lookup_table(task_id, goal_node.id, "lookup_table.json")
    else:
        print("No path found.")
        

if __name__ == "__main__":
    main()
