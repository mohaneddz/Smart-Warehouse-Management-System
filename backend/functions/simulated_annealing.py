import json
import random
import os
from typing import List, Optional
from core.node import Node

# --- File Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOOKUP_TABLE_PATH = os.path.join(BASE_DIR, "..", "data", "lookup_table.json")


def save_to_lookup_table(item_id, goal_node_id, rack, shelf, bin_range):
    lookup_data = {}
    if os.path.exists(LOOKUP_TABLE_PATH):
        with open(LOOKUP_TABLE_PATH, 'r') as f:
            try:
                lookup_data = json.load(f)
            except json.JSONDecodeError:
                print("Lookup table file exists but is not valid JSON.")

    lookup_data[item_id] = {
        "goal_node": goal_node_id,
        "rack": rack,
        "shelf": shelf,
        "bin_range": bin_range
    }

    with open(LOOKUP_TABLE_PATH, 'w') as f:
        json.dump(lookup_data, f, indent=2)


def simulated_annealing_algorithm(start: Node, goal: Node, item_id: str, temperature: float = 100, cooling_rate: float = 0.99) -> Optional[List[Node]]:
    search = SimulatedAnnealing(start, goal, temperature, cooling_rate)
    path = search.search()

    if path:
        # Example metadata generation (replace with real logic)
        rack = f"R{random.randint(1, 3)}"
        shelf = f"S{random.randint(1, 5)}"
        bin_range = f"B{random.randint(1, 3)}-B{random.randint(4, 6)}"
        save_to_lookup_table(item_id, goal.id, rack, shelf, bin_range)

    return path


class SimulatedAnnealing:
    def __init__(self, start: Node, goal: Node, temperature: float = 100, cooling_rate: float = 0.99):
        self.start = start
        self.goal = goal
        self.temperature = temperature
        self.cooling_rate = cooling_rate
        self.best_path = [start]

    def search(self) -> Optional[List[Node]]:
        current_node = self.start
        while self.temperature > 1:
            neighbors = self._get_neighbors(current_node)
            if not neighbors:
                break
            next_node = self._choose_next_node(current_node, neighbors)

            if self._accept_move(current_node, next_node):
                current_node = next_node
                self.best_path.append(current_node)

            self.temperature *= self.cooling_rate

        return self.best_path if current_node == self.goal else None

    def _get_neighbors(self, node: Node) -> List[Node]:
        return list(node.neighbours.keys())

    def _choose_next_node(self, current_node: Node, neighbors: List[Node]) -> Node:
        return random.choice(neighbors)

    def _accept_move(self, current_node: Node, next_node: Node) -> bool:
        current_cost = self._calculate_cost(current_node)
        next_cost = self._calculate_cost(next_node)

        if next_cost < current_cost:
            return True

        probability = 2.71828 ** ((current_cost - next_cost) / self.temperature)
        return random.random() < probability

    def _calculate_cost(self, node: Node) -> float:
        return ((node.x - self.goal.x) ** 2 + (node.y - self.goal.y) ** 2) ** 0.5
