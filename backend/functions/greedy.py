import json
import heapq
import os
import matplotlib.pyplot as plt
import random

# --- INSTRUCTIONS ---
# 1. Save your large JSON data into a file named 'map.json'.
# 2. Place 'map.json' in the SAME DIRECTORY as this Python script.
# 3. Make sure you have matplotlib installed: pip install matplotlib
# 4. Run this script from your terminal: python visualize_map.py

def load_json_data(path):
    """Loads JSON data from the given file path."""
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{path}'. Make sure it's in the same directory as the script.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{path}'. Check the file for syntax errors.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading JSON file: {e}")
        return None

def get_node_coordinates(node_id, nodes_data):
    """Safely retrieves x and y coordinates for a given node_id."""
    node_info = nodes_data.get(node_id)
    if node_info:
        return node_info.get("x"), node_info.get("y")
    return None, None

def manhattan_distance_heuristic(node1_id, node2_id, nodes_data):
    """Calculates Manhattan distance between two nodes."""
    x1, y1 = get_node_coordinates(node1_id, nodes_data)
    x2, y2 = get_node_coordinates(node2_id, nodes_data)
    if None in [x1, y1, x2, y2]:
        # print(f"Warning: Coordinates missing for {node1_id} or {node2_id} for heuristic.")
        return float('inf')  # Cannot calculate heuristic
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current_node_id):
    """Reconstructs the path from the start node to the current_node_id."""
    path = [current_node_id]
    while current_node_id in came_from and came_from[current_node_id] is not None:
        current_node_id = came_from[current_node_id]
        path.append(current_node_id)
    return path[::-1]  # Return reversed path

def greedy_best_first_search(start_node_id, goal_node_id, nodes_data, heuristic_function):
    """
    Performs Greedy Best-First Search.
    Returns the path and the set of explored nodes.
    """
    if start_node_id not in nodes_data or goal_node_id not in nodes_data:
        print("Error: Start or goal node ID not found in nodes_data.")
        return None, set()

    # Priority queue stores (heuristic_value, entry_count, node_id)
    # entry_count is a tie-breaker for nodes with the same heuristic
    open_list_pq = []
    entry_count = 0
    heapq.heappush(open_list_pq, (heuristic_function(start_node_id, goal_node_id, nodes_data), entry_count, start_node_id))
    entry_count += 1

    came_from = {start_node_id: None}
    # 'explored_nodes' will store all nodes ever pushed to open_list and processed,
    # or simply all nodes whose neighbors have been examined.
    explored_nodes = set()


    while open_list_pq:
        _, _, current_node_id = heapq.heappop(open_list_pq)

        if current_node_id in explored_nodes: # Already processed this node
            continue
        explored_nodes.add(current_node_id)

        if current_node_id == goal_node_id:
            return reconstruct_path(came_from, current_node_id), explored_nodes

        current_node_info = nodes_data.get(current_node_id, {})
        neighbors = current_node_info.get("neighbours", [])

        for neighbor_id in neighbors:
            if neighbor_id not in nodes_data:
                # print(f"Warning: Neighbor '{neighbor_id}' of '{current_node_id}' not found in nodes_data. Skipping.")
                continue

            neighbor_info = nodes_data[neighbor_id]
            if neighbor_info.get("locked", False):
                continue # Skip locked nodes

            if neighbor_id not in explored_nodes and neighbor_id not in came_from: # Process only if not explored and no path yet
                came_from[neighbor_id] = current_node_id
                priority = heuristic_function(neighbor_id, goal_node_id, nodes_data)
                heapq.heappush(open_list_pq, (priority, entry_count, neighbor_id))
                entry_count += 1
                # Add to explored when considering adding to open_list for visualization completeness
                # but it's more accurate to say a node is "explored" when popped and its neighbors are checked.
                # For visualization, we'll consider `explored_nodes` as those popped.

    return None, explored_nodes # No path found

def draw_warehouse_path(nodes_data, racks_data, start_node_id, goal_node_id, path, explored_nodes=None, title="Warehouse Path"):
    """Draws the map, racks, and the path."""
    if not nodes_data:
        print("No node data provided for drawing.")
        return

    plt.figure(figsize=(15, 10)) # Adjust figure size as needed

    # 1. Draw all nodes
    all_node_x = []
    all_node_y = []
    for node_id, info in nodes_data.items():
        x, y = get_node_coordinates(node_id, nodes_data)
        if x is not None and y is not None:
            all_node_x.append(x)
            all_node_y.append(y)
    plt.scatter(all_node_x, all_node_y, color='lightgray', s=20, label="All Nodes", zorder=1)

    # Optional: Draw connections between all nodes (can be very messy for large graphs)
    # for node_id, info in nodes_data.items():
    #     x1, y1 = get_node_coordinates(node_id, nodes_data)
    #     if x1 is not None and y1 is not None:
    #         for neighbor_id in info.get("neighbours", []):
    #             if neighbor_id in nodes_data:
    #                 x2, y2 = get_node_coordinates(neighbor_id, nodes_data)
    #                 if x2 is not None and y2 is not None:
    #                     plt.plot([x1, x2], [y1, y2], color='whitesmoke', linewidth=0.5, zorder=0)


    # 2. Draw explored nodes (if provided)
    if explored_nodes:
        explored_x = []
        explored_y = []
        for node_id in explored_nodes:
            x, y = get_node_coordinates(node_id, nodes_data)
            if x is not None and y is not None:
                explored_x.append(x)
                explored_y.append(y)
        plt.scatter(explored_x, explored_y, color='skyblue', s=30, label="Explored Nodes", zorder=2)

    # 3. Draw Start and Goal nodes
    sx, sy = get_node_coordinates(start_node_id, nodes_data)
    gx, gy = get_node_coordinates(goal_node_id, nodes_data)

    if sx is not None and sy is not None:
        plt.scatter(sx, sy, color='green', s=150, label="Start", edgecolors='black', marker='P', zorder=4)
    if gx is not None and gy is not None:
        plt.scatter(gx, gy, color='purple', s=150, label="Goal", edgecolors='black', marker='*', zorder=4)

    # 4. Draw the path (if found)
    if path:
        path_x = []
        path_y = []
        for node_id in path:
            x, y = get_node_coordinates(node_id, nodes_data)
            if x is not None and y is not None:
                path_x.append(x)
                path_y.append(y)
        plt.plot(path_x, path_y, color='red', linewidth=2.5, label="Agent Path", zorder=3)
        plt.scatter(path_x, path_y, color='orange', s=40, zorder=3) # Highlight nodes on path
    else:
        print("No path found to draw.")

    # 5. Draw Racks (as simple rectangles for now)
    if racks_data:
        for rack_id, rack_info in racks_data.items():
            # Using start_cords and end_cords to define a rectangle
            # This assumes racks are axis-aligned and defined by two opposite corners
            # If center_cords represents the center and you have width/height, that's another way.
            # For now, assuming start_cords is top-left and end_cords is bottom-right for visualization
            sc = rack_info.get("start_cords")
            ec = rack_info.get("end_cords")
            cc = rack_info.get("center_cords") # Could be used for label or center point

            if sc and ec:
                # Assuming sc = [x1, y1] and ec = [x2, y2]
                # For horizontal racks: y1=y2, x1 is start, x2 is end. height is arbitrary.
                # For vertical racks: x1=x2, y1 is start, y2 is end. width is arbitrary.

                # Simple visualization: plot start, center, and end points of racks
                # plt.scatter(sc[0], sc[1], color='black', marker='s', s=30, zorder=0)
                # if cc: plt.scatter(cc[0], cc[1], color='dimgray', marker='x', s=30, zorder=0)
                # plt.scatter(ec[0], ec[1], color='black', marker='s', s=30, zorder=0)

                # Or draw as lines/rectangles (more complex, depends on rack orientation)
                # Example: if vertical rack, width is small, height is ec[1]-sc[1]
                if sc[0] == ec[0]: # Vertical rack
                    rack_width = 10 # Arbitrary width for visualization
                    rect = plt.Rectangle((sc[0] - rack_width/2, sc[1]), rack_width, ec[1]-sc[1],
                                         linewidth=1, edgecolor='gray', facecolor='lightgoldenrodyellow', alpha=0.7, zorder=0)
                    plt.gca().add_patch(rect)
                # Example: if horizontal rack, height is small, width is ec[0]-sc[0]
                elif sc[1] == ec[1]: # Horizontal rack
                    rack_height = 10 # Arbitrary height for visualization
                    rect = plt.Rectangle((sc[0], sc[1] - rack_height/2), ec[0]-sc[0], rack_height,
                                         linewidth=1, edgecolor='gray', facecolor='lightgoldenrodyellow', alpha=0.7, zorder=0)
                    plt.gca().add_patch(rect)
                # If you want to label racks:
                # if cc:
                #     plt.text(cc[0], cc[1], rack_id, fontsize=7, color='black', ha='center', va='center', zorder=0)


    plt.title(title)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1)) # Legend outside plot
    plt.grid(True, linestyle=':', alpha=0.6)

    # --- IMPORTANT FOR VISUALIZATION MATCHING ---
    plt.gca().invert_yaxis()  # Invert Y-axis: (0,0) top-left, Y increases downwards
    plt.axis('equal')         # Enforce equal aspect ratio: 1 unit X == 1 unit Y

    plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout to make space for legend
    plt.show()

def run_pathfinding_simulation(num_tries=1):
    """Runs the pathfinding simulation multiple times."""
    # Determine the script's directory and construct the map file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    map_json_path = os.path.join(script_dir, '../data/map.json')
    # For alternative structure: '../data/map.json'
    # map_json_path = os.path.join(script_dir, '..', 'data', 'map.json')

    warehouse_data = load_json_data(map_json_path)

    if not warehouse_data:
        print("Exiting simulation due to map loading failure.")
        return

    all_nodes_map = warehouse_data.get("nodes")
    all_racks_map = warehouse_data.get("racks")


    if not all_nodes_map:
        print("Error: 'nodes' key not found or empty in map.json.")
        return

    # Filter for nodes that are not locked and have coordinates
    valid_nodes_for_pathfinding = [
        node_id for node_id, info in all_nodes_map.items()
        if not info.get("locked", False) and \
           isinstance(info.get("x"), (int, float)) and \
           isinstance(info.get("y"), (int, float))
    ]

    if len(valid_nodes_for_pathfinding) < 2:
        print("Not enough valid (unlocked, with coordinates) nodes for pathfinding.")
        return

    for i in range(num_tries):
        print(f"\n--- Simulation Run {i + 1} ---")

        # Select start and goal nodes
        start_node = "E1-2" # Your specified start
        if start_node not in valid_nodes_for_pathfinding:
            print(f"Warning: Default start node '{start_node}' is not valid. Choosing a random valid start.")
            start_node = random.choice(valid_nodes_for_pathfinding)

        goal_node = random.choice(valid_nodes_for_pathfinding)
        while goal_node == start_node: # Ensure goal is different
            goal_node = random.choice(valid_nodes_for_pathfinding)

        print(f"Attempting path from: {start_node} to {goal_node}")

        # Check if start node has neighbors (sanity check)
        if not all_nodes_map.get(start_node, {}).get("neighbours"):
            print(f"Warning: Start node '{start_node}' has no listed neighbors. Pathfinding might fail or be trivial.")
            # Still attempt to draw, showing just start/goal
            draw_warehouse_path(all_nodes_map, all_racks_map, start_node, goal_node, None, explored_nodes=set([start_node]),
                                title=f"Run {i+1}: {start_node} to {goal_node} (Start has no neighbors)")
            continue


        path_found, nodes_explored = greedy_best_first_search(
            start_node, goal_node, all_nodes_map, manhattan_distance_heuristic
        )

        if path_found:
            print(f"✅ Path found: {' -> '.join(path_found)}")
            print(f"Path length: {len(path_found) -1} segments, {len(path_found)} nodes.")
            print(f"Explored {len(nodes_explored)} nodes.")
        else:
            print(f"❌ No path found from {start_node} to {goal_node}.")
            print(f"Explored {len(nodes_explored)} nodes before failure.")


        draw_warehouse_path(all_nodes_map, all_racks_map, start_node, goal_node, path_found, nodes_explored,
                            title=f"Run {i+1}: {start_node} to {goal_node} (Greedy BFS)")

if __name__ == "__main__":
    run_pathfinding_simulation(num_tries=3) # Run 3 example paths