import json
import heapq
import math
import os

# --- File Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_FILE_PATH = os.path.join(BASE_DIR, ":.", "data", "map.json")

LOOKUP_TABLE_PATH = os.path.join(BASE_DIR,"..", "data", "lookup_table.json")

# --- Helper Functions ---
def load_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return None

def get_node_coordinates(node_id, graph_nodes):
    node_data = graph_nodes.get(node_id)
    if node_data and 'x' in node_data and 'y' in node_data:
        return node_data['x'], node_data['y']
    print(f"Warning: Coordinates not found for node_id '{node_id}'.")
    return None, None

def heuristic_euclidean(node_id_current, node_id_goal, graph_nodes):
    x_curr, y_curr = get_node_coordinates(node_id_current, graph_nodes)
    x_goal, y_goal = get_node_coordinates(node_id_goal, graph_nodes)
    if x_curr is None or y_curr is None or x_goal is None or y_goal is None:
        return float('inf')
    return math.sqrt((x_curr - x_goal)**2 + (y_curr - y_goal)**2)

def heuristic_manhattan(node_id_current, node_id_goal, graph_nodes):
    x_curr, y_curr = get_node_coordinates(node_id_current, graph_nodes)
    x_goal, y_goal = get_node_coordinates(node_id_goal, graph_nodes)
    if x_curr is None or y_curr is None or x_goal is None or y_goal is None:
        return float('inf')
    return abs(x_curr - x_goal) + abs(y_curr - y_goal)

def get_goal_node_from_lookup(item_or_task_id, lookup_table_content):
    if not lookup_table_content:
        print("Warning: Lookup table content is empty or not loaded.")
        return None
    item_data = lookup_table_content.get(item_or_task_id)
    if item_data and "goal_node" in item_data:
        return item_data["goal_node"]
    print(f"Warning: Item or task ID '{item_or_task_id}' not found or missing 'goal_node' in lookup table.")
    return None

def reconstruct_path(came_from, current_node_id):
    path = [current_node_id]
    while current_node_id in came_from and came_from[current_node_id] is not None:
        current_node_id = came_from[current_node_id]
        path.append(current_node_id)
    return path[::-1]

def greedy_search(start_node_id, goal_node_id, graph_nodes, heuristic_function):
    if start_node_id not in graph_nodes:
        print(f"Error: Start node ID '{start_node_id}' not found in the graph.")
        return None
    if goal_node_id not in graph_nodes:
        print(f"Error: Goal node ID '{goal_node_id}' not found in the graph.")
        return None
    if start_node_id == goal_node_id:
        return [start_node_id]

    open_set_pq = []
    h_start = heuristic_function(start_node_id, goal_node_id, graph_nodes)
    heapq.heappush(open_set_pq, (h_start, start_node_id))
    came_from = {start_node_id: None}
    explored_nodes = set()

    while open_set_pq:
        _, current_node_id = heapq.heappop(open_set_pq)
        if current_node_id in explored_nodes:
            continue
        explored_nodes.add(current_node_id)
        if current_node_id == goal_node_id:
            return reconstruct_path(came_from, current_node_id)

        current_node_data = graph_nodes.get(current_node_id)
        if not current_node_data:
            continue

        for neighbor_id in current_node_data.get("neighbours", []):
            if neighbor_id not in graph_nodes:
                continue
            neighbor_node_data = graph_nodes[neighbor_id]
            if neighbor_node_data.get("locked", False):
                continue
            if neighbor_id in explored_nodes:
                 continue
            if neighbor_id not in came_from:
                came_from[neighbor_id] = current_node_id
                h_value = heuristic_function(neighbor_id, goal_node_id, graph_nodes)
                heapq.heappush(open_set_pq, (h_value, neighbor_id))
    print(f"No path found from '{start_node_id}' to '{goal_node_id}'.")
    return None

def main()
    map_data = load_json_file(MAP_FILE_PATH)
    if not map_data or "nodes" not in map_data:
        print(f"Critical: Failed to load or parse map data from '{MAP_FILE_PATH}'. Exiting.")
        return
    warehouse_nodes = map_data["nodes"]

    lookup_table_content = load_json_file(LOOKUP_TABLE_PATH)
    if not lookup_table_content:
        print(f"Critical: Failed to load lookup table from '{LOOKUP_TABLE_PATH}'. Exiting.")
        return

    agent_start_node = "N2-4"  # Example start node
    item_ids_in_lookup = list(lookup_table_content.keys())
    if not item_ids_in_lookup:
        print("Lookup table is empty. No item to process.")
        return

    item_id_to_process = item_ids_in_lookup[0]
    print(f"\n--- Agent Task ---")
    print(f"Agent current location: {agent_start_node}")
    print(f"Processing item/task: {item_id_to_process}")

    goal_node_id = get_goal_node_from_lookup(item_id_to_process, lookup_table_content)
    if not goal_node_id or goal_node_id not in warehouse_nodes:
        print(f"Error: Invalid or missing goal node '{goal_node_id}' for item '{item_id_to_process}'.")
        return
    print(f"Target goal node for '{item_id_to_process}': {goal_node_id}")

    selected_heuristic = heuristic_manhattan  # Choose heuristic (Manhattan or Euclidean)
    print(f"Using heuristic: {selected_heuristic.__name__}")
    path_ids = greedy_search(agent_start_node, goal_node_id, warehouse_nodes, selected_heuristic)

    if path_ids:
        print(f"\nPath found from '{agent_start_node}' to '{goal_node_id}':")
        print(f"Path as node IDs: {' -> '.join(path_ids)}")
        print("\nFull node data for the path:")
        for node_id in path_ids:
            if node_id in warehouse_nodes:
                print(json.dumps(warehouse_nodes[node_id], indent=2))
            else:
                print(f"Error: Node ID '{node_id}' from path not found in warehouse_nodes.")
    else:
        print(f"\nNo path found from '{agent_start_node}' to '{goal_node_id}'.")

if __name__ == "__main__":
    main()
