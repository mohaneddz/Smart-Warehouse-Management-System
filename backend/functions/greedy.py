import json
import csv
from ast import literal_eval
from core.node import Node
from collections import deque

# Load the warehouse map
with open("backend/functions/map.json") as f:
    warehouse_map = json.load(f)

# Load the heuristic lookup table
with open("backend/functions/lookup_table.json") as f:
    heuristic_lookup = json.load(f)

def parse_position(pos_str):
    """Convert position string '(rack,shelf,b1-b2)' into a tuple"""
    rack, shelf, bin_range = literal_eval(pos_str)
    return (rack, shelf, bin_range)

def get_neighbors(pos):
    """Return neighbors of a given position if defined in the map."""
    return warehouse_map.get(str(pos), [])

def greedy_search(start, goal):
    """Greedy Search using heuristics from lookup_table.json"""
    start_node = Node(start)
    frontier = deque([start_node])
    explored = set()

    while frontier:
        current_node = frontier.popleft()
        current_pos = current_node.state

        if current_pos == goal:
            return current_node.path()

        explored.add(current_pos)

        for neighbor in get_neighbors(current_pos):
            neighbor_tuple = tuple(neighbor)
            if neighbor_tuple not in explored:
                h_value = heuristic_lookup.get(str(neighbor_tuple), 0)
                neighbor_node = Node(neighbor_tuple, parent=current_node, cost=h_value)
                frontier.append(neighbor_node)

        frontier = deque(sorted(frontier, key=lambda node: node.cost))

    return None

def run_from_csv():
    with open("backend/functions/item_movements.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_id = row["item_id"]
            start = parse_position(row["initial_position"])
            goal = parse_position(row["new_position"])
            path = greedy_search(start, goal)
            print(f"Item {item_id}: path from {start} to {goal} -> {path}")

if __name__ == "__main__":
    run_from_csv()
