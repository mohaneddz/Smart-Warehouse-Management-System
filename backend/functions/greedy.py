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

# Lookup table
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

# Heuristic: Euclidean distance
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
        for neighbor in nodes[current].get("neighbours", []):
            if neighbor not in visited and not nodes.get(neighbor, {}).get("locked", False):
                heapq.heappush(queue, (heuristic(neighbor, goal), neighbor, path + [neighbor]))
    return []

# Convert "3-5" to [3, 4, 5]
def bin_range_to_indices(bin_range):
    try:
        start, end = map(int, bin_range.split("-"))
        return list(range(start, end + 1))
    except ValueError:
        return []

# Get goal node from lookup_table using bin index
def get_goal_node(new_position):
    try:
        cleaned = new_position.strip("() ").replace("\"", "")
        rack, shelf_str, bin_range = [part.strip() for part in cleaned.split(",")]
        shelf = int(shelf_str)
        bin_indices = bin_range_to_indices(bin_range)

        if rack not in lookup_table:
            print(f"❌ Invalid rack: {rack}")
            return None
        if not (1 <= shelf <= 3):
            print(f"❌ Invalid shelf level: {shelf}")
            return None

        # Use middle bin index (average) to decide which node represents that bin
        if not bin_indices:
            return None
        avg_bin_index = sum(bin_indices) // len(bin_indices)

        # Determine which of the 5 nodes maps to this bin (assumes ~5 bins per node)
        node_list = lookup_table[rack]
        index = min(avg_bin_index // 2, len(node_list) - 1)  # bin 0–1 = node 0, 2–3 = node 1, ...
        return node_list[index]
    except Exception as e:
        print(f"⚠️ Failed to parse {new_position}: {e}")
        return None

# Main
start_node = "E1-2"
with open("./item_movements.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        item_id = row["item_id"]
        new_position = row["new_position"]
        goal_node = get_goal_node(new_position)

        if goal_node:
            print(f"\n🚚 Moving item {item_id} to {new_position} → goal node: {goal_node}")
            path = greedy_search(start_node, goal_node)
            if path:
                print(f"✅ Path: {' → '.join(path)}")
            else:
                print(f"❌ No path found to {goal_node}")
        else:
            print(f"⚠️ Skipped item {item_id} due to invalid position.")
