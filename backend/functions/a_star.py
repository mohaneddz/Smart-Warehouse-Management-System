import json
import csv
import heapq
import math

# Load warehouse map
try:
    with open("../data/map.json") as f:
        map_data = json.load(f)
except FileNotFoundError:
    print("Error: map.json not found in ../data/ directory.")
    exit()
except json.JSONDecodeError:
    print("Error: Invalid JSON format in map.json.")
    exit()

nodes = map_data["nodes"]

# Ensure all nodes have required keys
for node in nodes.values():
    node.setdefault("locked", False)
    node.setdefault("heuristic", 0)
    node.setdefault("is_goal", False)

# Location lookup table
lookup_table = {
    "A1L": ["N3-21", "N4-21", "N5-21", "N6-21", "N7-21"],
    "A1R": ["N3-20", "N4-20", "N5-20", "N6-20", "N7-20"],
    "A2L": ["N8-21", "N9-21", "N10-21", "N11-21", "N12-21"],
    "A2R": ["N8-20", "N9-20", "N10-20", "N11-20", "N12-20"],
    "A3L": ["N13-21", "N14-21", "N15-21", "N16-21", "N17-21"],
    "A3R": ["N13-20", "N14-20", "N15-20", "N16-20", "N17-20"],
    "B1L": ["C1-2", "C2-2", "C3-2", "C4-2", "C5-2"],
    "B1R": ["C1-1", "C2-1", "C3-1", "C4-1", "C5-1"],
    "B2L": ["C6-2", "C7-2", "C8-2", "C9-2", "C10-2"],
    "B2R": ["C6-1", "C7-1", "C8-1", "C9-1", "C10-1"],
    "B3L": ["C11-2", "C12-2", "C13-2", "C14-2", "C15-2"],
    "B3R": ["C11-1", "C12-1", "C13-1", "C14-1", "C15-1"],
    "C1L": ["C1-6", "C2-6", "C3-6", "C4-6", "C5-6"],
    "C1R": ["C1-5", "C2-5", "C3-5", "C4-5", "C5-5"],
    "C2L": ["C6-6", "C7-6", "C8-6", "C9-6", "C10-6"],
    "C2R": ["C6-5", "C7-5", "C8-5", "C9-5", "C10-5"],
    "C3L": ["C11-6", "C12-6", "C13-6", "C14-6", "C15-6"],
    "C3R": ["C11-5", "C12-5", "C13-5", "C14-5", "C15-5"],
    "D1L": ["C1-10", "C2-10", "C3-10", "C4-10", "C5-10"],
    "D1R": ["C1-9", "C2-9", "C3-9", "C4-9", "C5-9"],
    "D2L": ["C6-10", "C7-10", "C8-10", "C9-10", "C10-10"],
    "D2R": ["C6-9", "C7-9", "C8-9", "C9-9", "C10-9"],
    "D3L": ["C11-10", "C12-10", "C13-10", "C14-10", "C15-10"],
    "D3R": ["C11-9", "C12-9", "C13-9", "C14-9", "C15-9"],
}

def heuristic(node_a, node_b):
    if node_a not in nodes or node_b not in nodes:
        return float("inf")
    ax, ay = nodes[node_a]["x"], nodes[node_a]["y"]
    bx, by = nodes[node_b]["x"], nodes[node_b]["y"]
    # Using Manhattan distance which is generally better for grid-based movement
    return abs(ax - bx) + abs(ay - by)

def a_star_search(start, goal):
    if start not in nodes or goal not in nodes:
        print(f"Error: Start node '{start}' or goal node '{goal}' not found in the map.")
        return []

    open_set = [(heuristic(start, goal), 0, start, [start])]  # (f_score, g_score, current_node, path)
    g_costs = {start: 0}
    visited = set()

    while open_set:
        f, g, current, path = heapq.heappop(open_set)

        if current == goal:
            return path

        if current in visited:
            continue
        visited.add(current)

        for neighbor in nodes[current].get("neighbours", []):
            if neighbor not in nodes or nodes[neighbor].get("locked"):
                continue

            tentative_g = g + 1  # Assuming uniform cost of 1 for each step
            if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor, path + [neighbor]))

    return []  # Return an empty list if no path is found

def bin_range_to_indices(bin_range):
    try:
        start, end = map(int, bin_range.split("-"))
        return list(range(start, end + 1))
    except ValueError:
        return []

def get_goal_node(position_string):
    try:
        cleaned = position_string.strip("() ").replace("\"", "")
        rack, shelf_str, bin_range = map(str.strip, cleaned.split(","))
        try:
            shelf = int(shelf_str)
        except ValueError:
            print(f"❌ Invalid shelf level format: {shelf_str}")
            return None
        bin_indices = bin_range_to_indices(bin_range)
        if rack not in lookup_table:
            print(f"❌ Invalid rack: {rack}")
            return None
        if not (1 <= shelf <= 3):
            print(f"❌ Invalid shelf level: {shelf}")
            return None
        if not bin_indices:
            print(f"❌ Invalid bin range: {bin_range}")
            return None

        node_list = lookup_table[rack]
        # Calculate the target index in the node list based on the shelf and average bin index
        # Assuming the nodes in lookup_table are ordered corresponding to the bins
        num_bins_per_shelf = 5  # Based on the lookup table structure
        shelf_offset = (shelf - 1) * num_bins_per_shelf
        avg_bin_index_relative = sum(bin_indices) / len(bin_indices) - 1 # 0-based index
        index = min(int(round(avg_bin_index_relative)), len(node_list) - 1)
        return node_list[index]
    except Exception as e:
        print(f"⚠️ Failed to parse {position_string}: {e}")
        return None

# Run A* for each item movement
try:
    with open("./item_movements.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_id = row["item_id"]
            new_position = row["new_position"]
            category = row.get("category", "").strip().lower()

            start_node = "E1-1" if category == "frozen" else "E1-2"
            goal_node = get_goal_node(new_position)

            if goal_node:
                print(f"\n🚚 Moving item {item_id} to {new_position} → goal node: {goal_node}")
                path = a_star_search(start_node, goal_node)
                if path:
                    print(f"✅ A* Path: {' → '.join(path)}")
                else:
                    print(f"❌ No path found from {start_node} to {goal_node}")
            else:
                print(f"⚠️ Skipped item {item_id} due to invalid position: {new_position}")
except FileNotFoundError:
    print("Error: item_movements.csv not found in the current directory.")
except Exception as e:
    print(f"An error occurred while processing item movements: {e}")