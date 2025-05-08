import json
import csv
import heapq

# Load warehouse map
with open("../data/map.json") as f:
    map_data = json.load(f)

nodes = map_data["nodes"]

# Ensure all nodes have required keys
for node in nodes.values():
    node.setdefault("locked", False)
    node.setdefault("heuristic", 0)
    node.setdefault("is_goal", False)

# Define the lookup table for rack and shelf positions
lookup_table = {
    # ... include your full lookup_table here exactly as you've built it ...
}

# Heuristic function (Euclidean distance)
def heuristic(node_a, node_b):
    if node_a not in nodes or node_b not in nodes:
        return float("inf")
    ax, ay = nodes[node_a]["x"], nodes[node_a]["y"]
    bx, by = nodes[node_b]["x"], nodes[node_b]["y"]
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5

# Greedy search
def greedy_search(start, goal):
    visited = set()
    queue = [(heuristic(start, goal), start, [start])]
    while queue:
        _, current, path = heapq.heappop(queue)
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for neighbor in nodes[current]["neighbours"]:
            if neighbor not in visited and not nodes.get(neighbor, {}).get("locked", False):
                heapq.heappush(queue, (heuristic(neighbor, goal), neighbor, path + [neighbor]))
    return []

# Parse bin range like "3-5"
def bin_range_to_indices(bin_range):
    try:
        start, end = map(int, bin_range.split("-"))
        return list(range(start, end + 1))
    except ValueError:
        return []

# Extract the goal node from position string like "(A1L,1,3-5)"
def get_goal_node(new_position):
    try:
        cleaned = new_position.strip("() ").replace("\"", "")
        rack, shelf, bin_range = [part.strip() for part in cleaned.split(",")]
        key = rack  # Already like "A1L"
        shelf = int(shelf)
        bin_indices = bin_range_to_indices(bin_range)
        if key not in lookup_table:
            print(f"❌ Invalid rack key: {key}")
            return None
        if not (1 <= shelf <= 3):
            print(f"❌ Invalid shelf level: {shelf}")
            return None
        return lookup_table[key][shelf - 1]
    except Exception as e:
        print(f"⚠️ Failed to parse {new_position}: {e}")
        return None

# Main execution
start_node = "E1-1"
with open("./item_movements.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        item_id = row["item_id"]
        new_position = row["new_position"]
        goal_node = get_goal_node(new_position)

        if goal_node:
            print(f"🚚 Navigating to item {item_id} (Goal: {goal_node})")
            path = greedy_search(start_node, goal_node)
            if path:
                print(f"✔️ Path to {item_id}: {' -> '.join(path)}")
                start_node = "E1-1"  # Always return to initial node
            else:
                print(f"❌ No path found to item {item_id}")
