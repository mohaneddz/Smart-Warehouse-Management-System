import math
import heapq
import random
import copy
import time
import sys # Added for exit

# --- Database Library ---
try:
    import psycopg2
except ImportError:
    print("Error: The 'psycopg2' library is required but not found.")
    print("Please install it using: pip install psycopg2-binary")
    sys.exit(1) # Exit if database library is missing


# --- Database Connection Details ---
# !! IMPORTANT: Replace 'YOUR_SECRET_PASSWORD' with your actual database password !!
# !!           Consider using environment variables or a secrets manager for production !!
DB_CONFIG = {
    'host': 'db.jdmhigzuckvnpxcqpaho.supabase.co',
    'port': '5432',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'ensia02'
}

# --- Assumed Table and Column Names ---
# !! IMPORTANT: Change these if your table/columns are named differently !!
RACK_TABLE_NAME = 'racks'
X_COLUMN_NAME = 'x_coordinate'
Y_COLUMN_NAME = 'y_coordinate'


# --- Constants ---
FREE_SPACE = 0
OBSTACLE = 1
RACK = 2
AGENT = 3
TARGET_RACK_MARKER = 4

# --- Warehouse Grid Representation ---
class WarehouseGrid:
    def __init__(self, width, height, obstacles, racks):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles) # Use sets for O(1) lookups
        self.racks = set(racks)         # Use sets for O(1) lookups

    def is_valid(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def is_obstacle(self, pos):
        return pos in self.obstacles

    def is_rack(self, pos):
        return pos in self.racks

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if self.is_valid((nx, ny)):
                neighbors.append((nx, ny))
        return neighbors

# --- Database Interaction ---
def fetch_potential_racks_from_db():
    """
    Connects to the PostgreSQL database and fetches rack locations.

    Returns:
        A list of (x, y) tuples representing rack coordinates,
        or an empty list if fetching fails.
    """
    print(f"Connecting to database '{DB_CONFIG['database']}' on {DB_CONFIG['host']}...")
    conn = None
    rack_locations = []
    sql = f"SELECT {X_COLUMN_NAME}, {Y_COLUMN_NAME} FROM {RACK_TABLE_NAME};"

    if DB_CONFIG['password'] == 'YOUR_SECRET_PASSWORD':
         print("\n*** WARNING: Database password is not set in the script! ***")
         print("*** Please replace 'YOUR_SECRET_PASSWORD' with your actual password. ***\n")
         # Depending on policy, you might want to exit here or continue cautiously
         # return [] # Optionally stop if password isn't set

    try:
        # Establish connection
        conn = psycopg2.connect(**DB_CONFIG)
        print("Database connection successful.")

        # Create a cursor
        cur = conn.cursor()

        # Execute the query
        print(f"Executing query: {sql}")
        cur.execute(sql)

        # Fetch all results
        results = cur.fetchall() # Returns a list of tuples, e.g., [(1, 5), (10, 2)]

        # Process results (assuming columns are returned in the order x, y)
        for row in results:
            try:
                # Ensure coordinates are integers
                x = int(row[0])
                y = int(row[1])
                rack_locations.append((x, y))
            except (TypeError, ValueError, IndexError) as e:
                 print(f"Warning: Skipping row {row}. Could not parse coordinates: {e}")


        print(f"Fetched {len(rack_locations)} rack locations from the database.")

        # Close the cursor
        cur.close()

    except psycopg2.OperationalError as e:
        print(f"\n--- Database Connection Error ---")
        print(f"Could not connect to the database: {e}")
        print("Troubleshooting steps:")
        print(f" 1. Verify the host ('{DB_CONFIG['host']}') and port ('{DB_CONFIG['port']}').")
        print(f" 2. Ensure the database ('{DB_CONFIG['database']}') exists.")
        print(f" 3. Check if the user ('{DB_CONFIG['user']}') has connection permissions.")
        print(f" 4. Double-check the password (is it correct in the script?).")
        print(f" 5. Make sure the database server is running and accessible from your network.")
        print(f" 6. Check Supabase project status and networking/firewall rules.")
        print("-------------------------------\n")
        return [] # Return empty list on connection failure

    except psycopg2.Error as e:
        # Handle other potential database errors (like table not found, syntax error)
        print(f"\n--- Database Query Error ---")
        print(f"An error occurred while querying the database: {e}")
        print(f"Query attempted: {sql}")
        print("Troubleshooting steps:")
        print(f" 1. Verify the table name ('{RACK_TABLE_NAME}') is correct.")
        print(f" 2. Verify the column names ('{X_COLUMN_NAME}', '{Y_COLUMN_NAME}') are correct.")
        print(f" 3. Check if the table '{RACK_TABLE_NAME}' exists in the '{DB_CONFIG['database']}' database.")
        print(f" 4. Ensure the user '{DB_CONFIG['user']}' has SELECT permissions on the table.")
        print("----------------------------\n")

        return [] # Return empty list on query failure

    finally:
        # Ensure the connection is closed even if errors occurred
        if conn:
            conn.close()
            print("Database connection closed.")

    return rack_locations


# --- Simulated Annealing (Simplified Example - unchanged) ---
def simulated_annealing_select_target(agent_start_pos, potential_targets):
    print(f"Running Simplified Simulated Annealing for agent at {agent_start_pos}...")
    if not potential_targets:
        print("SA: No potential targets provided.")
        return None
    initial_temp = 100.0
    cooling_rate = 0.95
    min_temp = 0.1
    iterations_per_temp = 10
    def cost(rack_pos):
        return euclidean_distance(agent_start_pos, rack_pos)
    current_solution = random.choice(potential_targets)
    current_cost = cost(current_solution)
    best_solution = current_solution
    best_cost = current_cost
    temp = initial_temp
    while temp > min_temp:
        for _ in range(iterations_per_temp):
             if len(potential_targets) <= 1: break
             neighbor_solution = random.choice([t for t in potential_targets if t != current_solution])
             neighbor_cost = cost(neighbor_solution)
             cost_diff = neighbor_cost - current_cost
             if cost_diff < 0 or random.uniform(0, 1) < math.exp(-cost_diff / temp):
                 current_solution = neighbor_solution
                 current_cost = neighbor_cost
                 if current_cost < best_cost:
                     best_solution = current_solution
                     best_cost = current_cost
        temp *= cooling_rate
        if len(potential_targets) <= 1: break
    print(f"SA Result: Selected target {best_solution} (Cost: {best_cost:.2f})")
    return best_solution

# --- Heuristic Function (unchanged) ---
def euclidean_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# --- Greedy Best-First Search Implementation (unchanged) ---
def greedy_best_first_search(warehouse, start, goal, other_agent_positions):
    print(f"Starting Greedy Search from {start} to {goal}...")
    if start == goal: return [start]
    if not warehouse.is_valid(start) or not warehouse.is_valid(goal): return None
    if warehouse.is_obstacle(start) or warehouse.is_obstacle(goal): return None

    priority_queue = [(euclidean_distance(start, goal), start)]
    heapq.heapify(priority_queue)
    came_from = {start: None}
    visited = {start}

    while priority_queue:
        current_heuristic, current_pos = heapq.heappop(priority_queue)
        if current_pos == goal:
            print("Goal reached!")
            return reconstruct_path(came_from, goal)

        for neighbor_pos in warehouse.get_neighbors(current_pos):
            if neighbor_pos not in visited:
                valid_move = True
                if warehouse.is_obstacle(neighbor_pos): valid_move = False
                elif warehouse.is_rack(neighbor_pos) and neighbor_pos != goal: valid_move = False
                elif neighbor_pos in other_agent_positions:
                    print(f"  Conflict Warning: Neighbor {neighbor_pos} occupied (basic check). Skipping.")
                    valid_move = False
                if valid_move:
                    visited.add(neighbor_pos)
                    came_from[neighbor_pos] = current_pos
                    priority = euclidean_distance(neighbor_pos, goal)
                    heapq.heappush(priority_queue, (priority, neighbor_pos))
    print(f"No path found from {start} to {goal}.")
    return None

# --- Path Reconstruction (unchanged) ---
def reconstruct_path(came_from, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path

# --- Main Simulation (modified slightly to use DB-fetched racks) ---
if __name__ == "__main__":
    # --- Fetch Racks First ---
    # This now connects to your actual database
    db_rack_locations = fetch_potential_racks_from_db()

    if not db_rack_locations:
        print("\nFailed to fetch rack locations from the database. Cannot proceed.")
        print("Please check database connection details, credentials, table/column names, and error messages above.")
        sys.exit(1)

    # --- Warehouse Setup ---
    # Dimensions might need adjustment based on your coordinate system
    # Or calculate dynamically based on max X/Y from db_rack_locations
    WIDTH = 30 # Adjust if needed
    HEIGHT = 20 # Adjust if needed

    # Define Obstacles (keep your static obstacles)
    OBSTACLES = [
        (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
        (7, 0), (7, 1), (7, 2), (7, 3),
        (12, 5), (12, 6), (12, 7), (12, 8), (12, 9)
        # Add any other known static obstacles
    ]

    # Create Warehouse using fetched rack locations
    warehouse = WarehouseGrid(WIDTH, HEIGHT, OBSTACLES, db_rack_locations)
    print(f"\nWarehouse grid initialized with {len(warehouse.racks)} racks from DB and {len(warehouse.obstacles)} static obstacles.")


    # --- Agent Setup (same as before) ---
    agents = {
        "Agent_1": {"start_pos": (0, 0), "current_pos": (0, 0), "path": None, "target": None},
        "Agent_2": {"start_pos": (0, 19), "current_pos": (0, 19), "path": None, "target": None}, # Adjusted start pos
        "Agent_3": {"start_pos": (29, 0), "current_pos": (29, 0), "path": None, "target": None}, # Adjusted start pos
    }

    # --- Simulation Steps ---

    # 1. Potential targets are now the ones fetched from DB
    potential_targets = list(warehouse.racks) # Use the validated list from the grid object

    # 2. Assign targets using SA and find paths using Greedy Search for each agent
    agent_targets = {}
    agent_paths = {}

    all_current_agent_positions = set(details["current_pos"] for details in agents.values())

    for agent_id, agent_data in agents.items():
        print(f"\n--- Planning for {agent_id} ---")
        start_pos = agent_data["current_pos"]
        available_targets = [t for t in potential_targets if t not in agent_targets.values()]

        if not available_targets:
            print(f"No available targets left for {agent_id}.")
            continue # Skip if no targets remain

        target_rack = simulated_annealing_select_target(start_pos, available_targets)

        if target_rack:
            agent_data["target"] = target_rack
            agent_targets[agent_id] = target_rack
            other_agents_pos = all_current_agent_positions - {start_pos}
            path = greedy_best_first_search(warehouse, start_pos, target_rack, other_agents_pos)
            agent_data["path"] = path

            if path:
                print(f"Path found for {agent_id} to {target_rack}: {path}")
            else:
                print(f"Could not find a path for {agent_id} to {target_rack}.")
                agent_targets.pop(agent_id, None)
                agent_data["target"] = None
        else:
            print(f"No suitable target found or assigned for {agent_id}.")
            agent_data["path"] = None
            agent_data["target"] = None

    # --- Print Final State ---
    print("\n--- Simulation Complete ---")
    for agent_id, agent_data in agents.items():
        print(f"{agent_id}: Start={agent_data['start_pos']}, Current={agent_data['current_pos']}, Target={agent_data['target']}, Path Found={agent_data['path'] is not None}")
        if agent_data['path']:
             print(f"  Path: {agent_data['path'][:10]}..." if len(agent_data['path']) > 10 else f"  Path: {agent_data['path']}")