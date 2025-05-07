import json

LOOKUP_TABLE_PATH = "data/lookup_table.json"  # Adjust the file path as needed

def load_json_file(file_path):
    """ Load data from a JSON file. """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return {}

def save_json_file(file_path, data):
    """ Save data to a JSON file. """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error: Could not save JSON to {file_path}. {e}")

def update_lookup_table_with_sa_output(sa_output):
    """ Update the lookup table with the output from Simulated Annealing. """
    lookup_table = load_json_file(LOOKUP_TABLE_PATH)
    
    for task_id, goal_node in sa_output:
        lookup_table[task_id] = {"goal_node": goal_node}
        
    save_json_file(LOOKUP_TABLE_PATH, lookup_table)

def get_goal_node_from_lookup(item_or_task_id, lookup_table_content):
    """ Retrieve the goal node for a specific task or item ID. """
    item_data = lookup_table_content.get(item_or_task_id)
    if item_data and "goal_node" in item_data:
        return item_data["goal_node"]
    print(f"Warning: Item or task ID '{item_or_task_id}' not found or missing 'goal_node' in lookup table.")
    return None
