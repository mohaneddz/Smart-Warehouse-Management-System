import json
import heapq
import os
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import random

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: The file {file_path} is not valid JSON. Details: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error happened while loading {file_path}: {e}")
        return None

warehouse_map_data = load_json_file('map.json')

def get_node_coordinates(node_id, graph_nodes_data):
    node = graph_nodes_data.get(node_id)
    if node:
        x_coord = node.get('x')
        y_coord = node.get('y')
        if isinstance(x_coord, (int, float)) and isinstance(y_coord, (int, float)):
            return (x_coord, y_coord)
    return (None, None)

def heuristic_manhattan(node1_id, node2_id, all_nodes_data):
    x1, y1 = get_node_coordinates(node1_id, all_nodes_data)
    x2, y2 = get_node_coordinates(node2_id, all_nodes_data)
    
    if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
        return abs(x1 - x2) + abs(y1 - y2)
    return float('inf')

def reconstruct_path(came_from_map, current_node_id):
    total_path = [current_node_id]
    node_being_traced = current_node_id
    while node_being_traced in came_from_map and came_from_map[node_being_traced] is not None:
        node_being_traced = came_from_map[node_being_traced]
        total_path.append(node_being_traced)
    return total_path[::-1]

def greedy_best_first_search(start_node_id, goal_node_id, all_nodes_data, heuristic_func):
    if start_node_id not in all_nodes_data or goal_node_id not in all_nodes_data:
        return None, set()

    open_set_pq = [] 
    initial_h_value = heuristic_func(start_node_id, goal_node_id, all_nodes_data)
    heapq.heappush(open_set_pq, (initial_h_value, start_node_id))
    
    came_from = {start_node_id: None}
    closed_set = set()

    while len(open_set_pq) > 0:
        _current_h, current_node_id = heapq.heappop(open_set_pq)

        if current_node_id == goal_node_id:
            path = reconstruct_path(came_from, current_node_id)
            return path, closed_set

        if current_node_id in closed_set:
            continue 
        closed_set.add(current_node_id)
        
        current_node_details = all_nodes_data.get(current_node_id)
        if not current_node_details or 'neighbours' not in current_node_details:
            continue 

        for neighbor_id in current_node_details.get("neighbours", []):
            neighbor_details = all_nodes_data.get(neighbor_id)
            
            if neighbor_details and not neighbor_details.get("locked", False) and neighbor_id not in closed_set:
                if neighbor_id not in came_from: 
                    came_from[neighbor_id] = current_node_id
                    h_value_neighbor = heuristic_func(neighbor_id, goal_node_id, all_nodes_data)
                    heapq.heappush(open_set_pq, (h_value_neighbor, neighbor_id))
                else:
                    pass
                    
    return None, closed_set

def plot_path_on_map(all_nodes_data, start_node_id_plot, goal_node_id_plot, path_node_ids, title="Warehouse Path", explored_nodes_set=None):
    if not all_nodes_data:
        print("Cannot plot: No node data provided.")
        return

    fig, ax = plt.subplots(figsize=(18, 12))

    all_x_coords = []
    all_y_coords = []
    for node_id, node_info in all_nodes_data.items():
        x, y = get_node_coordinates(node_id, all_nodes_data)
        if x is not None and y is not None:
            all_x_coords.append(x)
            all_y_coords.append(y)
            ax.scatter(x, y, c='lightgray', s=30, zorder=1)

    if explored_nodes_set:
        explored_x_coords = []
        explored_y_coords = []
        for n_id in explored_nodes_set:
            if n_id in all_nodes_data:
                ex, ey = get_node_coordinates(n_id, all_nodes_data)
                if ex is not None and ey is not None:
                    explored_x_coords.append(ex)
                    explored_y_coords.append(ey)
        if len(explored_x_coords) > 0:
            ax.scatter(explored_x_coords, explored_y_coords, c='skyblue', s=50, label="Explored Nodes", alpha=0.5, zorder=2)

    start_x, start_y = get_node_coordinates(start_node_id_plot, all_nodes_data)
    goal_x, goal_y = get_node_coordinates(goal_node_id_plot, all_nodes_data)

    if start_x is not None:
        ax.scatter(start_x, start_y, c='lime', s=150, label="Start", zorder=5, marker='P', edgecolors='black') # type: ignore
        ax.text(start_x, start_y - 10, f"Start\n{start_node_id_plot}", fontsize=8, ha='center', color='green', weight='bold', zorder=6) # type: ignore
    if goal_x is not None:
        ax.scatter(goal_x, goal_y, c='magenta', s=150, label="Goal", zorder=5, marker='*', edgecolors='black') # type: ignore
        ax.text(goal_x, goal_y - 10, f"Goal\n{goal_node_id_plot}", fontsize=8, ha='center', color='purple', weight='bold', zorder=6) # type: ignore

    if path_node_ids and len(path_node_ids) > 0 :
        path_x_coords = []
        path_y_coords = []
        path_is_valid_for_plotting = True
        for node_id_in_path in path_node_ids:
            x, y = get_node_coordinates(node_id_in_path, all_nodes_data)
            if x is None or y is None:
                path_is_valid_for_plotting = False
                break
            path_x_coords.append(x)
            path_y_coords.append(y)

        if path_is_valid_for_plotting and len(path_x_coords) > 0:
            ax.plot(path_x_coords, path_y_coords, marker='.', markersize=5, linestyle='-', color='red', linewidth=1.5, label="Found Path", zorder=4)
    else:
        print(f"No path to plot for '{title}'.")

    ax.set_title(title, fontsize=16)
    ax.set_xlabel("X Coordinate", fontsize=12)
    ax.set_ylabel("Y Coordinate", fontsize=12)
    
    legend_elements_list = [
        mlines.Line2D([], [], color='lightgray', marker='o', linestyle='None', markersize=7, label='Map Nodes'),
        mlines.Line2D([], [], color='skyblue', marker='o', linestyle='None', markersize=7, label='Explored Nodes'),
        mlines.Line2D([], [], color='red', marker='.', linestyle='-', markersize=6, linewidth=1.5, label='Found Path'),
        mlines.Line2D([], [], color='lime', marker='P', linestyle='None', markersize=10, markeredgecolor='black', label='Start Node'),
        mlines.Line2D([], [], color='magenta', marker='*', linestyle='None', markersize=10, markeredgecolor='black', label='Goal Node')
    ]
    ax.legend(handles=legend_elements_list, loc='best')

    ax.grid(True, linestyle=':', alpha=0.6)
    ax.invert_yaxis() 
    ax.set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()

def run_pathfinding_simulation(num_operations=10):
    if not warehouse_map_data:
        print("Warehouse map data could not be loaded. Exiting simulation.")
        return

    all_nodes_in_map = warehouse_map_data.get("nodes", {})
    if not all_nodes_in_map:
        print("No nodes found in warehouse map data. Exiting simulation.")
        return

    list_of_node_ids = list(all_nodes_in_map.keys())
    if len(list_of_node_ids) < 2:
        print("Not enough nodes in the map to perform pathfinding.")
        return

    for i in range(num_operations):
        print(f"\n--- Operation {i+1}/{num_operations} ---")
        
        unlocked_node_ids = []
        for node_id, node_data in all_nodes_in_map.items():
            if not node_data.get("locked", False):
                unlocked_node_ids.append(node_id)
        
        if not unlocked_node_ids or len(unlocked_node_ids) < 2 :
             print("Not enough valid (unlocked) nodes to select start/goal. Check map data.")
             break 

        agent_start_node_id = random.choice(unlocked_node_ids)
        selected_goal_node_id = random.choice(unlocked_node_ids)
        
        while selected_goal_node_id == agent_start_node_id:
            selected_goal_node_id = random.choice(unlocked_node_ids)

        if agent_start_node_id not in all_nodes_in_map or selected_goal_node_id not in all_nodes_in_map:
            print(f"Simulation Error: A selected node is not in the map data. This shouldn't happen.")
            continue
            
        start_node_info = all_nodes_in_map[agent_start_node_id]
        if not start_node_info.get("neighbours") or len(start_node_info["neighbours"]) == 0:
            print(f"Warning: Start node '{agent_start_node_id}' has no defined neighbours. Pathfinding from it is not possible.")
            plot_path_on_map(all_nodes_in_map, agent_start_node_id, selected_goal_node_id, None, 
                             f"Greedy - No Path (Start '{agent_start_node_id}' Unconnected)", set())
            continue

        print(f"Selected Start: {agent_start_node_id}, Selected Goal: {selected_goal_node_id}")

        print("\nRunning Greedy Best-First Search...")
        greedy_path_result, greedy_explored_nodes = greedy_best_first_search(
            agent_start_node_id, selected_goal_node_id, all_nodes_in_map, heuristic_manhattan
        )
        
        plot_title_suffix = f"{agent_start_node_id} to {selected_goal_node_id} (Op {i+1})"
        if greedy_path_result:
            print(f"✅ Greedy Path Found: {' -> '.join(greedy_path_result)}")
            print(f"   Path Length: {len(greedy_path_result)-1} edges, Nodes in Closed Set (explored): {len(greedy_explored_nodes)}")
            plot_path_on_map(all_nodes_in_map, agent_start_node_id, selected_goal_node_id, greedy_path_result, 
                             f"Greedy Path - {plot_title_suffix}", greedy_explored_nodes)
        else:
            print(f"❌ Greedy: No path was found.")
            plot_path_on_map(all_nodes_in_map, agent_start_node_id, selected_goal_node_id, None, 
                             f"Greedy - No Path - {plot_title_suffix}", greedy_explored_nodes)
        
if __name__ == "__main__":
    run_pathfinding_simulation(num_operations=3)