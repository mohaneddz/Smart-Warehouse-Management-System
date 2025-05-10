import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy
import json
import csv
import random
import math
import pandas as pd

# --- CONFIGURATION & CONSTANTS ---
### MODIFICATION NOTE: Keeping these global constants as is. A student might define them here
### for clarity and easy access, even if some could later be refactored into classes.
MAX_SLOTS_PER_SHELF = 5
SHELF_LEVELS = 3
HEAVY_ITEM_THRESHOLD = 20
DISTANCE_BASE_FACTOR = 0.1
FREQUENCY_DISTANCE_MULTIPLIER = 5.0
MAX_DISTANCE_SCORE_CONTRIBUTION = 5.0

COMPATIBILITY_MATRIX = {
    'food':           {'food': 1.0, 'beverages': 0.8, 'household goods': 0.2, 'chemicals': 0.0, 'frozen': 0.1},
    'beverages':      {'food': 0.8, 'beverages': 1.0, 'household goods': 0.3, 'chemicals': 0.0, 'frozen': 0.1},
    'household goods':{'food': 0.2, 'beverages': 0.3, 'household goods': 1.0, 'chemicals': 0.1, 'frozen': 0.05},
    'chemicals':      {'food': 0.0, 'beverages': 0.0, 'household goods': 0.1, 'chemicals': 1.0, 'frozen': 0.0},
    'frozen':         {'food': 0.1, 'beverages': 0.1, 'household goods': 0.05, 'chemicals': 0.0, 'frozen': 1.0},
}
CATEGORY_COLORS = {
    'food': 'lightgreen', 'beverages': 'lightblue', 'household goods': 'lightcoral',
    'chemicals': 'gold', 'frozen': 'lightcyan', 'default': 'lightgrey'
}

# These will be loaded from facts.json
ENTRANCE_COORDS_MAIN = None
ENTRANCE_COORDS_FROZEN = None
MAX_WEIGHT_PER_SHELF_LEVEL = None
SHELF_MAX_HEIGHT_PER_LEVEL = None # Not heavily used yet, but good to have for later.

# --- DATA GENERATION FUNCTIONS ---
# Helper functions to create some sample data if we don't have real files.

def generate_dummy_item_csv(filename="dummy_items.csv", num_items=30):
    """
    Creates a dummy CSV file for items.
    Helpful for testing without needing real data.
    """
    categories = list(COMPATIBILITY_MATRIX.keys())
    items_data = [] # Using a list to build up rows, then write all at once.
    for i in range(num_items):
        item_id = f"item{str(i+1).zfill(3)}"
        category = random.choice(categories)
        name = f"{random.choice(['Premium', 'Value', 'Eco'])} {category.capitalize()} {random.choice(['Pack', 'Unit', 'Box'])}"
        weight = round(random.uniform(1, 75), 1)
        slots = random.randint(1, 3)
        retrieval_counter = random.randint(0, 100) # How often it's picked.
        insertion_counter = random.randint(1, 20)  # How often it's put away.
        items_data.append([item_id, name, weight, category, slots, retrieval_counter, insertion_counter])
    
    # Writing to CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'name', 'weight', 'category', 'slots_required', 'retrieval_counter', 'insertion_counter'])
        writer.writerows(items_data)
    print(f"Generated {filename} with {len(items_data)} items (incl. counters).")

def generate_dummy_rack_layout_csv(filename="dummy_rack_layout.csv", rack_ids=None, item_ids_for_layout=None):
    """
    Creates a dummy CSV for an initial (sparse) rack layout.
    So the warehouse isn't completely empty at the start.
    """
    if rack_ids is None: rack_ids = [f"R{str(i+1).zfill(2)}" for i in range(8)]
    if item_ids_for_layout is None:
        try: # Try to get item IDs from the items file if it exists
            temp_df = pd.read_csv("dummy_items.csv")
            item_ids_for_layout = list(temp_df['id'])
        except FileNotFoundError: # If file not found, make some up.
            print("dummy_items.csv not found for layout generation, creating generic item IDs.")
            item_ids_for_layout = [f"item{str(i+1).zfill(3)}" for i in range(30)]
        except Exception as e: # Catch other potential errors during pandas read
            print(f"Error reading dummy_items.csv for layout gen: {e}, creating generic item IDs.")
            item_ids_for_layout = [f"item{str(i+1).zfill(3)}" for i in range(30)]


    layout_data = []
    item_slots_map = {} # To quickly find how many slots an item needs.
    try:
        df_items = pd.read_csv("dummy_items.csv")
        # Create a dictionary mapping: item_id -> slots_required
        for index, row in df_items.iterrows():
            item_slots_map[row['id']] = row['slots_required']
        ### MODIFICATION NOTE: Changed from zip to explicit loop for item_slots_map.
        ### A newer Python user might write it this way first for clarity.
    except Exception:
        # If we can't read item slots, it's not fatal for dummy generation,
        # we'll use random slots later.
        pass

    for rack_id in rack_ids:
        for shelf_level in range(SHELF_LEVELS):
            # Let's not fill every shelf initially.
            num_items_on_shelf = random.randint(0,1) # Max 1 item per shelf for sparse layout
            current_slots_occupied_on_shelf = 0
            items_placed_on_this_shelf = 0
            
            # Make a copy and shuffle to pick items randomly for this shelf
            shuffled_item_ids_to_pick_from = random.sample(item_ids_for_layout, len(item_ids_for_layout))

            for item_id in shuffled_item_ids_to_pick_from:
                if items_placed_on_this_shelf >= num_items_on_shelf:
                    break # Already placed enough items on this shelf.

                # How many slots does this item need? Get from map or use random.
                slots_needed_for_this_item = item_slots_map.get(item_id, random.randint(1,2))

                if current_slots_occupied_on_shelf + slots_needed_for_this_item <= MAX_SLOTS_PER_SHELF:
                    layout_data.append([rack_id, shelf_level, item_id])
                    current_slots_occupied_on_shelf += slots_needed_for_this_item
                    items_placed_on_this_shelf +=1
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['rack_id', 'shelf_level', 'item_id'])
        writer.writerows(layout_data)
    print(f"Generated {filename} with initial layout.")


# --- HELPER FUNCTIONS ---
def euclidean_distance(p1, p2):
    """Calculates standard Euclidean distance. Needed for scoring based on proximity."""
    if p1 is None or p2 is None:
        # This can happen if coordinates are not set, so distance is effectively infinite.
        return float('inf')
    # Standard formula: sqrt((x2-x1)^2 + (y2-y1)^2)
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# --- CLASSES ---
### MODIFICATION NOTE: Keeping class structure as is - it's good.
### Adding slightly more "student-like" docstrings.

class ItemPlacementData:
    """Stores info about one item, like its weight, category, etc."""
    def __init__(self, item_id, name, weight, category, slots_required, retrieval_counter=0, insertion_counter=1):
        self.item_id = item_id
        self.name = name
        self.weight = float(weight) # Make sure weight is a number
        self.category = category
        self.slots_required = int(slots_required) # Slots should be an integer
        self.retrieval_counter = int(retrieval_counter)
        # Insertion counter should be at least 1 to avoid division by zero for frequency
        self.insertion_counter = max(1, int(insertion_counter))
        self.is_frozen = (category == 'frozen') # Quick check if it's a frozen item

    @property
    def frequency_metric(self):
        """A simple metric for how often an item is picked vs stocked."""
        # This tells us if an item is "popular".
        return self.retrieval_counter / self.insertion_counter

    def __repr__(self):
        # This is just for printing the item info nicely for debugging.
        return f"ItemData({self.item_id},'{self.name}',W:{self.weight},S:{self.slots_required},Fq:{self.frequency_metric:.2f})"

class ShelfState:
    """Represents one shelf on a rack and what's on it."""
    def __init__(self, shelf_level_index, max_slots=MAX_SLOTS_PER_SHELF):
        self.shelf_level_index = shelf_level_index # e.g., 0 for bottom, 1 for middle...
        self.max_slots = max_slots
        self.items_on_shelf = [] # A list to hold ItemPlacementData objects
        self.occupied_slots = 0
        self.current_weight_on_shelf = 0.0

    @property
    def available_slots(self):
        """How many slots are still free on this shelf?"""
        return self.max_slots - self.occupied_slots

    def can_add_item(self, item_data: ItemPlacementData, max_weight_for_this_level: float):
        """Checks if an item *can* be added (space and weight)."""
        if self.available_slots < item_data.slots_required:
            return False, "slot_capacity" # Reason: not enough slots
        if self.current_weight_on_shelf + item_data.weight > max_weight_for_this_level:
            return False, "weight_limit" # Reason: too heavy for this shelf
        return True, "ok" # Looks good, can be added

    def add_item(self, item_data: ItemPlacementData, max_weight_for_this_level: float):
        """Actually adds the item to the shelf if it's possible."""
        can_add_flag, _reason = self.can_add_item(item_data, max_weight_for_this_level)
        if can_add_flag:
            self.items_on_shelf.append(item_data)
            self.occupied_slots += item_data.slots_required
            self.current_weight_on_shelf += item_data.weight
            return True
        return False # Could not add item

    def __repr__(self):
        return f"ShelfState(L{self.shelf_level_index},{self.occupied_slots}/{self.max_slots}s,{self.current_weight_on_shelf:.1f}kg)"

class RackState:
    """Represents a whole rack, which has multiple shelves."""
    def __init__(self, rack_id_str, is_rack_frozen=False, rack_center_coords=None):
        self.rack_id_str = rack_id_str
        self.is_rack_frozen = is_rack_frozen # Is this a special rack for frozen stuff?
        self.rack_center_coords = tuple(rack_center_coords) if rack_center_coords else (0,0) # Where is it?
        # Create all the shelves for this rack
        self.shelf_states = []
        for i in range(SHELF_LEVELS):
            self.shelf_states.append(ShelfState(shelf_level_index=i))
        ### MODIFICATION NOTE: Changed list comprehension for shelf_states to an explicit loop.
        ### A student newer to Python might write it this way first.

    def get_shelf_state(self, shelf_level_index):
        """Gets a specific shelf from this rack by its level index."""
        if 0 <= shelf_level_index < SHELF_LEVELS:
            return self.shelf_states[shelf_level_index]
        else:
            # print(f"Warning: Tried to get invalid shelf level {shelf_level_index} from rack {self.rack_id_str}")
            return None # Invalid shelf level

    def __repr__(self):
        return f"RackState({self.rack_id_str},Frozen:{self.is_rack_frozen},Center:{self.rack_center_coords})"

class WarehousePlacementSystem:
    """
    The main class that manages the warehouse, items, and finding spots.
    This is where most of the "AI" logic for placement scoring happens.
    """
    def __init__(self, facts_json_file="facts.json"):
        self.rack_states_map = {} # Stores all RackState objects, like a database of racks
        self.item_database = {}   # Stores all ItemPlacementData objects
        self.main_entrance_coords = None
        self.frozen_区域_entrance_coords = None # "区域" means area/zone - good to remember!
        self.max_weight_config_per_level = None
        self.shelf_max_height_config_per_level = None # Might use this later for item height checks
        self._load_configuration_from_facts(facts_json_file) # Load settings from the JSON file

    def _load_configuration_from_facts(self, facts_json_file):
        """Loads important settings from the facts.json file."""
        ### MODIFICATION NOTE: Keeping the global variable assignments here.
        ### A student might do this thinking it makes them accessible everywhere,
        ### or if they learned to set module-level configs this way.
        global ENTRANCE_COORDS_MAIN, ENTRANCE_COORDS_FROZEN, MAX_WEIGHT_PER_SHELF_LEVEL, SHELF_MAX_HEIGHT_PER_LEVEL
        try:
            with open(facts_json_file, 'r') as f:
                facts_data = json.load(f)
            
            self.main_entrance_coords = ENTRANCE_COORDS_MAIN = tuple(facts_data["entrance_coords"])
            self.frozen_区域_entrance_coords = ENTRANCE_COORDS_FROZEN = tuple(facts_data["frozen_entrance_coords"])
            self.max_weight_config_per_level = MAX_WEIGHT_PER_SHELF_LEVEL = facts_data["max_weight_per_level"]
            self.shelf_max_height_config_per_level = SHELF_MAX_HEIGHT_PER_LEVEL = facts_data["shelfs_max_height"]

            # Create RackState objects based on the info in facts.json
            racks_info_from_file = facts_data.get("racks_info", {}) # Use .get for safety
            for rack_id_str, rack_specific_info in racks_info_from_file.items():
                is_frozen_rack = rack_specific_info.get("is_frozen", False)
                center_coords_for_rack = rack_specific_info.get("center_coords")
                self.rack_states_map[rack_id_str] = RackState(rack_id_str, is_frozen_rack, center_coords_for_rack)
        except FileNotFoundError:
            print(f"FATAL: Configuration file '{facts_json_file}' not found. Cannot continue.")
            exit()
        except KeyError as e:
            print(f"FATAL: Missing key {e} in configuration file '{facts_json_file}'. Cannot continue.")
            exit()
        except Exception as e: # Catch any other unexpected errors
            print(f"FATAL: Error loading configuration from '{facts_json_file}': {e}. Cannot continue.")
            exit()

    def load_item_properties_from_csv(self, items_csv_file="dummy_items.csv"):
        """Loads all the item details from the items CSV file."""
        try:
            df_items = pd.read_csv(items_csv_file)
            for _index, row_data in df_items.iterrows(): # _index to show we don't need the pandas index here
                # Store item properties as a dictionary in our item_database
                self.item_database[row_data['id']] = {
                    'name': row_data['name'],
                    'weight': float(row_data['weight']),
                    'category': row_data['category'],
                    'slots_required': int(row_data['slots_required']),
                    'retrieval_counter': int(row_data['retrieval_counter']),
                    'insertion_counter': int(row_data['insertion_counter'])
                }
        except FileNotFoundError:
            print(f"Error: Item properties file '{items_csv_file}' not found. No items loaded into database.")
        except Exception as e:
            print(f"Error loading item properties from '{items_csv_file}': {e}")

    def _get_item_placement_data_by_id(self, item_id_str: str) -> ItemPlacementData | None:
        """Helper to get an ItemPlacementData object for a given item ID."""
        item_props = self.item_database.get(item_id_str)
        if item_props:
            # Use dictionary unpacking to pass properties to constructor
            return ItemPlacementData(item_id_str, **item_props)
        else:
            # print(f"Warning: Item ID '{item_id_str}' not found in database.")
            return None

    def initialize_layout_from_csv(self, layout_csv_file="dummy_rack_layout.csv"):
        """Sets up the initial state of the warehouse based on a layout file."""
        if not self.max_weight_config_per_level:
            print("Warning: Max weight configuration not loaded. Cannot safely initialize layout from CSV.")
            return
        try:
            df_layout = pd.read_csv(layout_csv_file)
            items_added_count = 0
            for _index, layout_row in df_layout.iterrows():
                rack_id_str = layout_row['rack_id']
                shelf_level_idx = int(layout_row['shelf_level'])
                item_id_str = layout_row['item_id']

                if rack_id_str in self.rack_states_map:
                    rack = self.rack_states_map[rack_id_str]
                    shelf = rack.get_shelf_state(shelf_level_idx)
                    if shelf:
                        item_to_place = self._get_item_placement_data_by_id(item_id_str)
                        if item_to_place:
                            # Basic check for frozen items in non-frozen racks or vice-versa if shelf is occupied
                            valid_frozen_placement = True
                            if item_to_place.is_frozen and not rack.is_rack_frozen:
                                valid_frozen_placement = False
                            if not item_to_place.is_frozen and rack.is_rack_frozen and shelf.items_on_shelf:
                                # Don't put non-frozen with existing items in a frozen rack's shelf
                                valid_frozen_placement = False
                            
                            if valid_frozen_placement:
                                if shelf.add_item(item_to_place, self.max_weight_config_per_level[shelf_level_idx]):
                                    items_added_count += 1
                                # else:
                                    # print(f"Could not add {item_id_str} to {rack_id_str}-L{shelf_level_idx} during init (slots/weight).")
                            # else:
                                # print(f"Invalid frozen placement for {item_id_str} at {rack_id_str}-L{shelf_level_idx} during init.")
        except FileNotFoundError:
            print(f"Error: Layout file '{layout_csv_file}' not found. Initial layout not loaded.")
        except Exception as e:
            print(f"Error initializing layout from '{layout_csv_file}': {e}")

    def evaluate_potential_placement(self, item_to_place: ItemPlacementData, rack: RackState, shelf: ShelfState):
        """
        This is the core 'scoring' function. It decides how good a spot is.
        It's like the evaluation function in local search, but we use it to pick the
        best initial placement for one item, not to iteratively improve a whole layout.
        A higher score is better. Negative infinity means it's impossible.
        """
        ### MODIFICATION NOTE: Keeping this function long. A student might write a complex
        ### evaluation like this in one go once they have all the factors in mind.
        ### Adding more "thinking process" comments.

        score_components = { # Keep track of how the score is built, for debugging.
            "base": 0.0, # Starting point
            "slot_capacity_fail": 0.0, # Will be -inf if fails
            "shelf_weight_limit_fail": 0.0, # Will be -inf if fails
            "frozen_mismatch_penalty": 0.0, # For putting frozen in wrong place etc.
            "category_compatibility_score": 0.0, # Do items of this type go well together?
            "item_weight_placement_score": 0.0, # Heavy items on bottom?
            "space_utilization_bonus": 0.0, # Is the shelf nicely full?
            "distance_frequency_bonus": 0.0 # Popular items near entrance?
        }
        current_total_soft_score = 0.0 # For scores that add up, not hard fails.

        # 1. Check hard constraints: Can it physically go there?
        can_add_physically, reason_physical_fail = shelf.can_add_item(item_to_place, self.max_weight_config_per_level[shelf.shelf_level_index])
        if not can_add_physically:
            if reason_physical_fail == "slot_capacity":
                score_components["slot_capacity_fail"] = -float('inf')
            elif reason_physical_fail == "weight_limit":
                score_components["shelf_weight_limit_fail"] = -float('inf')
            return -float('inf'), score_components # No point checking further.

        # 2. Frozen item rules:
        if item_to_place.is_frozen and not rack.is_rack_frozen:
            # Frozen item MUST go in a frozen rack.
            score_components["frozen_mismatch_penalty"] = -float('inf')
            return -float('inf'), score_components
        if not item_to_place.is_frozen and rack.is_rack_frozen and len(shelf.items_on_shelf) > 0:
            # Don't mix non-frozen items with (presumably) frozen items already on a shelf in a frozen rack.
            score_components["frozen_mismatch_penalty"] = -float('inf')
            return -float('inf'), score_components
        elif not item_to_place.is_frozen and rack.is_rack_frozen and len(shelf.items_on_shelf) == 0:
            # Placing a non-frozen item in an EMPTY shelf of a frozen rack.
            # Not ideal, so give it a penalty, but not a hard fail.
            score_components["frozen_mismatch_penalty"] = -10.0 # Big penalty!

        # 3. Category Compatibility:
        # How well does this item's category fit with items already on the shelf?
        # A higher score here is better.
        if len(shelf.items_on_shelf) > 0:
            sum_compatibility = 0.0
            for existing_item_on_shelf in shelf.items_on_shelf:
                # Look up compatibility: item_to_place.category VS existing_item_on_shelf.category
                # Using .get for safety in case a category isn't in the matrix.
                compat_score = COMPATIBILITY_MATRIX.get(item_to_place.category, {}).get(existing_item_on_shelf.category, 0.0)
                sum_compatibility += compat_score
            # Average compatibility, and maybe give it a bit more weight.
            cat_compat_val = (sum_compatibility / len(shelf.items_on_shelf)) * 2.0
        else:
            # If the shelf is empty, compatibility is neutral (or good, depends on view).
            cat_compat_val = 1.0 # Default good score for an empty shelf.
        score_components["category_compatibility_score"] = cat_compat_val
        current_total_soft_score += cat_compat_val

        # 4. Item Weight Placement:
        # General rule: heavy items on bottom shelves, lighter items can go higher.
        item_w_place_val = 0.0
        if item_to_place.weight > HEAVY_ITEM_THRESHOLD: # It's a heavy item
            if shelf.shelf_level_index == 0: item_w_place_val = 1.5 # Good! Heavy on bottom.
            elif shelf.shelf_level_index == 1: item_w_place_val = 0.5 # Okay for middle.
            else: item_w_place_val = -1.0 # Bad! Heavy on top.
        else: # It's a light item
            if shelf.shelf_level_index == (SHELF_LEVELS - 1) : item_w_place_val = 0.2 # Slight bonus for light on top.
        score_components["item_weight_placement_score"] = item_w_place_val
        current_total_soft_score += item_w_place_val
        
        # 5. Space Utilization:
        # Encourage filling up shelves.
        new_occupancy_ratio = (shelf.occupied_slots + item_to_place.slots_required) / shelf.max_slots
        space_util_val = 0.0
        if new_occupancy_ratio > 0.75: space_util_val = 0.3 # Bonus if shelf becomes >75% full.
        if new_occupancy_ratio == 1.0: space_util_val += 0.5 # Extra bonus if it's perfectly full!
        score_components["space_utilization_bonus"] = space_util_val
        current_total_soft_score += space_util_val
        
        # 6. Distance to Entrance & Item Frequency:
        # Popular items (high frequency_metric) should be closer to the relevant entrance.
        dist_freq_val = 0.0
        # Pick the right entrance (main or frozen area)
        relevant_entrance_coords = self.frozen_区域_entrance_coords if rack.is_rack_frozen else self.main_entrance_coords
        if relevant_entrance_coords and rack.rack_center_coords != (0,0): # Check if coords are set
            distance_to_entrance = euclidean_distance(rack.rack_center_coords, relevant_entrance_coords)
            distance_to_entrance = max(distance_to_entrance, 0.1) # Avoid division by zero

            # Base score: higher for shorter distance.
            # The DISTANCE_BASE_FACTOR scales this - smaller factor means distance matters more quickly.
            base_dist_score_part = (1 / distance_to_entrance) * (1 / DISTANCE_BASE_FACTOR)
            
            # Multiplier based on item's pick frequency.
            # Popular items get a higher multiplier, making them prefer closer spots more strongly.
            frequency_multiplier = 1.0 + (item_to_place.frequency_metric * FREQUENCY_DISTANCE_MULTIPLIER)
            
            dist_freq_val = base_dist_score_part * frequency_multiplier
            dist_freq_val = min(dist_freq_val, MAX_DISTANCE_SCORE_CONTRIBUTION) # Cap this bonus.
        score_components["distance_frequency_bonus"] = dist_freq_val
        current_total_soft_score += dist_freq_val
        
        # Final score calculation
        # Add up the base (0), any soft penalties (like frozen mismatch if not -inf), and all soft scores.
        final_calculated_score = score_components["base"]
        if score_components["frozen_mismatch_penalty"] != -float('inf'): # only add if not a hard fail
            final_calculated_score += score_components["frozen_mismatch_penalty"]
        final_calculated_score += current_total_soft_score
        
        return final_calculated_score, score_components

    def find_best_placement_for_item(self, item_id_to_place: str):
        """
        Tries to find the best spot for a single item.
        It checks ALL possible shelves and picks the one with the highest score.
        This is like doing the 'get_best_neighbor' step of a local search, but for placing
        one item into the current warehouse state, not for improving an entire existing layout of many items.
        """
        item_data_to_place = self._get_item_placement_data_by_id(item_id_to_place)
        if not item_data_to_place:
            print(f"Cannot analyze {item_id_to_place}: item not in database.")
            return None, -float('inf'), {} # No item, no spot.

        all_evaluated_options = [] # To store scores for every possible spot
        
        print(f"\n--- Evaluating All Potential Placements for: {item_data_to_place} ---")
        print("-" * 90)
        print(f"{'Location':<12} | {'Score':>7} | {'Breakdown of Score (Key Factors)':<60}")
        print("-" * 90)

        # This is like exploring all possible "moves" for this one item.
        for rack_id, current_rack in self.rack_states_map.items():
            for shelf_idx in range(SHELF_LEVELS):
                current_shelf = current_rack.get_shelf_state(shelf_idx)
                if not current_shelf: continue # Should not happen if rack init is correct

                # Get the score for this specific rack-shelf combination
                calculated_score, score_details = self.evaluate_potential_placement(item_data_to_place, current_rack, current_shelf)
                
                option_location_string = f"{rack_id}-L{shelf_idx}"
                all_evaluated_options.append({
                    "score_value": calculated_score,
                    "placement_location_tuple": (rack_id, shelf_idx), # Store as tuple for easy use
                    "placement_location_str": option_location_string,
                    "score_breakdown_dict": score_details
                })

                # Prepare a summary of the score breakdown for printing
                breakdown_summary_parts = []
                for component_name, component_value in score_details.items():
                    if component_value == -float('inf'):
                        # Just show the part that failed, e.g., "Slot capacity: FAIL"
                        breakdown_summary_parts.append(f"{component_name.split('_')[0].capitalize()}: FAIL")
                    elif component_value != 0.0: # Only show non-zero contributing factors
                        breakdown_summary_parts.append(f"{component_name.split('_')[0].capitalize()}: {component_value:.2f}")
                print(f"{option_location_string:<12} | {calculated_score:7.2f} | {'; '.join(breakdown_summary_parts)}")
        print("-" * 90)

        # Now, find the best option from all evaluations
        # First, filter out spots where placement is impossible (score is -infinity)
        ### MODIFICATION NOTE: Using an explicit loop here instead of list comprehension.
        ### This is a common pattern for students newer to Python.
        valid_options_for_placement = []
        for option in all_evaluated_options:
            if option["score_value"] > -float('inf'):
                valid_options_for_placement.append(option)

        if not valid_options_for_placement:
            print(f"NO VALID SPOT FOUND for {item_data_to_place.item_id}. Reasons for failure across all spots:")
            # Let's count why it failed everywhere.
            failure_reason_counts = {}
            for spot_evaluation_result in all_evaluated_options: # Look at ALL attempts
                for component, value in spot_evaluation_result["score_breakdown_dict"].items():
                    if value == -float('inf'): # This component caused a hard fail for this spot
                        # Clean up the name for display, e.g. "slot_capacity_fail" -> "Slot capacity"
                        clean_reason_name = component.replace("_fail","").replace("_penalty","").replace("_mismatch","").replace("_", " ")
                        failure_reason_counts[clean_reason_name] = failure_reason_counts.get(clean_reason_name, 0) + 1
            # Print the summary of failure reasons
            for reason, count in sorted(failure_reason_counts.items(), key=lambda x: x[1], reverse=True): # Sort by most common
                print(f"  - {reason.capitalize()} caused failure at {count} locations.")
            return None, -float('inf'), failure_reason_counts # No spot, -inf score, and why.
            
        # If we have valid options, sort them to find the best (highest score)
        valid_options_for_placement.sort(key=lambda opt: opt["score_value"], reverse=True) # Highest score first
        
        chosen_best_option_details = valid_options_for_placement[0] # This is our "steepest ascent" for this one item.
        
        print(f"\nSELECTED BEST OPTION: {chosen_best_option_details['placement_location_str']} | Score: {chosen_best_option_details['score_value']:.2f}")
        print("  Breakdown for the Best Spot:")
        for component_name, component_value in chosen_best_option_details['score_breakdown_dict'].items():
            # Only show non-zero, non-infinity components that contributed to the final score.
            if component_value != 0.0 and component_value != -float('inf'):
                print(f"    - {component_name.split('_')[0].capitalize()}: {component_value:.2f}")
        
        return chosen_best_option_details['placement_location_tuple'], chosen_best_option_details['score_value'], chosen_best_option_details['score_breakdown_dict']

    def execute_item_placement(self, item_id_to_place: str, placement_location_tuple: tuple):
        """Actually puts the item on the shelf in our system's model."""
        if not placement_location_tuple or not self.max_weight_config_per_level:
            # print(f"Cannot execute placement for {item_id_to_place}: invalid location or missing weight config.")
            return False
        
        item_data = self._get_item_placement_data_by_id(item_id_to_place)
        if not item_data:
            # print(f"Cannot execute placement: item {item_id_to_place} not found.")
            return False
        
        rack_id_str, shelf_level_idx = placement_location_tuple
        
        if rack_id_str in self.rack_states_map:
            target_rack = self.rack_states_map[rack_id_str]
            target_shelf = target_rack.get_shelf_state(shelf_level_idx)
            
            if target_shelf:
                # The add_item method itself re-checks constraints.
                if target_shelf.add_item(item_data, self.max_weight_config_per_level[shelf_level_idx]):
                    # print(f"Successfully placed {item_id_to_place} at {rack_id_str}-L{shelf_level_idx}.")
                    return True
                # else:
                    # print(f"Execution failed: {item_id_to_place} could not be added to {rack_id_str}-L{shelf_level_idx} (likely already full or overweight).")
            # else:
                # print(f"Execution failed: Shelf {shelf_level_idx} not found in rack {rack_id_str}.")
        # else:
            # print(f"Execution failed: Rack {rack_id_str} not found.")
        return False

    def visualize_current_state(self, title_str="Warehouse State", item_id_to_highlight=None, rack_id_to_highlight=None, shelf_level_to_highlight=None):
        """
        Draws the warehouse state. This function is quite long because plotting has many details!
        A student might write it all in one go once they figure out matplotlib.
        """
        ### MODIFICATION NOTE: Keeping this function long. Adding some "student-like" comments about its complexity.
        num_racks_to_show = len(self.rack_states_map)
        if num_racks_to_show == 0:
            print("No racks to visualize.")
            return

        plot_cols = 4 # How many racks side-by-side
        plot_rows = (num_racks_to_show + plot_cols - 1) // plot_cols # Calculate rows needed
        
        # This creates the main window and all the little sub-plots for each rack
        fig_obj, axes_array = plt.subplots(plot_rows, plot_cols, figsize=(plot_cols * 4.5, plot_rows * 4.5), squeeze=False)
        flat_axes = axes_array.flatten() # Makes it easier to loop through subplots
        
        # Sort racks by ID so they appear in a consistent order in the plot
        sorted_rack_ids = sorted(list(self.rack_states_map.keys()))
        
        # Prepare labels for the shelf levels (y-axis of each rack plot)
        shelf_labels_for_plot = []
        if self.max_weight_config_per_level and len(self.max_weight_config_per_level) >= SHELF_LEVELS:
            for j in range(SHELF_LEVELS):
                shelf_labels_for_plot.append(f"L{j}\n({self.max_weight_config_per_level[j]}kg)")
        else: # Fallback if weight info is missing
            for j in range(SHELF_LEVELS):
                shelf_labels_for_plot.append(f"L{j}\n(?kg)")

        ax_idx = -1 # To keep track of which subplot we are drawing on
        for ax_idx, current_rack_id in enumerate(sorted_rack_ids):
            ax_current = flat_axes[ax_idx] # Get the current subplot
            current_rack_object = self.rack_states_map[current_rack_id]

            # Setup for each rack's plot
            ax_current.set_xlim(-0.5, MAX_SLOTS_PER_SHELF + 0.5)
            ax_current.set_ylim(-0.5, SHELF_LEVELS - 0.5 + 1) # +1 to make top shelf fully visible
            ax_current.set_xticks(range(MAX_SLOTS_PER_SHELF + 1))
            ax_current.set_yticks(range(SHELF_LEVELS))
            ax_current.set_yticklabels(shelf_labels_for_plot)
            ax_current.grid(True, linestyle='--', alpha=0.7) # Light grid for readability
            
            rack_plot_title = f"R {current_rack_object.rack_id_str}"
            if current_rack_object.is_rack_frozen:
                rack_plot_title += " (F)" # Mark frozen racks
            ax_current.set_title(rack_plot_title, fontsize=9)

            # Draw items on each shelf of this rack
            for shelf_idx_in_rack, current_shelf_object in enumerate(current_rack_object.shelf_states):
                x_draw_offset = 0 # Start drawing items from the left of the shelf
                for item_on_this_shelf in current_shelf_object.items_on_shelf:
                    item_display_width = item_on_this_shelf.slots_required
                    item_display_height = 0.8 # Make items not fill the whole shelf height
                    
                    item_color = CATEGORY_COLORS.get(item_on_this_shelf.category, CATEGORY_COLORS['default'])
                    
                    # Is this the specific item we want to highlight?
                    is_the_highlighted_item = (item_on_this_shelf.item_id == item_id_to_highlight and
                                               current_rack_object.rack_id_str == rack_id_to_highlight and
                                               current_shelf_object.shelf_level_index == shelf_level_to_highlight)
                    
                    edge_color, line_width = ('red', 2.5) if is_the_highlighted_item else ('black', 1)
                    
                    # Create the rectangle for the item
                    item_rectangle = patches.Rectangle(
                        (x_draw_offset, shelf_idx_in_rack + (1 - item_display_height) / 2), # Position (x, y_centered)
                        item_display_width, item_display_height,
                        facecolor=item_color, edgecolor=edge_color, linewidth=line_width,
                        alpha=0.8, label=f"_{item_on_this_shelf.category}" # Underscore hides from auto-legend if not handled
                    )
                    ax_current.add_patch(item_rectangle)
                    # Add text inside the item (ID and weight)
                    ax_current.text(x_draw_offset + item_display_width / 2, shelf_idx_in_rack + 0.5, # Centered text
                                    f"{item_on_this_shelf.item_id[:5]}\n{item_on_this_shelf.weight}kg",
                                    ha='center', va='center', fontsize=5.5, color='black')
                    x_draw_offset += item_display_width # Move to the right for the next item

            # If we're highlighting a *potential* placement spot (item not yet on shelf)
            if item_id_to_highlight and rack_id_to_highlight == current_rack_object.rack_id_str and shelf_level_to_highlight is not None:
                target_shelf_for_highlight = current_rack_object.get_shelf_state(shelf_level_to_highlight)
                if target_shelf_for_highlight:
                    # Check if the item to highlight is ALREADY on this shelf. If so, it was drawn above.
                    item_already_present = False
                    for existing_item in target_shelf_for_highlight.items_on_shelf:
                        if existing_item.item_id == item_id_to_highlight:
                            item_already_present = True
                            break
                    
                    if not item_already_present: # If it's a true "target" for a new item
                        target_item_details = self._get_item_placement_data_by_id(item_id_to_highlight)
                        if target_item_details and self.max_weight_config_per_level:
                            # Check if it *can* be placed here (for visualization purposes)
                            can_place_visual_target, _ = target_shelf_for_highlight.can_add_item(
                                target_item_details, self.max_weight_config_per_level[shelf_level_to_highlight]
                            )
                            if can_place_visual_target:
                                # Draw a placeholder for the target item
                                target_rect_viz = patches.Rectangle(
                                    (target_shelf_for_highlight.occupied_slots, shelf_level_to_highlight + (1 - 0.8) / 2),
                                    target_item_details.slots_required, 0.8,
                                    facecolor='yellow', edgecolor='red', linewidth=2, alpha=0.5, linestyle='--'
                                )
                                ax_current.add_patch(target_rect_viz)
                                ax_current.text(
                                    target_shelf_for_highlight.occupied_slots + target_item_details.slots_required / 2,
                                    shelf_level_to_highlight + 0.5,
                                    f"TARGET\n{target_item_details.item_id[:5]}",
                                    ha='center', va='center', fontsize=5, color='red'
                                )
        
        # Clean up any unused subplots if the number of racks isn't a perfect multiple of plot_cols
        if ax_idx >= 0: # If at least one rack was drawn
            for k in range(ax_idx + 1, len(flat_axes)):
                fig_obj.delaxes(flat_axes[k]) # Remove empty subplots
        
        # Create a legend for item categories
        legend_patches = []
        for category_name, color_code in CATEGORY_COLORS.items():
            if category_name != 'default': # Don't include 'default' in legend explicitly
                legend_patches.append(patches.Patch(color=color_code, label=category_name))
        
        fig_obj.legend(handles=legend_patches, loc='lower center', ncol=len(legend_patches),
                       bbox_to_anchor=(0.5, 0.01), fontsize='small') # Position legend at bottom
        
        fig_obj.suptitle(title_str, fontsize=16) # Main title for the whole plot
        plt.tight_layout(rect=[0, 0.05, 1, 0.96]) # Adjust layout to prevent overlap (leave space for legend/title)
        plt.show() # Display the plot


# --- MAIN EXECUTION ---
# This is what runs when you execute the script.
if __name__ == "__main__":
    print("--- Generating Dummy Data (if needed) ---")
    generate_dummy_item_csv("dummy_items.csv", num_items=50) # Create 50 dummy items
    
    # Try to get rack IDs from facts.json, or use defaults if it fails
    try:
        with open("facts.json", 'r') as f:
            facts_config = json.load(f)
        rack_ids_for_layout = list(facts_config.get("racks_info", {}).keys())
        all_item_ids_from_csv = list(pd.read_csv("dummy_items.csv")['id'])
    except Exception as e:
        print(f"Note: Could not read facts.json or dummy_items.csv for dynamic layout generation ({e}). Using defaults.")
        rack_ids_for_layout = [f"R{str(i+1).zfill(2)}" for i in range(12)] # Default to 12 racks
        all_item_ids_from_csv = [f"item{str(i+1).zfill(3)}" for i in range(50)] # Default to 50 item IDs

    # Generate an initial sparse layout, using only some of the items
    generate_dummy_rack_layout_csv("dummy_rack_layout.csv",
                                   rack_ids=rack_ids_for_layout,
                                   item_ids_for_layout=all_item_ids_from_csv[:15]) # Use first 15 items for initial layout
    print("-" * 30)

    # Setup the warehouse system
    print("--- Initializing Warehouse System ---")
    placement_system = WarehousePlacementSystem(facts_json_file="facts.json") # This loads facts.json
    placement_system.load_item_properties_from_csv("dummy_items.csv") # Load all item details
    placement_system.initialize_layout_from_csv("dummy_rack_layout.csv") # Place items from the layout file

    print("\n--- Initial Warehouse State ---")
    placement_system.visualize_current_state("Initial Warehouse Layout")

    # --- Now, let's try to place some NEW items ---
    # Find items that are in our database but not yet in the warehouse
    all_item_ids_in_system_db = list(placement_system.item_database.keys())
    
    ids_of_items_already_placed = set()
    for rack in placement_system.rack_states_map.values():
        for shelf in rack.shelf_states:
            for item_on_shelf in shelf.items_on_shelf:
                ids_of_items_already_placed.add(item_on_shelf.item_id)
    
    items_needing_placement = []
    for item_id_candidate in all_item_ids_in_system_db:
        if item_id_candidate not in ids_of_items_already_placed:
            items_needing_placement.append(item_id_candidate)
    ### MODIFICATION NOTE: Changed list comprehension to explicit loop for `items_needing_placement`.

    random.shuffle(items_needing_placement) # Place them in a random order
    
    # Let's try to place a few of these, e.g., the first 10
    num_items_to_try_inserting = 10
    items_to_insert_in_this_run = items_needing_placement[:num_items_to_try_inserting]

    if not items_to_insert_in_this_run:
        print("\nNo new items from the database need placement (all already in initial layout or DB empty).")

    summary_of_successful_placements = [] # To keep track of what we did

    for i, current_item_id_to_add in enumerate(items_to_insert_in_this_run):
        print(f"\n\n{'='*15} ATTEMPTING TO PLACE ITEM {i+1}/{len(items_to_insert_in_this_run)}: {current_item_id_to_add} {'='*15}")
        
        item_details_for_placement = placement_system._get_item_placement_data_by_id(current_item_id_to_add)
        if not item_details_for_placement:
            print(f"Skipping item {current_item_id_to_add} - details not found in database.")
            continue
        
        # This is where we ask the system to find the best spot using our scoring logic
        best_spot_found_tuple, best_score_for_spot, score_breakdown = placement_system.find_best_placement_for_item(current_item_id_to_add)
        
        if best_spot_found_tuple: # If a valid spot was found (score > -infinity)
            # Record this potential successful placement
            summary_of_successful_placements.append({
                "item_id": item_details_for_placement.item_id,
                "item_name": item_details_for_placement.name,
                "rack_id": best_spot_found_tuple[0],
                "shelf_level": best_spot_found_tuple[1],
                "score": best_score_for_spot
            })

            # Visualize where we *intend* to place it (the "TARGET")
            # Making a copy so the visualization doesn't change the actual system state yet
            temp_warehouse_for_viz = copy.deepcopy(placement_system)
            temp_warehouse_for_viz.visualize_current_state(
                f"Target for ({i+1}): {item_details_for_placement.item_id} at {best_spot_found_tuple[0]}-L{best_spot_found_tuple[1]}",
                item_id_to_highlight=current_item_id_to_add,
                rack_id_to_highlight=best_spot_found_tuple[0],
                shelf_level_to_highlight=best_spot_found_tuple[1]
            )
            
            print(f"\n--- System recommends placing {current_item_id_to_add} at {best_spot_found_tuple}. Attempting now... ---")
            # Now, actually try to place it in the main system
            if placement_system.execute_item_placement(current_item_id_to_add, best_spot_found_tuple):
                print(f"Successfully placed {current_item_id_to_add}.")
                # Show the warehouse state *after* successful placement
                placement_system.visualize_current_state(
                    f"Placed ({i+1}): {item_details_for_placement.item_id} at {best_spot_found_tuple[0]}-L{best_spot_found_tuple[1]}",
                    item_id_to_highlight=current_item_id_to_add,
                    rack_id_to_highlight=best_spot_found_tuple[0],
                    shelf_level_to_highlight=best_spot_found_tuple[1]
                )
                # Update insertion counter for the item in the database
                if current_item_id_to_add in placement_system.item_database:
                    placement_system.item_database[current_item_id_to_add]['insertion_counter'] += 1
            else:
                # This should be rare if find_best_placement_for_item worked, but good to handle.
                print(f"ERROR: Placement of {current_item_id_to_add} FAILED during execution, even though a spot was found.")
                # If execution failed, remove it from the "successful" summary
                summary_of_successful_placements = [p for p in summary_of_successful_placements if p["item_id"] != current_item_id_to_add]
        else:
            print(f"===> No suitable spot found for item {current_item_id_to_add} based on current rules. Item not placed. <===")
            # Show the state, indicating no spot was found for this one
            placement_system.visualize_current_state(f"No spot found for {current_item_id_to_add} (Attempt {i+1}) - Warehouse State")
        
        # Optional: Pause between items for manual review
        # if i < len(items_to_insert_in_this_run) - 1:
        #      input(f"Press Enter to attempt placing the next item ({len(items_to_insert_in_this_run) - 1 - i} remaining)...")

    print("\n\n--- Final Warehouse State After All Placement Attempts ---")
    placement_system.visualize_current_state("Final Warehouse State")

    # --- Print a summary of what was placed ---
    print("\n\n--- SUMMARY OF SUCCESSFUL PLACEMENTS THIS RUN ---")
    if summary_of_successful_placements:
        for placement_info in summary_of_successful_placements:
            print(f"Item ID: {placement_info['item_id']} (Name: {placement_info['item_name']}) "
                  f"placed at Rack: {placement_info['rack_id']}, Shelf: L{placement_info['shelf_level']} "
                  f"(Score: {placement_info['score']:.2f})")
    else:
        print("No new items were successfully placed during this simulation run.")

    print("\n--- Simulation Complete ---")