import json
import heapq
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches # <<<<<<<<<<<<<<<<<<<< ADDED IMPORT
import matplotlib.colors as mcolors # For potential gradient effects (not used yet but good to have)
import numpy as np # For gradient effects (not used yet)
import random

# --- ENHANCED STYLING CONSTANTS (Copied from previous "beautiful" version) ---
FIG_BG_COLOR = '#F4F6F6'
AXES_BG_COLOR = '#FFFFFF'
GRID_COLOR = '#E0E0E0'
GRID_STYLE = '--'
GRID_ALPHA = 0.7

NODE_COLOR_DEFAULT = '#D0D3D4'
NODE_SIZE_DEFAULT = 18
NODE_EDGE_COLOR_DEFAULT = '#B0B3B4'
NODE_EDGE_WIDTH_DEFAULT = 0.5

NODE_COLOR_EXPLORED = '#A9CCE3'
NODE_SIZE_EXPLORED = 22
NODE_EDGE_COLOR_EXPLORED = '#7FB3D5'

NODE_COLOR_PATH = '#F5B041'
NODE_SIZE_PATH = 35
NODE_EDGE_COLOR_PATH = '#AF601A'
NODE_EDGE_WIDTH_PATH = 1

PATH_LINE_COLOR = '#E74C3C'
PATH_LINE_WIDTH = 2.5
PATH_LINE_STYLE = '-'
PATH_MARKER_STYLE = 'o'
PATH_MARKER_SIZE = 5
PATH_MARKER_EDGE_COLOR = '#A93226'

START_NODE_COLOR = '#2ECC71'
START_NODE_SIZE_MULTIPLIER = 2.8
START_NODE_EDGE_COLOR = '#1D8348'
START_NODE_MARKER = 'P'

GOAL_NODE_COLOR = '#AF7AC5'
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

MANUALLY_DEFINED_AREAS = [
    # IMPORTANT: If your Figma has green obstacles or other special blue zones
    # not directly represented by racks, you MUST define them here.
    # Example:
    # {'x': 450, 'y': 500, 'width': 40, 'height': 50, 'face_color': '#90EE90', 'edge_color': '#5499C7', 'type': 'obstacle'},
]
# --- END OF STYLING CONSTANTS ---


# --- Your existing functions (load_json_data, get_node_coordinates, etc.) ---
def load_json_data(path):
    """Loads JSON data from the given file path."""
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{path}'. Make sure the path is correct.")
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
        return float('inf')
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current_node_id):
    """Reconstructs the path from the start node to the current_node_id."""
    path = [current_node_id]
    while current_node_id in came_from and came_from[current_node_id] is not None:
        current_node_id = came_from[current_node_id]
        path.append(current_node_id)
    return path[::-1]

def greedy_best_first_search(start_node_id, goal_node_id, nodes_data, heuristic_function):
    if start_node_id not in nodes_data or goal_node_id not in nodes_data:
        print("Error: Start or goal node ID not found in nodes_data.")
        return None, set()
    open_list_pq = []
    entry_count = 0
    heapq.heappush(open_list_pq, (heuristic_function(start_node_id, goal_node_id, nodes_data), entry_count, start_node_id))
    entry_count += 1
    came_from = {start_node_id: None}
    explored_nodes = set()
    while open_list_pq:
        _, _, current_node_id = heapq.heappop(open_list_pq)
        if current_node_id in explored_nodes:
            continue
        explored_nodes.add(current_node_id)
        if current_node_id == goal_node_id:
            return reconstruct_path(came_from, current_node_id), explored_nodes
        current_node_info = nodes_data.get(current_node_id, {})
        neighbors = current_node_info.get("neighbours", [])
        for neighbor_id in neighbors:
            if neighbor_id not in nodes_data:
                continue
            neighbor_info = nodes_data[neighbor_id]
            if neighbor_info.get("locked", False):
                continue
            if neighbor_id not in explored_nodes and neighbor_id not in came_from:
                came_from[neighbor_id] = current_node_id
                priority = heuristic_function(neighbor_id, goal_node_id, nodes_data)
                heapq.heappush(open_list_pq, (priority, entry_count, neighbor_id))
                entry_count += 1
    return None, explored_nodes

# --- REPLACED draw_warehouse_path FUNCTION ---
def draw_warehouse_path(nodes_data, racks_data, start_node_id, goal_node_id, path, explored_nodes=None, title="Warehouse Path"):
    if not nodes_data:
        print("No node data provided for drawing.")
        return

    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor(FIG_BG_COLOR)
    ax.set_facecolor(AXES_BG_COLOR)

    # 0. Manually Defined Areas
    for area_def in MANUALLY_DEFINED_AREAS:
        rect = patches.Rectangle((area_def['x'], area_def['y']), area_def['width'], area_def['height'],
                                 linewidth=area_def.get('linewidth', 1),
                                 edgecolor=area_def.get('edge_color', 'none'),
                                 facecolor=area_def.get('face_color', 'none'),
                                 alpha=area_def.get('alpha', 1.0), zorder=0)
        ax.add_patch(rect)

    # 1. Racks
    if racks_data:
        for rack_id, rack_info in racks_data.items():
            sc = rack_info.get("start_cords")
            cc = rack_info.get("center_cords")
            ec = rack_info.get("end_cords")
            is_frozen = rack_info.get("is_frozen", False)
            
            rack_body_color = RACK_COLOR_FROZEN_BLUE if is_frozen else RACK_COLOR_NORMAL
            current_rack_edge_color = RACK_EDGE_COLOR_FROZEN if is_frozen else RACK_EDGE_COLOR

            if sc and cc and ec: # Ensure all coordinate types are present
                x_span = abs(sc[0] - ec[0])
                y_span = abs(sc[1] - ec[1])
                
                if y_span > x_span : # Vertical Rack
                    y_start = min(sc[1], ec[1]) 
                    height = y_span
                    center_x = cc[0]
                    rect_x = center_x - RACK_VISUAL_WIDTH_FOR_VERTICAL / 2 
                    rect = patches.Rectangle((rect_x, y_start), RACK_VISUAL_WIDTH_FOR_VERTICAL, height,
                                             linewidth=RACK_LINEWIDTH, edgecolor=current_rack_edge_color, 
                                             facecolor=rack_body_color, zorder=1, alpha=0.9)
                    ax.add_patch(rect)
                elif x_span >= y_span: # Horizontal Rack
                    x_start = min(sc[0], ec[0]) 
                    width = x_span
                    center_y = cc[1]
                    rect_y = center_y - RACK_VISUAL_HEIGHT_FOR_HORIZONTAL / 2
                    rect = patches.Rectangle((x_start, rect_y), width, RACK_VISUAL_HEIGHT_FOR_HORIZONTAL,
                                             linewidth=RACK_LINEWIDTH, edgecolor=current_rack_edge_color, 
                                             facecolor=rack_body_color, zorder=1, alpha=0.9)
                    ax.add_patch(rect)

    # 2. All Nodes
    all_node_x = [info["x"] for info in nodes_data.values() if "x" in info and isinstance(info["x"], (int,float))]
    all_node_y = [info["y"] for info in nodes_data.values() if "y" in info and isinstance(info["y"], (int,float))]
    ax.scatter(all_node_x, all_node_y, color=NODE_COLOR_DEFAULT, s=NODE_SIZE_DEFAULT, 
               zorder=2, edgecolors=NODE_EDGE_COLOR_DEFAULT, linewidths=NODE_EDGE_WIDTH_DEFAULT, label="All Nodes")

    # 3. Explored Nodes
    if explored_nodes:
        # Ensure explored_nodes is a set of valid node_ids present in nodes_data
        valid_explored_nodes = [n for n in explored_nodes if n in nodes_data and "x" in nodes_data.get(n,{}) and "y" in nodes_data.get(n,{})]
        explored_x = [nodes_data[n]["x"] for n in valid_explored_nodes]
        explored_y = [nodes_data[n]["y"] for n in valid_explored_nodes]
        if explored_x : 
            ax.scatter(explored_x, explored_y, color=NODE_COLOR_EXPLORED, s=NODE_SIZE_EXPLORED, 
                       zorder=3, edgecolors=NODE_EDGE_COLOR_EXPLORED, linewidths=NODE_EDGE_WIDTH_DEFAULT, label="Explored Nodes")

    # 4. Path
    if path:
        # Ensure path is a list of valid node_ids present in nodes_data
        valid_path_nodes = [n for n in path if n in nodes_data and "x" in nodes_data.get(n,{}) and "y" in nodes_data.get(n,{})]
        path_x = [nodes_data[n]["x"] for n in valid_path_nodes]
        path_y = [nodes_data[n]["y"] for n in valid_path_nodes]
        if path_x and path_y: # Check if path_x/path_y are not empty after filtering
            ax.plot(path_x, path_y, color=PATH_LINE_COLOR, linewidth=PATH_LINE_WIDTH, 
                    zorder=4, linestyle=PATH_LINE_STYLE,
                    marker=PATH_MARKER_STYLE, markersize=PATH_MARKER_SIZE, 
                    markeredgecolor=PATH_MARKER_EDGE_COLOR, markeredgewidth=0.5,
                    label="Agent Path")
            ax.scatter(path_x, path_y, color=NODE_COLOR_PATH, s=NODE_SIZE_PATH, 
                       zorder=5, edgecolors=NODE_EDGE_COLOR_PATH, linewidths=NODE_EDGE_WIDTH_PATH)

    # 5. Start and Goal Nodes
    sx, sy = get_node_coordinates(start_node_id, nodes_data)
    gx, gy = get_node_coordinates(goal_node_id, nodes_data)
    
    if sx is not None:
        ax.scatter(sx+1, sy+1, color='gray', s=NODE_SIZE_PATH * START_NODE_SIZE_MULTIPLIER * 1.1, 
                   marker=START_NODE_MARKER, zorder=5, alpha=0.4) 
        ax.scatter(sx, sy, color=START_NODE_COLOR, s=NODE_SIZE_PATH * START_NODE_SIZE_MULTIPLIER, 
                   label="Start", edgecolors=START_NODE_EDGE_COLOR, linewidths=1.5, 
                   marker=START_NODE_MARKER, zorder=6)
    if gx is not None: 
        ax.scatter(gx+1, gy+1, color='gray', s=NODE_SIZE_PATH * GOAL_NODE_SIZE_MULTIPLIER * 1.1, 
                   marker=GOAL_NODE_MARKER, zorder=5, alpha=0.4)
        ax.scatter(gx, gy, color=GOAL_NODE_COLOR, s=NODE_SIZE_PATH * GOAL_NODE_SIZE_MULTIPLIER, 
                   label="Goal", edgecolors=GOAL_NODE_EDGE_COLOR, linewidths=1.5, 
                   marker=GOAL_NODE_MARKER, zorder=6)

    ax.set_title(title, color=TEXT_COLOR_DARK, fontsize=14, fontweight='medium')
    ax.set_xticks([])
    ax.set_yticks([])
    
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)

    ax.legend(loc='upper right', frameon=True, facecolor='#FFFFFFE6', edgecolor=GRID_COLOR, fontsize=9, title_fontsize=10)
    ax.grid(True, linestyle=GRID_STYLE, color=GRID_COLOR, alpha=GRID_ALPHA, zorder=-1)

    ax.invert_yaxis()
    ax.set_aspect('equal', adjustable='box')
    
    # Auto-adjust plot limits with padding
    # Consolidate all x and y coordinates that will be plotted
    all_plotted_x = []
    all_plotted_y = []
    if all_node_x: all_plotted_x.extend(x for x in all_node_x if x is not None)
    if all_node_y: all_plotted_y.extend(y for y in all_node_y if y is not None)
    # Add rack coordinates if needed for bounds, or assume nodes cover the area
    
    if all_plotted_x and all_plotted_y:
        min_x, max_x = min(all_plotted_x), max(all_plotted_x)
        min_y, max_y = min(all_plotted_y), max(all_plotted_y)
        
        x_margin = (max_x - min_x) * 0.05 if (max_x - min_x) > 0 else 50
        y_margin = (max_y - min_y) * 0.05 if (max_y - min_y) > 0 else 50
        
        ax.set_xlim(min_x - x_margin, max_x + x_margin)
        ax.set_ylim(max_y + y_margin, min_y - y_margin) # Inverted Y: max is top, min is bottom

    plt.tight_layout(pad=1.5)
    plt.show()
# --- END OF REPLACED draw_warehouse_path FUNCTION ---


def run_pathfinding_simulation(num_tries=1):
    """Runs the pathfinding simulation multiple times."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Using the path from your script structure
    map_json_path = os.path.join(script_dir, '../data/map.json') 

    warehouse_data = load_json_data(map_json_path)

    if not warehouse_data:
        print("Exiting simulation due to map loading failure.")
        return

    all_nodes_map = warehouse_data.get("nodes")
    all_racks_map = warehouse_data.get("racks") 

    if not all_nodes_map:
        print("Error: 'nodes' key not found or empty in map.json.")
        return

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

        start_node = "E1-2" # Default start, as in your original script
        if start_node not in valid_nodes_for_pathfinding:
            print(f"Warning: Default start node '{start_node}' is not valid. Choosing a random valid start.")
            start_node = random.choice(valid_nodes_for_pathfinding)

        goal_node = random.choice(valid_nodes_for_pathfinding)
        while goal_node == start_node: 
            goal_node = random.choice(valid_nodes_for_pathfinding)
        
        current_title = f"Run {i+1}: {start_node} to {goal_node} (Greedy BFS)"
        print(f"Attempting path for: {current_title}")

        if not all_nodes_map.get(start_node, {}).get("neighbours"):
            print(f"Warning: Start node '{start_node}' has no listed neighbors. Pathfinding might fail or be trivial.")
            draw_warehouse_path(all_nodes_map, all_racks_map, start_node, goal_node, None, set([start_node]),
                                title=f"Run {i+1}: {start_node} to {goal_node} (Start has no neighbors)")
            continue

        path_found, nodes_explored = greedy_best_first_search(
            start_node, goal_node, all_nodes_map, manhattan_distance_heuristic
        )

        if path_found:
            print(f"✅ Path found: {' -> '.join(path_found)}")
            print(f"Path length: {len(path_found) -1} segments.")
            # print(f"Explored {len(nodes_explored)} nodes.") # Optional: can be verbose
        else:
            print(f"❌ No path found from {start_node} to {goal_node}.")
            # print(f"Explored {len(nodes_explored)} nodes before failure.")


        draw_warehouse_path(all_nodes_map, all_racks_map, start_node, goal_node, path_found, nodes_explored,
                            title=current_title)

if __name__ == "__main__":
    run_pathfinding_simulation(num_tries=3) # Run 3 example paths