import json
import heapq
import math
import os
import matplotlib.pyplot as plt

# --- File Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_FILE_PATH = os.path.join(BASE_DIR, "..", "data", "map.json")
LOOKUP_TABLE_PATH = os.path.join(BASE_DIR, "..", "data", "lookup_table.json")

# --- Helper Functions ---
def load_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON from {file_path}: {e}")
        return None

def get_node_coordinates(node_id, graph_nodes):
    node = graph_nodes.get(node_id)
    return (node['x'], node['y']) if node else (None, None)

def heuristic_manhattan(n1, n2, nodes):
    x1, y1 = get_node_coordinates(n1, nodes)
    x2, y2 = get_node_coordinates(n2, nodes)
    return abs(x1 - x2) + abs(y1 - y2) if None not in (x1, y1, x2, y2) else float('inf')

def get_goal_node_from_lookup(item_id, table):
    return table.get(item_id, {}).get("goal_node")

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from and came_from[current]:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def greedy_search(start, goal, nodes, heuristic):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal, nodes), start))
    came_from = {start: None}
    explored = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in explored:
            continue
        explored.add(current)
        if current == goal:
            return reconstruct_path(came_from, current), explored

        for neighbor in nodes[current].get("neighbours", []):
            if neighbor not in explored and not nodes[neighbor].get("locked", False):
                came_from[neighbor] = current
                heapq.heappush(open_set, (heuristic(neighbor, goal, nodes), neighbor))

    return None, explored

def plot_statistics(path_ids, explored, warehouse_nodes, item_id):
    heuristics = [
        heuristic_manhattan(n, path_ids[-1], warehouse_nodes)
        for n in path_ids[:-1]
    ]
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))
    fig.suptitle(f"Greedy Search Haul Statistics for {item_id}")

    axs[0].bar(["Path Length", "Explored Nodes"], [len(path_ids), len(explored)], color=["blue", "orange"])
    axs[0].set_ylabel("Count")
    axs[0].set_title("Path and Explored Nodes")

    axs[1].plot(range(1, len(heuristics) + 1), heuristics, marker='o', color="green")
    axs[1].set_xlabel("Step in Path")
    axs[1].set_ylabel("Heuristic to Goal")
    axs[1].set_title("Heuristic Values Along Path")

    plt.tight_layout()
    plt.show()

# --- Main ---
def main():
    warehouse_map = load_json_file(MAP_FILE_PATH)
    lookup_table = load_json_file(LOOKUP_TABLE_PATH)
    if not warehouse_map or not lookup_table:
        print("Map or lookup table could not be loaded.")
        return

    nodes = warehouse_map["nodes"]
    agent_start_node = "N2-4"  # Start node for the agent, can be modified if needed

    # Iterate over all items in the lookup table
    for item_id, item_data in lookup_table.items():
        goal_node = get_goal_node_from_lookup(item_id, lookup_table)

        if not goal_node or goal_node not in nodes:
            print(f"Invalid goal node for item {item_id}. Skipping...")
            continue

        print(f"Searching from {agent_start_node} to {goal_node} for item {item_id}")
        path, explored = greedy_search(agent_start_node, goal_node, nodes, heuristic_manhattan)

        if path:
            print(f"Path found for {item_id}: {' -> '.join(path)}")
            plot_statistics(path, explored, nodes, item_id)
        else:
            print(f"No path found for {item_id}.")

if __name__ == "__main__":
    main()
