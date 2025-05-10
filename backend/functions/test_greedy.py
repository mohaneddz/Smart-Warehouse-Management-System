import json
import heapq
import os
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import numpy as np
import random

# --- ENHANCED STYLING CONSTANTS ---
FIG_BG_COLOR = '#F4F6F6'
AXES_BG_COLOR = '#FFFFFF'
GRID_COLOR = '#E0E0E0'
GRID_STYLE = '--'
GRID_ALPHA = 0.7
NODE_COLOR_DEFAULT = '#D0D3D4'
NODE_SIZE_DEFAULT = 18
NODE_EDGE_COLOR_DEFAULT = '#B0B3B4'
NODE_EDGE_WIDTH_DEFAULT = 0.5
NODE_COLOR_EXPLORED = '#A9CCE3' # Light Blue
NODE_SIZE_EXPLORED = 22
NODE_EDGE_COLOR_EXPLORED = '#7FB3D5'
NODE_COLOR_PATH = '#F5B041' # Orange
NODE_SIZE_PATH = 35
NODE_EDGE_COLOR_PATH = '#AF601A'
NODE_EDGE_WIDTH_PATH = 1
PATH_LINE_COLOR = '#E74C3C' # Red
PATH_LINE_WIDTH = 2.5
PATH_LINE_STYLE = '-'
PATH_MARKER_STYLE = 'o'
PATH_MARKER_SIZE = 5
PATH_MARKER_EDGE_COLOR = '#A93226'
START_NODE_COLOR = '#2ECC71' # Green
START_NODE_SIZE_MULTIPLIER = 2.8
START_NODE_EDGE_COLOR = '#1D8348'
START_NODE_MARKER = 'P'
GOAL_NODE_COLOR = '#AF7AC5' # Purple
GOAL_NODE_SIZE_MULTIPLIER = 2.8
GOAL_NODE_EDGE_COLOR = '#7D3C98'
GOAL_NODE_MARKER = '*'
RACK_COLOR_NORMAL = '#F7F9F9'
RACK_COLOR_FROZEN_BLUE = '#D6EAF8'
RACK_EDGE_COLOR = '#CCD1D1'
RACK_EDGE_COLOR_FROZEN = '#A9CCE3'
RACK_LINEWIDTH = 0.8
RACK_VISUAL_WIDTH_FOR_VERTICAL = 16
RACK_VISUAL_HEIGHT_FOR_HORIZONTAL = 16
TEXT_COLOR_DARK = '#34495E'
TEXT_COLOR_LIGHT = '#7F8C8D'
MANUALLY_DEFINED_AREAS = []
# --- END OF STYLING CONSTANTS ---

def load_json_data(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{path}'.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{path}'.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading JSON: {e}")
        return None

def get_node_coordinates(node_id, nodes_data):
    node_info = nodes_data.get(node_id)
    if node_info:
        return node_info.get("x"), node_info.get("y")
    return None, None

def manhattan_distance_heuristic(node1_id, node2_id, nodes_data):
    x1, y1 = get_node_coordinates(node1_id, nodes_data)
    x2, y2 = get_node_coordinates(node2_id, nodes_data)
    if None in [x1, y1, x2, y2]:
        # This can happen if a node_id is invalid or lacks coordinates
        # print(f"Warning: Could not get coordinates for {node1_id} or {node2_id} in heuristic.")
        return float('inf')
    return abs(x1 - x2) + abs(y1 - y2)

def calculate_path_distance(path, nodes_data, distance_metric_fn=manhattan_distance_heuristic):
    if not path or len(path) < 2:
        return 0
    total_distance = 0
    for i in range(len(path) - 1):
        node1_id = path[i]
        node2_id = path[i+1]
        dist = distance_metric_fn(node1_id, node2_id, nodes_data)
        if dist == float('inf'):
            print(f"Warning: Infinite distance between adjacent nodes {node1_id} and {node2_id} in path during distance calculation.")
            return float('inf')
        total_distance += dist
    return total_distance

def reconstruct_path(came_from, current_node_id):
    path = [current_node_id]
    while current_node_id in came_from and came_from[current_node_id] is not None:
        current_node_id = came_from[current_node_id]
        path.append(current_node_id)
    return path[::-1]

def greedy_best_first_search(start_node_id, goal_node_id, nodes_data, heuristic_function):
    if start_node_id not in nodes_data or goal_node_id not in nodes_data:
        # print(f"GBFS Warning: Start ({start_node_id}) or Goal ({goal_node_id}) not in nodes_data.")
        return None, set(), 0
    
    open_list_pq = []
    entry_count = 0 # Tie-breaker for heapq
    
    h_start = heuristic_function(start_node_id, goal_node_id, nodes_data)
    if h_start == float('inf'):
        # print(f"GBFS Error: Cannot calculate heuristic for start node {start_node_id} to goal {goal_node_id}.")
        return None, set(), 0
        
    heapq.heappush(open_list_pq, (h_start, entry_count, start_node_id))
    entry_count += 1
    
    came_from = {start_node_id: None}
    explored_nodes = set() # Tracks nodes that have been popped and processed
    
    while open_list_pq:
        _, _, current_node_id = heapq.heappop(open_list_pq)
        
        if current_node_id in explored_nodes:
            continue
        explored_nodes.add(current_node_id)
        
        if current_node_id == goal_node_id:
            path = reconstruct_path(came_from, current_node_id)
            return path, explored_nodes, len(path)
            
        current_node_info = nodes_data.get(current_node_id, {})
        neighbors = current_node_info.get("neighbours", [])
        
        for neighbor_id in neighbors:
            if neighbor_id not in nodes_data:
                # print(f"GBFS Warning: Neighbor {neighbor_id} of {current_node_id} not in nodes_data.")
                continue
            neighbor_info = nodes_data[neighbor_id]
            if neighbor_info.get("locked", False):
                continue
                
            if neighbor_id not in explored_nodes and neighbor_id not in came_from: # came_from check implies not in open_list yet
                came_from[neighbor_id] = current_node_id
                priority = heuristic_function(neighbor_id, goal_node_id, nodes_data)
                if priority == float('inf'):
                    # print(f"GBFS Warning: Infinite heuristic for neighbor {neighbor_id} of {current_node_id}.")
                    continue # Don't add non-viable neighbors
                heapq.heappush(open_list_pq, (priority, entry_count, neighbor_id))
                entry_count += 1
                
    return None, explored_nodes, 0

def a_star_search(start_node_id, goal_node_id, nodes_data, heuristic_function):
    if start_node_id not in nodes_data or goal_node_id not in nodes_data:
        # print(f"A* Warning: Start ({start_node_id}) or Goal ({goal_node_id}) not in nodes_data.")
        return None, set(), 0

    open_list_pq = [] # Priority queue: (f_score, entry_count, node_id)
    entry_count = 0   # Tie-breaker for heapq

    g_score = {node_id: float('inf') for node_id in nodes_data.keys()} # Cost from start to node
    g_score[start_node_id] = 0
    
    f_score = {node_id: float('inf') for node_id in nodes_data.keys()} # Estimated total cost (g + h)
    h_start = heuristic_function(start_node_id, goal_node_id, nodes_data)
    if h_start == float('inf'):
        # print(f"A* Error: Cannot calculate heuristic for start node {start_node_id} to goal {goal_node_id}.")
        return None, set(), 0
    f_score[start_node_id] = h_start
    
    heapq.heappush(open_list_pq, (f_score[start_node_id], entry_count, start_node_id))
    entry_count += 1
    
    came_from = {start_node_id: None}
    explored_nodes_set = set() # Tracks nodes for which neighbors have been fully evaluated (i.e., popped from open_list_pq)

    while open_list_pq:
        current_f, _, current_node_id = heapq.heappop(open_list_pq)
        
        # Optimization: if we've already found a better path to this node, skip
        if current_f > f_score.get(current_node_id, float('inf')):
             continue

        if current_node_id == goal_node_id:
            path = reconstruct_path(came_from, current_node_id)
            return path, explored_nodes_set, len(path)

        explored_nodes_set.add(current_node_id) # Mark as explored (processed)

        current_node_info = nodes_data.get(current_node_id, {})
        neighbors = current_node_info.get("neighbours", [])

        for neighbor_id in neighbors:
            if neighbor_id not in nodes_data:
                # print(f"A* Warning: Neighbor {neighbor_id} of {current_node_id} not in nodes_data.")
                continue
            neighbor_info = nodes_data[neighbor_id]
            if neighbor_info.get("locked", False):
                continue

            # Cost between current and neighbor (assuming 1 if not specified, or use heuristic)
            # For A* to be optimal, this cost should be the actual cost.
            # Here, we use Manhattan distance as the actual edge cost between adjacent nodes.
            cost_to_neighbor = manhattan_distance_heuristic(current_node_id, neighbor_id, nodes_data)
            if cost_to_neighbor == float('inf'): # Should not happen for valid adjacent nodes
                 # print(f"A* Warning: Infinite cost between adjacent {current_node_id} and {neighbor_id}.")
                 continue

            tentative_g_score = g_score.get(current_node_id, float('inf')) + cost_to_neighbor

            if tentative_g_score < g_score.get(neighbor_id, float('inf')):
                came_from[neighbor_id] = current_node_id
                g_score[neighbor_id] = tentative_g_score
                h_neighbor = heuristic_function(neighbor_id, goal_node_id, nodes_data)
                if h_neighbor == float('inf'):
                    # print(f"A* Warning: Infinite heuristic for neighbor {neighbor_id} of {current_node_id}.")
                    continue 
                f_score[neighbor_id] = tentative_g_score + h_neighbor
                
                # Add to P-Queue if not already processed with a better or equal path.
                # Since we check current_f > f_score[current_node_id] at the start of the loop,
                # and we always add to explored_nodes_set when popped,
                # we don't strictly need to check if neighbor_id is in explored_nodes_set here.
                # However, not re-adding if already in open_list_pq with a better f_score can be an optimization.
                # For simplicity, standard A* often just pushes. heapq handles duplicates by processing lowest f_score first.
                # if neighbor_id not in explored_nodes_set: # Not strictly needed with the f_score check at pop
                heapq.heappush(open_list_pq, (f_score[neighbor_id], entry_count, neighbor_id))
                entry_count += 1
                
    return None, explored_nodes_set, 0

def draw_warehouse_path(nodes_data, racks_data, start_node_id, goal_node_id, path, explored_nodes=None, title="Warehouse Path"):
    if not nodes_data:
        print("No node data provided for drawing.")
        return
    fig, ax = plt.subplots(figsize=(16, 12)) 
    fig.patch.set_facecolor(FIG_BG_COLOR)
    ax.set_facecolor(AXES_BG_COLOR)

    # Draw Manually Defined Areas (if any)
    for area_def in MANUALLY_DEFINED_AREAS:
        rect = patches.Rectangle((area_def['x'], area_def['y']), area_def['width'], area_def['height'],
                                 linewidth=area_def.get('linewidth', 1), 
                                 edgecolor=area_def.get('edge_color', 'none'),
                                 facecolor=area_def.get('face_color', 'none'), 
                                 alpha=area_def.get('alpha', 1.0), zorder=0)
        ax.add_patch(rect)

    # Draw Racks
    if racks_data:
        for rack_id, rack_info in racks_data.items():
            sc, cc, ec = rack_info.get("start_cords"), rack_info.get("center_cords"), rack_info.get("end_cords")
            is_frozen = rack_info.get("is_frozen", False)
            rack_body_color = RACK_COLOR_FROZEN_BLUE if is_frozen else RACK_COLOR_NORMAL
            current_rack_edge_color = RACK_EDGE_COLOR_FROZEN if is_frozen else RACK_EDGE_COLOR
            if sc and cc and ec:
                x_coords = [sc[0], ec[0]]
                y_coords = [sc[1], ec[1]]
                x_span, y_span = abs(sc[0] - ec[0]), abs(sc[1] - ec[1])

                if y_span > x_span: # Vertical rack
                    y_start, height = min(y_coords), y_span
                    center_x = cc[0]
                    rect_x = center_x - RACK_VISUAL_WIDTH_FOR_VERTICAL / 2
                    rect_width = RACK_VISUAL_WIDTH_FOR_VERTICAL
                    rect_height = height if height > 0 else RACK_VISUAL_HEIGHT_FOR_HORIZONTAL # Min height for dot-like racks
                    rect = patches.Rectangle((rect_x, y_start), rect_width, rect_height, 
                                             linewidth=RACK_LINEWIDTH, edgecolor=current_rack_edge_color, 
                                             facecolor=rack_body_color, zorder=1, alpha=0.9)
                elif x_span >= y_span: # Horizontal rack (or dot-like)
                    x_start, width = min(x_coords), x_span
                    center_y = cc[1]
                    rect_y = center_y - RACK_VISUAL_HEIGHT_FOR_HORIZONTAL / 2
                    rect_width = width if width > 0 else RACK_VISUAL_WIDTH_FOR_VERTICAL # Min width for dot-like racks
                    rect_height = RACK_VISUAL_HEIGHT_FOR_HORIZONTAL
                    rect = patches.Rectangle((x_start, rect_y), rect_width, rect_height, 
                                             linewidth=RACK_LINEWIDTH, edgecolor=current_rack_edge_color, 
                                             facecolor=rack_body_color, zorder=1, alpha=0.9)
                else: # Should not happen if sc, cc, ec are valid
                    continue
                ax.add_patch(rect)

    # Draw All Nodes (those not explored and not on path, for context)
    all_node_ids = set(nodes_data.keys())
    path_node_ids = set(path) if path else set()
    explored_node_ids = set(explored_nodes) if explored_nodes else set()
    
    # Nodes that are neither in path nor explored (and not start/goal)
    other_nodes_ids = all_node_ids - path_node_ids - explored_node_ids
    if start_node_id: other_nodes_ids.discard(start_node_id)
    if goal_node_id: other_nodes_ids.discard(goal_node_id)

    other_x = [nodes_data[n]["x"] for n in other_nodes_ids if n in nodes_data and "x" in nodes_data[n] and "y" in nodes_data[n]]
    other_y = [nodes_data[n]["y"] for n in other_nodes_ids if n in nodes_data and "x" in nodes_data[n] and "y" in nodes_data[n]]
    if other_x:
        ax.scatter(other_x, other_y, color=NODE_COLOR_DEFAULT, s=NODE_SIZE_DEFAULT, zorder=2,
                   edgecolors=NODE_EDGE_COLOR_DEFAULT, linewidths=NODE_EDGE_WIDTH_DEFAULT, label="Other Nodes")

    # Draw Explored Nodes (not on the path and not start/goal)
    if explored_nodes:
        # Filter out path nodes, start, and goal from explored for distinct plotting
        explored_to_plot_ids = explored_node_ids - path_node_ids
        if start_node_id: explored_to_plot_ids.discard(start_node_id)
        if goal_node_id: explored_to_plot_ids.discard(goal_node_id)

        explored_x = [nodes_data[n]["x"] for n in explored_to_plot_ids if n in nodes_data and "x" in nodes_data[n] and "y" in nodes_data[n]]
        explored_y = [nodes_data[n]["y"] for n in explored_to_plot_ids if n in nodes_data and "x" in nodes_data[n] and "y" in nodes_data[n]]
        if explored_x:
            ax.scatter(explored_x, explored_y, color=NODE_COLOR_EXPLORED, s=NODE_SIZE_EXPLORED, zorder=3,
                       edgecolors=NODE_EDGE_COLOR_EXPLORED, linewidths=NODE_EDGE_WIDTH_DEFAULT, label="Explored Nodes")

    # Draw Path
    if path:
        valid_path_nodes = [n for n in path if n in nodes_data and "x" in nodes_data.get(n,{}) and "y" in nodes_data.get(n,{})]
        path_x = [nodes_data[n]["x"] for n in valid_path_nodes]
        path_y = [nodes_data[n]["y"] for n in valid_path_nodes]
        if path_x and path_y:
            ax.plot(path_x, path_y, color=PATH_LINE_COLOR, linewidth=PATH_LINE_WIDTH, zorder=4, linestyle=PATH_LINE_STYLE,
                    marker=PATH_MARKER_STYLE, markersize=PATH_MARKER_SIZE, markeredgecolor=PATH_MARKER_EDGE_COLOR,
                    markeredgewidth=0.5, label="Agent Path")
            # Path nodes (excluding start/goal for distinct markers, if they are drawn separately)
            path_nodes_intermediate_x = [nodes_data[n]["x"] for n in valid_path_nodes if n != start_node_id and n != goal_node_id]
            path_nodes_intermediate_y = [nodes_data[n]["y"] for n in valid_path_nodes if n != start_node_id and n != goal_node_id]
            if path_nodes_intermediate_x:
                ax.scatter(path_nodes_intermediate_x, path_nodes_intermediate_y, color=NODE_COLOR_PATH, s=NODE_SIZE_PATH, zorder=5,
                           edgecolors=NODE_EDGE_COLOR_PATH, linewidths=NODE_EDGE_WIDTH_PATH)

    # Draw Start and Goal Nodes distinctly
    sx, sy = get_node_coordinates(start_node_id, nodes_data)
    gx, gy = get_node_coordinates(goal_node_id, nodes_data)
    if sx is not None and sy is not None:
        ax.scatter(sx, sy, color=START_NODE_COLOR, s=NODE_SIZE_PATH*START_NODE_SIZE_MULTIPLIER, label="Start Node",
                   edgecolors=START_NODE_EDGE_COLOR, linewidths=1.5, marker=START_NODE_MARKER, zorder=6)
    if gx is not None and gy is not None:
        ax.scatter(gx, gy, color=GOAL_NODE_COLOR, s=NODE_SIZE_PATH*GOAL_NODE_SIZE_MULTIPLIER, label="Goal Node",
                   edgecolors=GOAL_NODE_EDGE_COLOR, linewidths=1.5, marker=GOAL_NODE_MARKER, zorder=6)

    ax.set_title(title, color=TEXT_COLOR_DARK, fontsize=16, fontweight='bold')
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values(): spine.set_edgecolor(GRID_COLOR)
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0., frameon=True, facecolor='#FFFFFFE6', edgecolor=GRID_COLOR, fontsize=9, title_fontsize=10)
    ax.grid(True, linestyle=GRID_STYLE, color=GRID_COLOR, alpha=GRID_ALPHA, zorder=-1)
    ax.invert_yaxis(); ax.set_aspect('equal', adjustable='box')

    # Auto-adjust plot limits
    all_drawn_x = [c for c in other_x + (explored_x if 'explored_x' in locals() else []) + (path_x if path else []) if c is not None]
    all_drawn_y = [c for c in other_y + (explored_y if 'explored_y' in locals() else []) + (path_y if path else []) if c is not None]
    if sx is not None: all_drawn_x.append(sx)
    if sy is not None: all_drawn_y.append(sy)
    if gx is not None: all_drawn_x.append(gx)
    if gy is not None: all_drawn_y.append(gy)

    if all_drawn_x and all_drawn_y:
        min_x, max_x = min(all_drawn_x), max(all_drawn_x)
        min_y, max_y = min(all_drawn_y), max(all_drawn_y)
        x_margin = (max_x - min_x) * 0.1 if (max_x - min_x) > 0 else 50
        y_margin = (max_y - min_y) * 0.1 if (max_y - min_y) > 0 else 50
        ax.set_xlim(min_x - x_margin, max_x + x_margin)
        ax.set_ylim(max_y + y_margin, min_y - y_margin) # Inverted Y

    plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust rect to make space for legend outside
    plt.show()


def run_pathfinding_experiments(num_iterations_per_pair=10, num_node_pairs=5, specific_pairs=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    map_json_path = os.path.join(script_dir, '..', 'data', 'map.json')

    warehouse_data = load_json_data(map_json_path)
    if not warehouse_data:
        print("Exiting due to map loading failure.")
        return

    all_nodes_map = warehouse_data.get("nodes")
    all_racks_map = warehouse_data.get("racks")

    if not all_nodes_map:
        print("Error: 'nodes' key not found or empty in map.json.")
        return

    valid_nodes = [
        node_id for node_id, info in all_nodes_map.items()
        if not info.get("locked", False) and \
           isinstance(info.get("x"), (int, float)) and \
           isinstance(info.get("y"), (int, float))
    ]

    if len(valid_nodes) < 2:
        print("Not enough valid (unlocked, with coordinates) nodes for pathfinding experiments.")
        return

    node_pairs_to_test = []
    if specific_pairs:
        for start_node, goal_node in specific_pairs:
            valid_pair = True
            if start_node not in all_nodes_map:
                print(f"Warning: Specific pair ({start_node}, {goal_node}) invalid. Start node '{start_node}' not found in map. Skipping.")
                valid_pair = False
            elif goal_node not in all_nodes_map:
                print(f"Warning: Specific pair ({start_node}, {goal_node}) invalid. Goal node '{goal_node}' not found in map. Skipping.")
                valid_pair = False
            elif start_node not in valid_nodes:
                 print(f"Warning: Specific pair ({start_node}, {goal_node}) invalid. Start node '{start_node}' is locked or has no/invalid coordinates. Skipping.")
                 valid_pair = False
            elif goal_node not in valid_nodes:
                 print(f"Warning: Specific pair ({start_node}, {goal_node}) invalid. Goal node '{goal_node}' is locked or has no/invalid coordinates. Skipping.")
                 valid_pair = False
            elif start_node == goal_node:
                 print(f"Warning: Specific pair ({start_node}, {goal_node}) invalid. Start and goal nodes are the same. Skipping.")
                 valid_pair = False
            
            if valid_pair:
                node_pairs_to_test.append((start_node, goal_node))
        
        if not node_pairs_to_test:
             print("No valid specific pairs remained after filtering. Exiting.")
             return
    else: # Generate random pairs if specific_pairs is None or empty after filtering
        generated_pairs_set = set()
        # Ensure num_node_pairs does not exceed available unique pairs
        max_possible_pairs = len(valid_nodes) * (len(valid_nodes) - 1) // 2
        target_num_pairs = min(num_node_pairs, max_possible_pairs)
        if target_num_pairs == 0 and len(valid_nodes) >=2: target_num_pairs = 1 # Try to get at least one pair if possible

        while len(node_pairs_to_test) < target_num_pairs and len(valid_nodes) >=2 :
            start_node, goal_node = random.sample(valid_nodes, 2)
            if (start_node, goal_node) not in generated_pairs_set and (goal_node, start_node) not in generated_pairs_set:
                node_pairs_to_test.append((start_node, goal_node))
                generated_pairs_set.add((start_node, goal_node))
        
        if len(node_pairs_to_test) < num_node_pairs and target_num_pairs > 0 :
            print(f"Warning: Could only generate {len(node_pairs_to_test)} unique random node pairs (target was {num_node_pairs}).")
        if not node_pairs_to_test:
            print("Could not generate any node pairs for random testing. Exiting.")
            return

    algorithms = {
        "Greedy BFS": greedy_best_first_search,
        "A* Search": a_star_search
    }
    overall_stats = {name: {"runtimes": [], "distances": [], "path_lengths_nodes": [], 
                            "successes": 0, "failures": 0, "nodes_explored_list": []}
                     for name in algorithms}
    
    print(f"\n--- Starting Pathfinding Experiments ---")
    print(f"Number of unique Start-Goal pairs to test: {len(node_pairs_to_test)}")
    print(f"Iterations per pair: {num_iterations_per_pair}")
    print(f"Total runs per algorithm: {len(node_pairs_to_test) * num_iterations_per_pair}")

    per_pair_results = []

    for pair_idx, (start_node, goal_node) in enumerate(node_pairs_to_test):
        print(f"\n--- Pair {pair_idx+1}/{len(node_pairs_to_test)}: {start_node} -> {goal_node} ---")
        
        current_pair_data = {"start": start_node, "goal": goal_node}
        for algo_key in algorithms.keys():
            current_pair_data[algo_key] = {} # Initialize sub-dictionary for each algo

        for algo_name, search_function in algorithms.items():
            pair_algo_runtimes = []
            pair_algo_distances = []
            pair_algo_path_lengths = []
            pair_algo_nodes_explored = []
            pair_algo_success_count = 0
            
            path_for_drawing = None 
            explored_for_drawing = None

            for i in range(num_iterations_per_pair):
                iter_start_time = time.perf_counter()
                path_found, nodes_explored, path_len_nodes = search_function(
                    start_node, goal_node, all_nodes_map, manhattan_distance_heuristic
                )
                iter_end_time = time.perf_counter()
                runtime_ms = (iter_end_time - iter_start_time) * 1000

                overall_stats[algo_name]["runtimes"].append(runtime_ms)
                overall_stats[algo_name]["nodes_explored_list"].append(len(nodes_explored))
                pair_algo_runtimes.append(runtime_ms)
                pair_algo_nodes_explored.append(len(nodes_explored))

                if path_found:
                    overall_stats[algo_name]["successes"] += 1
                    pair_algo_success_count += 1
                    distance = calculate_path_distance(path_found, all_nodes_map, manhattan_distance_heuristic)
                    overall_stats[algo_name]["distances"].append(distance)
                    overall_stats[algo_name]["path_lengths_nodes"].append(path_len_nodes)
                    
                    pair_algo_distances.append(distance)
                    pair_algo_path_lengths.append(path_len_nodes)
                    if i == 0 : # Store first successful path for this pair/algo for drawing
                        path_for_drawing = path_found
                        explored_for_drawing = nodes_explored
                else:
                    overall_stats[algo_name]["failures"] += 1
            
            current_pair_data[algo_name]["runtime_avg_ms"] = np.mean(pair_algo_runtimes) if pair_algo_runtimes else float('nan')
            current_pair_data[algo_name]["distance_avg"] = np.mean(pair_algo_distances) if pair_algo_distances else float('nan')
            current_pair_data[algo_name]["path_len_avg"] = np.mean(pair_algo_path_lengths) if pair_algo_path_lengths else float('nan')
            current_pair_data[algo_name]["nodes_explored_avg"] = np.mean(pair_algo_nodes_explored) if pair_algo_nodes_explored else float('nan')
            current_pair_data[algo_name]["success_rate"] = (pair_algo_success_count / num_iterations_per_pair) * 100 if num_iterations_per_pair > 0 else 0
            current_pair_data[algo_name]["path_example"] = path_for_drawing 
            current_pair_data[algo_name]["explored_example"] = explored_for_drawing 

        per_pair_results.append(current_pair_data)

    print("\n\n--- Aggregate Experiment Statistics ---")
    for algo_name, stats in overall_stats.items():
        print(f"\nAlgorithm: {algo_name}")
        total_attempts = stats["successes"] + stats["failures"]
        if total_attempts == 0:
            print("  No runs executed for this algorithm.")
            continue
        success_rate = (stats["successes"] / total_attempts) * 100 if total_attempts > 0 else 0
        avg_runtime = np.mean(stats["runtimes"]) if stats["runtimes"] else float('nan')
        std_runtime = np.std(stats["runtimes"]) if stats["runtimes"] else float('nan')
        avg_distance = np.mean(stats["distances"]) if stats["distances"] else float('nan')
        std_distance = np.std(stats["distances"]) if stats["distances"] else float('nan')
        avg_path_len_nodes = np.mean(stats["path_lengths_nodes"]) if stats["path_lengths_nodes"] else float('nan')
        avg_nodes_explored = np.mean(stats["nodes_explored_list"]) if stats["nodes_explored_list"] else float('nan')

        print(f"  Success Rate: {success_rate:.2f}% ({stats['successes']}/{total_attempts})")
        print(f"  Average Runtime: {avg_runtime:.4f} ms (StdDev: {std_runtime:.4f} ms)")
        if stats["successes"] > 0:
            print(f"  Average Path Distance (Manhattan): {avg_distance:.2f} (StdDev: {std_distance:.2f})")
            print(f"  Average Path Length (nodes): {avg_path_len_nodes:.2f}")
        print(f"  Average Nodes Explored: {avg_nodes_explored:.2f}")

    print("\n\n--- Detailed Per-Pair Comparison ---")
    header = f"{'Pair':<16} | {'Algorithm':<12} | {'Runtime(ms)':<12} | {'Distance':<10} | {'PathLen(N)':<12} | {'Explored(N)':<13} | {'Success%':<10}"
    print(header)
    print("-" * len(header))
    for res in per_pair_results:
        start_goal = f"{res['start'][:7]}..->{res['goal'][:7]}.." if len(res['start']) > 7 or len(res['goal']) > 7 else f"{res['start']}->{res['goal']}"
        start_goal = start_goal.ljust(16) # Ensure pair string is fixed width

        for algo_key_for_print in algorithms.keys():
            algo_res = res[algo_key_for_print]
            runtime_str = f"{algo_res.get('runtime_avg_ms', float('nan')):.3f}"
            dist_str = f"{algo_res.get('distance_avg', float('nan')):.1f}"
            pathlen_str = f"{algo_res.get('path_len_avg', float('nan')):.1f}"
            explored_str = f"{algo_res.get('nodes_explored_avg', float('nan')):.1f}"
            success_str = f"{algo_res.get('success_rate', 0.0):.1f}"
            
            print(f"{start_goal} | {algo_key_for_print:<12} | {runtime_str:<12} | {dist_str:<10} | {pathlen_str:<12} | {explored_str:<13} | {success_str:<10}")
        print("-" * len(header))

    # Plot one example from the last pair tested for visual comparison
    if per_pair_results:
        last_pair_data = per_pair_results[-1]
        last_start, last_goal = last_pair_data["start"], last_pair_data["goal"]
        
        gbfs_key = "Greedy BFS"
        astar_key = "A* Search"

        if gbfs_key in last_pair_data:
            print(f"\nPlotting one example for {gbfs_key}: {last_start} -> {last_goal}")
            path_g = last_pair_data[gbfs_key].get("path_example")
            explored_g = last_pair_data[gbfs_key].get("explored_example")
            dist_g = last_pair_data[gbfs_key].get('distance_avg', float('nan'))
            len_g_nodes = len(path_g) if path_g else 0
            len_g_explored = len(explored_g) if explored_g else 0

            if path_g:
                draw_warehouse_path(all_nodes_map, all_racks_map, last_start, last_goal, path_g, explored_g,
                                    title=f"{gbfs_key}: {last_start} to {last_goal}\nDist: {dist_g:.1f}, Path Nodes: {len_g_nodes}, Explored: {len_g_explored}")
            else:
                print(f"  No path found by {gbfs_key} for {last_start} -> {last_goal} in example run to plot.")

        if astar_key in last_pair_data:
            print(f"Plotting one example for {astar_key}: {last_start} -> {last_goal}")
            path_a = last_pair_data[astar_key].get("path_example")
            explored_a = last_pair_data[astar_key].get("explored_example")
            dist_a = last_pair_data[astar_key].get('distance_avg', float('nan'))
            len_a_nodes = len(path_a) if path_a else 0
            len_a_explored = len(explored_a) if explored_a else 0

            if path_a:
                draw_warehouse_path(all_nodes_map, all_racks_map, last_start, last_goal, path_a, explored_a,
                                    title=f"{astar_key}: {last_start} to {last_goal}\nDist: {dist_a:.1f}, Path Nodes: {len_a_nodes}, Explored: {len_a_explored}")
            else:
                print(f"  No path found by {astar_key} for {last_start} -> {last_goal} in example run to plot.")
    else:
        print("\nNo pairs were tested, so no plots will be generated.")

if __name__ == "__main__":
    # Define specific start-goal pairs for consistent testing.
    # IMPORTANT: Replace these with ACTUAL VALID, UNLOCKED node IDs from YOUR map.json
    # The warnings you received previously indicate these example IDs might not be valid in your map.
    specific_test_pairs = [
        ("E1-2", "N10-13"),  # Example: Assumed valid from your earlier run
        ("E1-1", "N30-25"),  # Example: Assumed valid
        ("C1-1", "G3"),      # Example: Assumed valid
        ("N1-1", "N20-10"),  # Example: Assumed valid
        # ("E2-1", "A3"),    # This was previously invalid, check your map for a replacement
        ("N13-1", "N13-25"), # Example: Assumed valid
        ("C4-13", "E1-7"),   # Example: Assumed valid
        # ("N28-1", "N2-30"),# This might be a long one, good test
        # ("J1", "N1-12"),   # This was previously invalid, check your map for a replacement or use node near rack J1
        # ("H1", "F3")     # This was previously invalid, check your map for a replacement or use node near rack H1
        # Add more valid pairs from your map to get at least a few for testing.
    ]
    
    # If you don't have specific valid pairs yet, you can test with random pairs:
    # specific_pairs_to_run = None
    # Or, to use the list above (after verifying/replacing invalid ones):
    specific_pairs_to_run = specific_test_pairs

    # You can adjust num_iterations_per_pair and num_node_pairs (if specific_pairs_to_run is None)
    run_pathfinding_experiments(
        num_iterations_per_pair=5,  # Lowered for quicker testing, increase for more stable averages
        num_node_pairs=5,           # Used if specific_pairs_to_run is None
        specific_pairs=specific_pairs_to_run
    )