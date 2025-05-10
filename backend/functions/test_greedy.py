import json
import heapq
import os
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import numpy as np
import random
import pandas as pd

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
NODE_COLOR_EXPLORED_GBFS = '#A9CCE3'
NODE_EDGE_COLOR_EXPLORED_GBFS = '#7FB3D5'
NODE_COLOR_PATH_ASTAR = '#F5B041'
NODE_EDGE_COLOR_PATH_ASTAR = '#AF601A'
BAR_COLOR_GBFS = '#85C1E9'
BAR_COLOR_ASTAR = '#F8C471'
BOXPLOT_GBFS_PROPS = {'color': BAR_COLOR_GBFS, 'linewidth': 1.5, 'patch_artist': True, 'boxprops': dict(facecolor=mcolors.to_rgba(BAR_COLOR_GBFS, alpha=0.6))}
BOXPLOT_ASTAR_PROPS = {'color': BAR_COLOR_ASTAR, 'linewidth': 1.5, 'patch_artist': True, 'boxprops': dict(facecolor=mcolors.to_rgba(BAR_COLOR_ASTAR, alpha=0.6))}
SCATTER_GBFS_COLOR = BAR_COLOR_GBFS
SCATTER_ASTAR_COLOR = BAR_COLOR_ASTAR
ERROR_BAR_COLOR = '#566573'
NODE_SIZE_EXPLORED = 22
NODE_SIZE_PATH = 35
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
MANUALLY_DEFINED_AREAS = []
# --- END OF STYLING CONSTANTS ---

def load_json_data(path):
    try:
        with open(path, 'r') as f: data = json.load(f); return data
    except FileNotFoundError: print(f"E: JSON file not found: {path}"); return None
    except json.JSONDecodeError: print(f"E: Could not decode JSON: {path}"); return None
    except Exception as e: print(f"E: Unexpected error loading JSON: {e}"); return None

def get_node_coordinates(node_id, nodes_data):
    node_info = nodes_data.get(node_id)
    return (node_info.get("x"), node_info.get("y")) if node_info else (None, None)

def manhattan_distance_heuristic(node1_id, node2_id, nodes_data):
    x1,y1=get_node_coordinates(node1_id,nodes_data); x2,y2=get_node_coordinates(node2_id,nodes_data)
    return abs(x1-x2)+abs(y1-y2) if None not in [x1,y1,x2,y2] else float('inf')

def calculate_path_distance(path, nodes_data, dist_fn=manhattan_distance_heuristic):
    if not path or len(path)<2: return 0
    total_dist=0
    for i in range(len(path)-1):
        d=dist_fn(path[i],path[i+1],nodes_data)
        if d==float('inf'): print(f"W: Inf dist in path calc {path[i]}-{path[i+1]}"); return float('inf')
        total_dist+=d
    return total_dist

def reconstruct_path(came_from, current_node_id):
    path=[current_node_id]
    while current_node_id in came_from and came_from[current_node_id] is not None:
        current_node_id=came_from[current_node_id]; path.append(current_node_id)
    return path[::-1]

def greedy_best_first_search(start_node_id, goal_node_id, nodes_data, heuristic_function):
    if start_node_id not in nodes_data or goal_node_id not in nodes_data: return None,set(),0
    pq,ec=[],0; h_s=heuristic_function(start_node_id,goal_node_id,nodes_data)
    if h_s==float('inf'): return None,set(),0
    heapq.heappush(pq,(h_s,ec,start_node_id)); ec+=1
    cf,ex_n={start_node_id:None},set()
    while pq:
        _,_,curr_n_id=heapq.heappop(pq)
        if curr_n_id in ex_n: continue
        ex_n.add(curr_n_id)
        if curr_n_id==goal_node_id: p=reconstruct_path(cf,curr_n_id); return p,ex_n,len(p)
        curr_n_info=nodes_data.get(curr_n_id,{})
        for neigh_id in curr_n_info.get("neighbours",[]):
            if neigh_id not in nodes_data or nodes_data[neigh_id].get("locked",False): continue
            if neigh_id not in ex_n and neigh_id not in cf:
                cf[neigh_id]=curr_n_id; prio=heuristic_function(neigh_id,goal_node_id,nodes_data)
                if prio==float('inf'): continue
                heapq.heappush(pq,(prio,ec,neigh_id)); ec+=1
    return None,ex_n,0

def a_star_search(start_node_id, goal_node_id, nodes_data, heuristic_function):
    if start_node_id not in nodes_data or goal_node_id not in nodes_data: return None,set(),0
    pq,ec=[],0
    g_s={n:float('inf') for n in nodes_data}; g_s[start_node_id]=0
    f_s={n:float('inf') for n in nodes_data}
    h_s=heuristic_function(start_node_id,goal_node_id,nodes_data)
    if h_s==float('inf'): return None,set(),0
    f_s[start_node_id]=h_s
    heapq.heappush(pq,(f_s[start_node_id],ec,start_node_id)); ec+=1
    cf,ex_n_set={start_node_id:None},set()
    while pq:
        curr_f,_,curr_n_id=heapq.heappop(pq)
        if curr_f > f_s.get(curr_n_id,float('inf')): continue
        if curr_n_id==goal_node_id: p=reconstruct_path(cf,curr_n_id); return p,ex_n_set,len(p)
        ex_n_set.add(curr_n_id)
        curr_n_info=nodes_data.get(curr_n_id,{})
        for neigh_id in curr_n_info.get("neighbours",[]):
            if neigh_id not in nodes_data or nodes_data[neigh_id].get("locked",False): continue
            cost_neigh=manhattan_distance_heuristic(curr_n_id,neigh_id,nodes_data)
            if cost_neigh==float('inf'): continue
            tent_g_s=g_s.get(curr_n_id,float('inf'))+cost_neigh
            if tent_g_s < g_s.get(neigh_id,float('inf')):
                cf[neigh_id]=curr_n_id; g_s[neigh_id]=tent_g_s
                h_n=heuristic_function(neigh_id,goal_node_id,nodes_data)
                if h_n==float('inf'): continue
                f_s[neigh_id]=tent_g_s+h_n
                heapq.heappush(pq,(f_s[neigh_id],ec,neigh_id)); ec+=1
    return None,ex_n_set,0

def draw_warehouse_path(nodes_data, racks_data, start_node_id, goal_node_id, path, explored_nodes=None, title="Warehouse Path", algo_name=""):
    if not nodes_data: print("No node data for drawing."); return
    fig, ax = plt.subplots(figsize=(14, 10)); fig.patch.set_facecolor(FIG_BG_COLOR); ax.set_facecolor(AXES_BG_COLOR)
    for area_def in MANUALLY_DEFINED_AREAS:
        ax.add_patch(patches.Rectangle((area_def['x'], area_def['y']), area_def['width'], area_def['height'],
                                 linewidth=area_def.get('linewidth',1), edgecolor=area_def.get('edge_color','none'),
                                 facecolor=area_def.get('face_color','none'), alpha=area_def.get('alpha',1.0), zorder=0))
    if racks_data:
        for r_id, r_info in racks_data.items():
            sc,cc,ec = r_info.get("start_cords"),r_info.get("center_cords"),r_info.get("end_cords")
            is_fr = r_info.get("is_frozen",False)
            r_col,r_edge=(RACK_COLOR_FROZEN_BLUE,RACK_EDGE_COLOR_FROZEN) if is_fr else (RACK_COLOR_NORMAL,RACK_EDGE_COLOR)
            if sc and cc and ec:
                xs,ys=abs(sc[0]-ec[0]),abs(sc[1]-ec[1])
                if ys>xs:y_st,h,cx=min(sc[1],ec[1]),ys,cc[0];rx=cx-RACK_VISUAL_WIDTH_FOR_VERTICAL/2;ax.add_patch(patches.Rectangle((rx, y_st), RACK_VISUAL_WIDTH_FOR_VERTICAL, h,linewidth=RACK_LINEWIDTH, edgecolor=r_edge, facecolor=r_col, zorder=1, alpha=0.9))
                elif xs>=ys:x_st,w,cy=min(sc[0],ec[0]),xs,cc[1];ry=cy-RACK_VISUAL_HEIGHT_FOR_HORIZONTAL/2;ax.add_patch(patches.Rectangle((x_st, ry), w, RACK_VISUAL_HEIGHT_FOR_HORIZONTAL,linewidth=RACK_LINEWIDTH, edgecolor=r_edge, facecolor=r_col, zorder=1, alpha=0.9))
    all_nx,all_ny=[i["x"] for i in nodes_data.values() if "x" in i],[i["y"] for i in nodes_data.values() if "y" in i]
    ax.scatter(all_nx,all_ny,color=NODE_COLOR_DEFAULT,s=NODE_SIZE_DEFAULT,zorder=2,edgecolors=NODE_EDGE_COLOR_DEFAULT,linewidths=NODE_EDGE_WIDTH_DEFAULT,label="Other Nodes")
    
    node_color_exp,node_edge_exp = NODE_COLOR_EXPLORED_GBFS,NODE_EDGE_COLOR_EXPLORED_GBFS
    node_color_pth,node_edge_pth = NODE_COLOR_PATH_ASTAR,NODE_EDGE_COLOR_PATH_ASTAR
    
    if explored_nodes:
        val_ex_n=list(set(n for n in explored_nodes if n in nodes_data and "x" in nodes_data[n])-(set(path) if path else set()))
        ex_x,ex_y=[nodes_data[n]["x"] for n in val_ex_n],[nodes_data[n]["y"] for n in val_ex_n]
        if ex_x: ax.scatter(ex_x,ex_y,color=node_color_exp,s=NODE_SIZE_EXPLORED,zorder=3,edgecolors=node_edge_exp,linewidths=NODE_EDGE_WIDTH_DEFAULT,label="Explored")
    if path:
        val_p_n=[n for n in path if n in nodes_data and "x" in nodes_data[n]]
        p_x,p_y=[nodes_data[n]["x"] for n in val_p_n],[nodes_data[n]["y"] for n in val_p_n]
        if p_x and p_y:
            ax.plot(p_x,p_y,color=PATH_LINE_COLOR,linewidth=PATH_LINE_WIDTH,zorder=4,linestyle=PATH_LINE_STYLE,marker=PATH_MARKER_STYLE,markersize=PATH_MARKER_SIZE,markeredgecolor=PATH_MARKER_EDGE_COLOR,markeredgewidth=0.5,label="Path")
            ax.scatter(p_x,p_y,color=node_color_pth,s=NODE_SIZE_PATH,zorder=5,edgecolors=node_edge_pth,linewidths=NODE_EDGE_WIDTH_PATH)
    sx,sy=get_node_coordinates(start_node_id,nodes_data); gx,gy=get_node_coordinates(goal_node_id,nodes_data)
    if sx is not None:ax.scatter(sx,sy,color=START_NODE_COLOR,s=NODE_SIZE_PATH*START_NODE_SIZE_MULTIPLIER,label="Start",edgecolors=START_NODE_EDGE_COLOR,linewidths=1.5,marker=START_NODE_MARKER,zorder=6)
    if gx is not None:ax.scatter(gx,gy,color=GOAL_NODE_COLOR,s=NODE_SIZE_PATH*GOAL_NODE_SIZE_MULTIPLIER,label="Goal",edgecolors=GOAL_NODE_EDGE_COLOR,linewidths=1.5,marker=GOAL_NODE_MARKER,zorder=6)
    ax.set_title(title,color=TEXT_COLOR_DARK,fontsize=14,fontweight='medium');ax.set_xticks([]);ax.set_yticks([])
    for sp in ax.spines.values():sp.set_edgecolor(GRID_COLOR)
    ax.legend(loc='upper left',bbox_to_anchor=(1.02,1),borderaxespad=0.,frameon=True,facecolor='#FFFFFFE6',edgecolor=GRID_COLOR,fontsize=9,title_fontsize=10)
    ax.grid(True,linestyle=GRID_STYLE,color=GRID_COLOR,alpha=GRID_ALPHA,zorder=-1);ax.invert_yaxis();ax.set_aspect('equal',adjustable='box')
    all_plot_x,all_plot_y=[x for x in all_nx if x is not None],[y for y in all_ny if y is not None]
    if all_plot_x and all_plot_y:
        min_x,max_x=min(all_plot_x),max(all_plot_x);min_y,max_y=min(all_plot_y),max(all_plot_y)
        x_m,y_m=(max_x-min_x)*0.05 if (max_x-min_x)>0 else 50,(max_y-min_y)*0.05 if (max_y-min_y)>0 else 50
        ax.set_xlim(min_x-x_m,max_x+x_m);ax.set_ylim(max_y+y_m,min_y-y_m)
    plt.tight_layout(rect=[0,0,0.85,1]);plt.show()

def plot_bar_charts_with_errors(overall_stats, algorithms_list):
    # THIS metrics_config dictionary NOW INCLUDES 'title'
    metrics_config = {
        "runtimes_ms": {"label": "Average Runtime (ms)", "title": "Average Runtime", "lower_is_better": True},
        "path_distances": {"label": "Average Path Distance (Cost)", "title": "Average Path Distance", "lower_is_better": True},
        "path_lengths_nodes": {"label": "Average Path Length (Nodes)", "title": "Average Path Length", "lower_is_better": True},
        "nodes_explored": {"label": "Average Nodes Explored", "title": "Average Nodes Explored", "lower_is_better": True},
        "success_rate": {"label": "Success Rate (%)", "title": "Success Rate", "lower_is_better": False}
    }
    num_metrics = len(metrics_config)
    n_cols = 2; n_rows = (num_metrics + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(8 * n_cols, 6 * n_rows), squeeze=False)
    axes = axes.flatten()
    algo_colors_map = {"Greedy BFS": BAR_COLOR_GBFS, "A* Search": BAR_COLOR_ASTAR}

    plot_idx = 0
    for metric_key, config in metrics_config.items():
        if plot_idx >= len(axes): break
        ax = axes[plot_idx]
        metric_label = config["label"]
        averages, std_devs = [], []

        for algo_name in algorithms_list:
            s = overall_stats.get(algo_name, {})
            if metric_key == "success_rate":
                total = s.get("successes",0) + s.get("failures",0)
                avg = (s.get("successes",0)/total)*100 if total > 0 else 0
                std = 0 # Std dev not typically shown for success rate this way
            else:
                data_list = s.get(metric_key, []) # This key should be 'runtimes_ms', 'path_distances' etc.
                avg = np.mean(data_list) if data_list else 0
                std = np.std(data_list) if data_list else 0
            averages.append(avg)
            std_devs.append(std)

        bars = ax.bar(algorithms_list, averages, yerr=(std_devs if metric_key != "success_rate" else None),
                      color=[algo_colors_map.get(name, NODE_COLOR_DEFAULT) for name in algorithms_list], capsize=5, ecolor=ERROR_BAR_COLOR, alpha=0.8)
        
        ax.set_ylabel(metric_label); ax.set_title(f"{config['title']}") # Correctly uses 'title'
        
        ax.grid(True, axis='y', linestyle=GRID_STYLE, alpha=GRID_ALPHA, zorder=0)
        ax.set_xticklabels(algorithms_list, rotation=0, ha='center')
        for bar_idx, bar in enumerate(bars):
            yval = bar.get_height()
            text_label = f'{yval:.1f}%' if metric_key == "success_rate" else f'{yval:.2f}'
            ax.text(bar.get_x()+bar.get_width()/2.0, yval, text_label, ha='center', va='bottom', 
                    fontsize=9, color=TEXT_COLOR_DARK, bbox=dict(facecolor='white', alpha=0.5, pad=0.5, boxstyle='round,pad=0.2'))
        plot_idx += 1
    
    for i in range(plot_idx, len(axes)): fig.delaxes(axes[i])
    fig.suptitle("Algorithm Performance Comparison between A* and Greedy", fontsize=16, fontweight='bold', color=TEXT_COLOR_DARK)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def plot_box_plots_for_metrics(all_runs_df, algorithms_list, metrics_config):
    plotable_metrics = {k:v for k,v in metrics_config.items() if k != "success_rate"}
    num_metrics = len(plotable_metrics)
    if num_metrics == 0: return

    n_cols = 2
    n_rows = (num_metrics + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(8 * n_cols, 6 * n_rows), squeeze=False)
    axes = axes.flatten()
    plot_idx = 0

    for metric_key, config in plotable_metrics.items():
        if plot_idx >= len(axes): break
        ax = axes[plot_idx]
        metric_label = config["label"]
        
        data_to_plot = []
        labels_for_plot = []
        boxprops_list = []

        for algo_name in algorithms_list:
            df_algo = all_runs_df[all_runs_df['algorithm'] == algo_name]
            if metric_key in ["path_distances", "path_lengths_nodes"]:
                df_algo_metric = df_algo[df_algo['success'] == True][metric_key].dropna()
            else: 
                df_algo_metric = df_algo[metric_key].dropna()
            
            if not df_algo_metric.empty:
                data_to_plot.append(df_algo_metric.tolist())
                labels_for_plot.append(algo_name)
                if algo_name == "Greedy BFS": boxprops_list.append(BOXPLOT_GBFS_PROPS)
                elif algo_name == "A* Search": boxprops_list.append(BOXPLOT_ASTAR_PROPS)
                else: boxprops_list.append({}) 
        
        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels_for_plot, patch_artist=True, vert=True, whis=1.5, showmeans=False)
            for i, patch in enumerate(bp['boxes']):
                props = boxprops_list[i] if i < len(boxprops_list) else {}
                patch.set_facecolor(props.get('boxprops', {}).get('facecolor', 'lightgray'))
                patch.set_edgecolor(props.get('color', 'black'))
                patch.set_linewidth(props.get('linewidth', 1))
            for median in bp['medians']: median.set_color('black')

        ax.set_ylabel(metric_label); ax.set_title(f"Distribution of {config['title']}")
        ax.grid(True, axis='y', linestyle=GRID_STYLE, alpha=GRID_ALPHA, zorder=0)
        if labels_for_plot: ax.set_xticklabels(labels_for_plot, rotation=0, ha='center')
        plot_idx += 1

    for i in range(plot_idx, len(axes)): fig.delaxes(axes[i])
    fig.suptitle("Metric Distributions (Box Plots)", fontsize=16, fontweight='bold', color=TEXT_COLOR_DARK)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def plot_scatter_correlations(all_runs_df, algorithms_list, scatter_config):
    num_scatters = len(scatter_config)
    if num_scatters == 0: return
    n_cols = min(2, num_scatters)
    n_rows = (num_scatters + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(7 * n_cols, 6 * n_rows), squeeze=False)
    axes = axes.flatten()
    plot_idx = 0
    
    algo_scatter_colors = {"Greedy BFS": SCATTER_GBFS_COLOR, "A* Search": SCATTER_ASTAR_COLOR}

    for config in scatter_config:
        if plot_idx >= len(axes): break
        ax = axes[plot_idx]
        x_key, y_key = config["x_key"], config["y_key"]
        x_label, y_label, title = config["x_label"], config["y_label"], config["title"]

        for algo_name in algorithms_list:
            df_algo = all_runs_df[all_runs_df['algorithm'] == algo_name]
            if x_key in ["path_distances", "path_lengths_nodes"] or y_key in ["path_distances", "path_lengths_nodes"]:
                df_to_plot = df_algo[df_algo['success'] == True]
            else:
                df_to_plot = df_algo
            
            if not df_to_plot.empty and x_key in df_to_plot and y_key in df_to_plot:
                ax.scatter(df_to_plot[x_key], df_to_plot[y_key], 
                           label=algo_name, alpha=0.6, s=30, 
                           color=algo_scatter_colors.get(algo_name, NODE_COLOR_DEFAULT),
                           edgecolors='w', linewidths=0.5)
        
        ax.set_xlabel(x_label); ax.set_ylabel(y_label); ax.set_title(title)
        ax.grid(True, linestyle=GRID_STYLE, alpha=GRID_ALPHA, zorder=0)
        ax.legend(fontsize=9)
        plot_idx += 1
        
    for i in range(plot_idx, len(axes)): fig.delaxes(axes[i])
    fig.suptitle("Metric Correlations (Scatter Plots)", fontsize=16, fontweight='bold', color=TEXT_COLOR_DARK)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def run_pathfinding_experiments(num_iterations_per_pair=10, num_node_pairs_if_random=3, specific_pairs=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    map_json_path = os.path.join(script_dir, '..', 'data', 'map.json')
    warehouse_data = load_json_data(map_json_path)
    if not warehouse_data: return None, None, None, None
    all_nodes_map, all_racks_map = warehouse_data.get("nodes"), warehouse_data.get("racks")
    if not all_nodes_map: print("E: 'nodes' key not found."); return None, None, None, None

    valid_nodes = [nid for nid,i in all_nodes_map.items() if not i.get("locked",False) and \
                   isinstance(i.get("x"),(int,float)) and isinstance(i.get("y"),(int,float)) and i.get("neighbours")]
    if len(valid_nodes) < 2: print("E: Not enough valid nodes for experiments."); return None, None, None, None

    node_pairs_to_test = []
    if specific_pairs:
        for sn, gn in specific_pairs:
            vp = True
            for nid_check, role in [(sn, "Start"), (gn, "Goal")]:
                if nid_check not in all_nodes_map: print(f"W: {role} '{nid_check}' pair({sn},{gn}) !in map. Skip."); vp=False; break
                if nid_check not in valid_nodes: print(f"W: {role} '{nid_check}' pair({sn},{gn}) invalid. Skip."); vp=False; break
            if not vp: continue
            if sn == gn: print(f"W: Start=Goal ({sn}). Skip."); continue
            node_pairs_to_test.append((sn,gn))
        if not node_pairs_to_test: print("W: No valid specific pairs. Trying random if allowed.");
    
    if not node_pairs_to_test and num_node_pairs_if_random > 0:
        print("Generating random pairs...")
        generated_set = set()
        for _ in range(num_node_pairs_if_random * 10): # Try more to get unique pairs
            if len(valid_nodes) < 2 or len(node_pairs_to_test) >= num_node_pairs_if_random: break
            try:
                s, g = random.sample(valid_nodes, 2)
                pair_tuple_sorted = tuple(sorted((s,g)))
                if pair_tuple_sorted not in generated_set:
                     node_pairs_to_test.append((s,g))
                     generated_set.add(pair_tuple_sorted)
            except ValueError: # Not enough unique items to sample
                print("W: Not enough unique valid nodes to sample for random pairs.")
                break
        if len(node_pairs_to_test) < num_node_pairs_if_random and num_node_pairs_if_random > 0 :
            print(f"W: Could only generate {len(node_pairs_to_test)} unique random pairs.")

    if not node_pairs_to_test: print("E: No node pairs to test. Exiting experiments."); return None, None, None, None
        
    algorithms = {"Greedy BFS": greedy_best_first_search, "A* Search": a_star_search}
    all_runs_data_list = [] 
    overall_stats = {name:{"runtimes_ms":[],"path_distances":[],"path_lengths_nodes":[],"nodes_explored":[],"successes":0,"failures":0} for name in algorithms}
    per_pair_details = {}

    print(f"\n--- Starting Pathfinding Experiments ---")
    print(f"Pairs to test: {len(node_pairs_to_test)}, Iterations/algo/pair: {num_iterations_per_pair}")

    for pair_idx, (start_node, goal_node) in enumerate(node_pairs_to_test):
        print(f"\nPair {pair_idx+1}/{len(node_pairs_to_test)}: {start_node} -> {goal_node}")
        pair_key = (start_node, goal_node); per_pair_details[pair_key] = {name:{} for name in algorithms}
        for algo_name, search_fn in algorithms.items():
            iter_runtimes, iter_dists, iter_lens, iter_expl, iter_succ = [],[],[],[],0 
            path_draw, explor_draw = None, None
            for i in range(num_iterations_per_pair):
                st_time = time.perf_counter()
                path, explor_set, path_len_n = search_fn(start_node,goal_node,all_nodes_map,manhattan_distance_heuristic)
                end_time = time.perf_counter(); runtime = (end_time-st_time)*1000
                
                run_entry = {"algorithm": algo_name, "pair_start": start_node, "pair_goal": goal_node,
                             "iteration": i, "runtimes_ms": runtime, "nodes_explored": len(explor_set),
                             "success": bool(path)}
                
                # Store ALL individual run data in overall_stats lists for later use in boxplots/scatter
                overall_stats[algo_name]["runtimes_ms"].append(runtime)
                overall_stats[algo_name]["nodes_explored"].append(len(explor_set))
                
                # For per-pair averaging (text table) and also to feed overall_stats for path metrics
                iter_runtimes.append(runtime); iter_expl.append(len(explor_set))

                if path:
                    overall_stats[algo_name]["successes"]+=1; iter_succ+=1
                    dist = calculate_path_distance(path,all_nodes_map)
                    overall_stats[algo_name]["path_distances"].append(dist) # For aggregate bar/box
                    overall_stats[algo_name]["path_lengths_nodes"].append(path_len_n) # For aggregate bar/box
                    iter_dists.append(dist); iter_lens.append(path_len_n)
                    if i==0: path_draw,explor_draw = path,explor_set
                    run_entry["path_distances"] = dist
                    run_entry["path_lengths_nodes"] = path_len_n
                else: 
                    overall_stats[algo_name]["failures"]+=1
                    # For scatter/box plots, it's better to have NaN for non-existent paths
                    run_entry["path_distances"] = float('nan') 
                    run_entry["path_lengths_nodes"] = float('nan')
                    # For overall_stats lists (used for averages in bar charts),
                    # we only append if successful. The mean will be correct for successful runs.
                
                all_runs_data_list.append(run_entry)
            
            per_pair_details[pair_key][algo_name] = {
                "runtime_avg_ms":np.mean(iter_runtimes) if iter_runtimes else float('nan'),
                "distance_avg":np.mean(iter_dists) if iter_dists else float('nan'), # Avg of successful for this pair
                "path_len_avg":np.mean(iter_lens) if iter_lens else float('nan'), # Avg of successful for this pair
                "nodes_explored_avg":np.mean(iter_expl) if iter_expl else float('nan'),
                "success_rate":(iter_succ/num_iterations_per_pair)*100 if num_iterations_per_pair>0 else 0,
                "path_example":path_draw, "explored_example":explor_draw
            }
    
    all_runs_df = pd.DataFrame(all_runs_data_list) if all_runs_data_list else pd.DataFrame()

    # --- Text-based Statistical Reporting ---
    print("\n\n" + "="*30 + " AGGREGATE EXPERIMENT STATISTICS (TEXT) " + "="*30)
    for algo_name, stats_dict in overall_stats.items(): # Renamed 'stats' to 'stats_dict'
        print(f"\nAlgorithm: {algo_name}")
        total_att = stats_dict["successes"]+stats_dict["failures"]
        if total_att == 0: print("  No runs."); continue
        succ_rate=(stats_dict["successes"]/total_att)*100 if total_att>0 else 0
        print(f"  Success: {succ_rate:.2f}% ({stats_dict['successes']}S / {stats_dict['failures']}F of {total_att})")
        for mkey,mlabel in [("runtimes_ms","Avg Runtime (ms)"),("path_distances","Avg Path Dist."),
                            ("path_lengths_nodes","Avg Path Len (N)"),("nodes_explored","Avg N.Explored")]:
            vals = stats_dict[mkey] 
            avg = np.mean(vals) if vals else float('nan')
            std = np.std(vals) if vals else float('nan')
            if mkey in ["path_distances", "path_lengths_nodes"] and not stats_dict["successes"]:
                 print(f"  {mlabel}: N/A (no successful paths for this metric)")
            else:
                 print(f"  {mlabel}: {avg:.2f} ( {std:.2f})")

    print("\n\n" + "="*30 + " DETAILED PER-PAIR COMPARISON (TEXT) " + "="*30)
    hdr="{:<18} | {:<12} | {:<12} | {:<8} | {:<10} | {:<12} | {:<10}".format("Pair (S->G)","Algorithm","Runtime(ms)","Dist.","PathLen","N.Explored","Success%")
    print(hdr); print("-"*len(hdr))
    for pkey, adata in per_pair_details.items():
        sn,gn = pkey; pstr = f"{sn[:7]}->{gn[:7]}"
        first=True
        for aname_prn in algorithms.keys():
            res = adata.get(aname_prn,{})
            print("{:<18} | {:<12} | {:<12.2f} | {:<8.1f} | {:<10.1f} | {:<12.1f} | {:<10.1f}".format(
                pstr if first else "", aname_prn, res.get('runtime_avg_ms',float('nan')), 
                res.get('distance_avg',float('nan')), res.get('path_len_avg',float('nan')),
                res.get('nodes_explored_avg',float('nan')), res.get('success_rate',0.0)))
            first=False
        print("-"*len(hdr))

    # --- Visual Statistical Plotting ---
    if not all_runs_df.empty:
        # Bar charts use overall_stats (which has lists of ALL runs for each metric per algo)
        plot_bar_charts_with_errors(overall_stats, list(algorithms.keys())) 
        
        metrics_for_box_and_scatter = {
            "runtimes_ms": {"label": "Runtime (ms)", "title": "Runtime"},
            "path_distances": {"label": "Path Distance (Cost)", "title": "Path Distance"},
            "path_lengths_nodes": {"label": "Path Length (Nodes)", "title": "Path Length"},
            "nodes_explored": {"label": "Nodes Explored", "title": "Nodes Explored"}
        }
        # Box plots and Scatter plots use all_runs_df for detailed distributions
        plot_box_plots_for_metrics(all_runs_df, list(algorithms.keys()), metrics_for_box_and_scatter)
        
        scatter_pairs_config = [
            {"x_key": "nodes_explored", "y_key": "path_lengths_nodes", "x_label": "Nodes Explored", 
             "y_label": "Path Length (Nodes)", "title": "Nodes Explored vs. Path Length"},
            {"x_key": "nodes_explored", "y_key": "runtimes_ms", "x_label": "Nodes Explored", 
             "y_label": "Runtime (ms)", "title": "Nodes Explored vs. Runtime"},
        ]
        plot_scatter_correlations(all_runs_df, list(algorithms.keys()), scatter_pairs_config)

    # --- Plotting one map example ---
    if node_pairs_to_test and per_pair_details: # Check if any pairs were actually tested and details exist
        # Find the last pair that actually has data in per_pair_details
        last_pair_with_data = None
        for p_key_rev in reversed(node_pairs_to_test):
            if p_key_rev in per_pair_details and per_pair_details[p_key_rev]:
                last_pair_with_data = p_key_rev
                break
        
        if last_pair_with_data:
            last_pdata = per_pair_details[last_pair_with_data]
            s_n,g_n = last_pair_with_data
            print(f"\n--- Plotting Map Example for Last Processed Pair with Data: {s_n} -> {g_n} ---")
            for aname_plot,pdata in last_pdata.items():
                path_ex,expl_ex = pdata.get("path_example"),pdata.get("explored_example")
                # For title, use the per-pair average for consistency if available, else use example run details
                dist_v = pdata.get('distance_avg', (calculate_path_distance(path_ex, all_nodes_map) if path_ex else float('nan')))
                nodes_p = len(path_ex if path_ex else [])
                nodes_e = len(expl_ex if expl_ex else [])
                if path_ex: # Only plot if there's an example path
                    ptitle=f"{aname_plot}: {s_n} to {g_n}\nDist:{dist_v:.1f}, PathN:{nodes_p}, ExplN:{nodes_e}"
                    print(f"  Plotting map for {aname_plot}...")
                    draw_warehouse_path(all_nodes_map,all_racks_map,s_n,g_n,path_ex,expl_ex,title=ptitle, algo_name=aname_plot)
                else: print(f"  Skip map plot for {aname_plot} (no path in example for {s_n}->{g_n}).")
        else:
            print("\nNo data in per_pair_details for any tested pairs to plot map example.")
    else: print("\nNo pairs tested, or no per_pair_details, so no map example plots.")
    
    return overall_stats, per_pair_details, node_pairs_to_test, list(algorithms.keys())

if __name__ == "__main__":
    # CRITICAL: Update with ACTUAL VALID, UNLOCKED node IDs from YOUR map.json
    # The list should contain tuples: (start_node_id, goal_node_id)
    specific_test_pairs = [
        ("E1-2", "N10-13"), # This pair worked in your previous output
        # ("E1-1", "N30-25"), # This pair FAILED in your previous output. INVESTIGATE or REMOVE.
                            # Possible reasons: N30-25 doesn't exist, is locked, has no coords/neighbours,
                            # or is genuinely unreachable from E1-1.
        # Add 1-3 MORE KNOWN VALID and DIVERSE pairs from YOUR map.
        # For example:
        # ("YOUR_VALID_START_1", "YOUR_VALID_GOAL_1"),
        # ("YOUR_VALID_START_2", "YOUR_VALID_GOAL_2"),
    ]
    
    # If specific_test_pairs is empty, script will try to generate random pairs.
    # Set specific_pairs_to_run to None to FORCE random pairs.
    specific_pairs_to_run = specific_test_pairs 
    num_random_pairs_to_generate = 2 # Fallback if specific_test_pairs is empty or all invalid. Make it at least 1.

    if not specific_pairs_to_run: 
        print("No specific pairs provided or list is empty. Will attempt to use random pairs.")
        specific_pairs_to_run = None 
    
    results = run_pathfinding_experiments(
        num_iterations_per_pair=10, # Number of times each algo runs on the same S-G pair
        num_node_pairs_if_random=num_random_pairs_to_generate,
        specific_pairs=specific_pairs_to_run
    )

    if results and results[0]: # Check if experiments ran and returned stats
        print("\nPathfinding experiments completed. Check plots and console output.")
    else:
        print("\nPathfinding experiments did not complete successfully or no data was generated.")


    # ---------------------------------------------------------------------------
    # --- GUIDE TO VISUAL ANALYSIS, STATISTICAL INTERPRETATION, AND CONCLUSIONS ---
    # ---------------------------------------------------------------------------
    print("\n\n" + "="*70)
    print("GUIDE TO ANALYSIS, INTERPRETATION, AND CONCLUSIONS")
    print("="*70)
