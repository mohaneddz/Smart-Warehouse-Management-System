import random
import copy
import math

# --- DUMMY DATA AND HELPERS (Assume these are well-defined for your actual data) ---
DUMMY_ITEM_DB = {
    'itemA': {'weight': 15, 'category': 'food', 'slots': 1}, 'itemB': {'weight': 25, 'category': 'food', 'slots': 2},
    'itemC': {'weight': 5, 'category': 'beverages', 'slots': 1}, 'itemD': {'weight': 40, 'category': 'household goods', 'slots': 3},
    'itemE': {'weight': 50, 'category': 'household goods', 'slots': 2}, 'itemF': {'weight': 2, 'category': 'chemicals', 'slots': 1},
    'itemG': {'weight': 8, 'category': 'food', 'slots': 1}, 'itemH': {'weight': 12, 'category': 'beverages', 'slots': 2},
    'itemI': {'weight': 30, 'category': 'household goods', 'slots': 1}, 'itemJ': {'weight': 60, 'category': 'household goods', 'slots': 3},
    'itemK_frozen': {'weight': 10, 'category': 'frozen', 'slots': 1}, 'itemL_frozen': {'weight': 18, 'category': 'frozen', 'slots': 2},
    'itemM_frozen_sml': {'weight': 5, 'category': 'frozen', 'slots': 1}, 'itemN_food_sml': {'weight': 7, 'category': 'food', 'slots': 1},
}
MAX_SLOTS_PER_SHELF = 5
HEAVY_ITEM_THRESHOLD = 20

def get_item_details(item_id):
    return DUMMY_ITEM_DB.get(item_id, {'weight': 0, 'category': 'unknown', 'slots': 1})

COMPATIBILITY_MATRIX = {
    'food': {'food': True, 'beverages': True, 'household goods': True, 'chemicals': False, 'frozen': False},
    'beverages': {'food': True, 'beverages': True, 'household goods': True, 'chemicals': False, 'frozen': False},
    'household goods': {'food': True, 'beverages': True, 'household goods': True, 'chemicals': False, 'frozen': False},
    'chemicals': {'food': False, 'beverages': False, 'household goods': False, 'chemicals': True, 'frozen': False},
    'frozen': {'food': False, 'beverages': False, 'household goods': False, 'chemicals': False, 'frozen': True},
}

def is_compatible_on_shelf(shelf_items_categories, new_item_category, is_rack_frozen):
    if is_rack_frozen and new_item_category != 'frozen':
        return False # Non-frozen item cannot go into a frozen rack's shelf
    if not is_rack_frozen and new_item_category == 'frozen':
        return False # Frozen item cannot go into a non-frozen rack's shelf

    for existing_category in shelf_items_categories:
        if new_item_category == 'frozen' and existing_category != 'frozen': return False
        if existing_category == 'frozen' and new_item_category != 'frozen': return False
        if not COMPATIBILITY_MATRIX.get(existing_category, {}).get(new_item_category, False):
            return False
    return True

def get_shelf_categories(shelf_items):
    return [get_item_details(item_id)['category'] for item_id in shelf_items]

# --- RACK DATA (Placeholder - you'll get this from your Warehouse object) ---
# Assume each rack object/dict has an 'id' and 'is_frozen' attribute
# and a 'layout' attribute: [[L1_items], [L2_items], [L3_items]]
DUMMY_RACKS_DATA = {
    'R01': {'id': 'R01', 'is_frozen': False, 'layout': [['itemA', 'itemC'], ['itemD'], ['itemF', 'itemN_food_sml']]},
    'R02': {'id': 'R02', 'is_frozen': False, 'layout': [['itemJ'], [], ['itemB', 'itemG']]},
    'R03': {'id': 'R03', 'is_frozen': False, 'layout': [[], ['itemE', 'itemH'], []]},
    'R04': {'id': 'R04', 'is_frozen': True, 'layout': [['itemK_frozen'], ['itemL_frozen'], []]},
    'R05': {'id': 'R05', 'is_frozen': True, 'layout': [['itemM_frozen_sml'],[],[]]}
}
# --- Genetic Algorithm Class (Revised for Pool of Racks) ---

class GeneticAlgorithmPoolOptimizer:
    def __init__(self, initial_rack_pool_layouts, is_optimizing_frozen_racks,
                 generations=50, population_size=30, tournament_size=3,
                 crossover_rate=0.8, mutation_rate=0.1, elite_size=2):
        """
        Initializes GA for a pool of racks (either all frozen or all non-frozen).
        Args:
            initial_rack_pool_layouts (list): List of rack layouts.
                Each element is {'id': str, 'is_frozen': bool, 'layout': [[L1], [L2], [L3]]}.
            is_optimizing_frozen_racks (bool): True if this GA instance is for frozen racks.
        """
        if not initial_rack_pool_layouts:
            raise ValueError("Initial rack pool cannot be empty.")

        self.is_optimizing_frozen_racks = is_optimizing_frozen_racks
        self.num_racks_in_pool = len(initial_rack_pool_layouts)

        # Population: list of individuals. Each individual is a list of rack data dicts.
        self.population = []
        for _ in range(population_size):
            # Create a deep copy of the initial pool for each individual in the population
            individual = copy.deepcopy(initial_rack_pool_layouts)
            self.population.append(individual)

        # Introduce initial variations (more advanced mutation might be needed for diversity)
        # For simplicity, we'll rely on the main mutation operator during evolution.
        # Or, apply a light initial shuffle/mutation to each individual if desired.

        self.generations = generations
        self.population_size = population_size
        self.tournament_size = tournament_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate # Chance for an individual (pool state) to be mutated
        self.rack_mutation_rate = 0.2 # Chance for a rack within an individual to be part of mutation
        self.shelf_mutation_rate = 0.1 # Chance for a shelf to be chosen for item move/swap
        self.elite_size = elite_size
        self.fitness_cache = {}

        # Fitness weights (these might need different tuning for frozen vs non-frozen)
        self.w_util = 0.40
        self.w_purity = 0.15
        self.w_weight = 0.20
        self.w_compat = 0.20 # Compatibility is handled more by rack type now
        self.w_empty = 0.05

    def _get_shelf_slots_used(self, shelf_items):
        return sum(get_item_details(item_id)['slots'] for item_id in shelf_items)

    def _validate_and_repair_shelf(self, shelf_items, is_rack_frozen):
        validated_items = []
        slots_used = 0
        for item_id in shelf_items:
            item_detail = get_item_details(item_id)
            # Basic check: frozen items only in frozen racks, non-frozen only in non-frozen
            if is_rack_frozen and item_detail['category'] != 'frozen':
                continue # Skip non-frozen item for a frozen rack's shelf
            if not is_rack_frozen and item_detail['category'] == 'frozen':
                continue # Skip frozen item for a non-frozen rack's shelf

            if slots_used + item_detail['slots'] <= MAX_SLOTS_PER_SHELF:
                current_shelf_categories = get_shelf_categories(validated_items)
                if is_compatible_on_shelf(current_shelf_categories, item_detail['category'], is_rack_frozen):
                    validated_items.append(item_id)
                    slots_used += item_detail['slots']
        return validated_items

    def _validate_and_repair_rack_layout(self, rack_data): # rack_data is {'id':.., 'is_frozen':.., 'layout':..}
        is_frozen = rack_data['is_frozen']
        for i in range(len(rack_data['layout'])):
            rack_data['layout'][i] = self._validate_and_repair_shelf(rack_data['layout'][i], is_frozen)
        return rack_data

    def _calculate_fitness_for_single_rack(self, rack_data): # rack_data is {'id':.., 'is_frozen':.., 'layout':..}
        rack_layout = rack_data['layout']
        is_rack_frozen = rack_data['is_frozen']

        total_utilization = 0; total_purity = 0; weight_penalty = 0
        compatibility_penalty_rack = 0; empty_shelf_penalty = 0
        num_shelves = 3

        for level_idx, shelf_items in enumerate(rack_layout):
            slots_used = self._get_shelf_slots_used(shelf_items)
            shelf_utilization = slots_used / MAX_SLOTS_PER_SHELF if MAX_SLOTS_PER_SHELF > 0 else 0
            total_utilization += shelf_utilization

            shelf_item_details = [get_item_details(item_id) for item_id in shelf_items]
            categories_on_shelf = set(details['category'] for details in shelf_item_details)

            for details in shelf_item_details:
                if is_rack_frozen and details['category'] != 'frozen':
                    compatibility_penalty_rack += 50 # Severe penalty for non-frozen in frozen rack
                if not is_rack_frozen and details['category'] == 'frozen':
                    compatibility_penalty_rack += 50 # Severe penalty for frozen in non-frozen rack
                if level_idx > 0 and details['weight'] > HEAVY_ITEM_THRESHOLD:
                    weight_penalty += details['weight'] * level_idx * 0.01 # Scaled penalty

            if categories_on_shelf:
                total_purity += 1.0 / len(categories_on_shelf)
                # Check within-shelf compatibility (already partially handled by validate_and_repair)
                current_shelf_cats = list(categories_on_shelf)
                for i in range(len(current_shelf_cats)):
                    for j in range(i + 1, len(current_shelf_cats)):
                        if not is_compatible_on_shelf([current_shelf_cats[i]], current_shelf_cats[j], is_rack_frozen):
                             compatibility_penalty_rack += 2 # Smaller penalty, as validate should catch most
            else:
                total_purity += 1.0 # Max purity for empty shelf

            is_empty = not shelf_items
            if level_idx > 0 and is_empty and level_idx -1 >=0 and \
               self._get_shelf_slots_used(rack_layout[level_idx-1]) < MAX_SLOTS_PER_SHELF * 0.5:
                empty_shelf_penalty += 0.5
            elif level_idx == 0 and is_empty and any(len(s) > 0 for s in rack_layout[1:]):
                 empty_shelf_penalty += 1

        avg_utilization = total_utilization / num_shelves if num_shelves > 0 else 0
        avg_purity = total_purity / num_shelves if num_shelves > 0 else 0

        fitness = (self.w_util * avg_utilization) + (self.w_purity * avg_purity) - \
                  (self.w_weight * weight_penalty) - (self.w_compat * compatibility_penalty_rack) - \
                  (self.w_empty * empty_shelf_penalty)
        return max(0, fitness)


    def _calculate_overall_fitness(self, individual_pool_state): # individual_pool_state is a list of rack_data dicts
        # For caching, convert the whole state to a hashable form
        # Sorting by rack ID ensures consistent hashing for the same overall state
        sorted_racks_for_hash = sorted(individual_pool_state, key=lambda r: r['id'])
        individual_tuple = tuple(
            (rack['id'], tuple(tuple(sorted(shelf)) for shelf in rack['layout']))
            for rack in sorted_racks_for_hash
        )

        if individual_tuple in self.fitness_cache:
            return self.fitness_cache[individual_tuple]

        total_fitness_sum = 0
        for rack_data in individual_pool_state:
            total_fitness_sum += self._calculate_fitness_for_single_rack(rack_data)
        
        avg_fitness = total_fitness_sum / self.num_racks_in_pool if self.num_racks_in_pool > 0 else 0
        self.fitness_cache[individual_tuple] = avg_fitness
        return avg_fitness

    def _tournament_selection(self):
        # ... (similar to before, but operates on self.population of individuals (pools))
        # Ensure it calls self._calculate_overall_fitness
        if not self.population: raise ValueError("Population empty.")
        tournament_candidates_indices = random.sample(range(len(self.population)), self.tournament_size)
        tournament_candidates = [self.population[i] for i in tournament_candidates_indices]
        
        best_in_tournament = max(tournament_candidates, key=self._calculate_overall_fitness)
        return best_in_tournament


    def _crossover(self, parent1_pool_state, parent2_pool_state):
        # parentX_pool_state is a list of rack_data dicts
        child1_pool_state = copy.deepcopy(parent1_pool_state)
        child2_pool_state = copy.deepcopy(parent2_pool_state)

        if random.random() < self.crossover_rate:
            # Iterate through corresponding racks in the two parent pools
            # Assumes parent1 and parent2 have racks in the same order (e.g., sorted by ID initially)
            # Or, better, ensure racks are identifiable (e.g., by ID) and map them.
            # For simplicity now, assume same order based on initial pool.
            for rack_idx in range(self.num_racks_in_pool):
                # For each shelf level
                for level in range(3): # L1, L2, L3
                    if random.random() < 0.3: # Chance to swap this specific shelf level between these two racks
                        # Ensure rack_idx is valid for both children
                        if rack_idx < len(child1_pool_state) and rack_idx < len(child2_pool_state):
                            # Swap the shelf contents for this level
                            shelf1_content = child1_pool_state[rack_idx]['layout'][level]
                            shelf2_content = child2_pool_state[rack_idx]['layout'][level]
                            child1_pool_state[rack_idx]['layout'][level] = shelf2_content
                            child2_pool_state[rack_idx]['layout'][level] = shelf1_content
            
            # Validate all racks in the new children pools
            for i in range(self.num_racks_in_pool):
                if i < len(child1_pool_state): child1_pool_state[i] = self._validate_and_repair_rack_layout(child1_pool_state[i])
                if i < len(child2_pool_state): child2_pool_state[i] = self._validate_and_repair_rack_layout(child2_pool_state[i])
        
        return child1_pool_state, child2_pool_state

    def _mutate(self, individual_pool_state):
        mutated_pool = copy.deepcopy(individual_pool_state)
        if random.random() > self.mutation_rate: # Chance to mutate this entire pool state
            return mutated_pool # No mutation for this individual

        # Attempt to swap items between shelves of two different racks in the pool
        if self.num_racks_in_pool < 2: # Need at least two racks to swap between
            return mutated_pool

        # Select two different racks from the pool for potential item swap
        rack_idx1, rack_idx2 = random.sample(range(self.num_racks_in_pool), 2)
        
        rack1_data = mutated_pool[rack_idx1]
        rack2_data = mutated_pool[rack_idx2]

        # Ensure racks are of the same type (both frozen or both non-frozen) for swapping
        if rack1_data['is_frozen'] != rack2_data['is_frozen']:
            return mutated_pool # Cannot swap between frozen and non-frozen racks directly here

        # Try a few times to find a valid swap
        for _attempt in range(5): # Max 5 attempts for a valid swap
            # Select a random shelf from each rack
            shelf_level1 = random.randrange(3)
            shelf_level2 = random.randrange(3) # Can be same or different level

            shelf1_items = rack1_data['layout'][shelf_level1]
            shelf2_items = rack2_data['layout'][shelf_level2]

            if not shelf1_items or not shelf2_items: continue # Need items on both shelves

            # Select a random item from each shelf
            item1_idx = random.randrange(len(shelf1_items))
            item2_idx = random.randrange(len(shelf2_items))
            item1_id = shelf1_items[item1_idx]
            item2_id = shelf2_items[item2_idx]

            item1_details = get_item_details(item1_id)
            item2_details = get_item_details(item2_id)

            # Constraint 1: Items must have the same slot size
            if item1_details['slots'] != item2_details['slots']:
                continue

            # Temporarily perform the swap to check validity
            original_shelf1_item = shelf1_items.pop(item1_idx)
            original_shelf2_item = shelf2_items.pop(item2_idx)

            shelf1_items.insert(item1_idx, item2_id) # Item2 goes to shelf1
            shelf2_items.insert(item2_idx, item1_id) # Item1 goes to shelf2

            # Constraint 2 & 3 & 4: Validate both shelves after swap (compatibility, capacity, weight for L1)
            # We simplify validation by just checking the modified shelves.
            # A full re-validation might be safer but more costly.
            
            temp_shelf1_validated = self._validate_and_repair_shelf(list(shelf1_items), rack1_data['is_frozen'])
            temp_shelf2_validated = self._validate_and_repair_shelf(list(shelf2_items), rack2_data['is_frozen'])

            # Check if the swapped items are still present after validation (meaning swap was valid capacity-wise)
            # and that the shelves are still compatible overall.
            valid_swap = True
            if item2_id not in temp_shelf1_validated or item1_id not in temp_shelf2_validated:
                valid_swap = False
            
            # Check overall compatibility of the new shelves
            if valid_swap:
                shelf1_cats = get_shelf_categories(temp_shelf1_validated)
                for cat_idx in range(len(shelf1_cats)): # Check internal compat
                    if not is_compatible_on_shelf(shelf1_cats[:cat_idx], shelf1_cats[cat_idx], rack1_data['is_frozen']):
                        valid_swap = False; break
                if not valid_swap: continue

                shelf2_cats = get_shelf_categories(temp_shelf2_validated)
                for cat_idx in range(len(shelf2_cats)):
                    if not is_compatible_on_shelf(shelf2_cats[:cat_idx], shelf2_cats[cat_idx], rack2_data['is_frozen']):
                        valid_swap = False; break
                if not valid_swap: continue


            # Weight constraint (simplified for this mutation):
            # if shelf_level1 > 0 and item2_details['weight'] > HEAVY_ITEM_THRESHOLD: valid_swap = False
            # if shelf_level2 > 0 and item1_details['weight'] > HEAVY_ITEM_THRESHOLD: valid_swap = False
            # A more robust check would involve the items being replaced.
            # For now, rely on the main fitness function to penalize bad weight distribution over time.

            if valid_swap:
                # print(f"  MUTATION: Swapped {item1_id} (R{rack1_data['id']}-L{shelf_level1+1}) with {item2_id} (R{rack2_data['id']}-L{shelf_level2+1})")
                rack1_data['layout'][shelf_level1] = temp_shelf1_validated
                rack2_data['layout'][shelf_level2] = temp_shelf2_validated
                break # Successful swap, exit attempt loop
            else:
                # Revert swap
                shelf1_items.pop(item1_idx)
                shelf1_items.insert(item1_idx, original_shelf1_item)
                shelf2_items.pop(item2_idx)
                shelf2_items.insert(item2_idx, original_shelf2_item)
        
        # Validate all racks in the pool after potential mutations
        for i in range(self.num_racks_in_pool):
            mutated_pool[i] = self._validate_and_repair_rack_layout(mutated_pool[i])
            
        return mutated_pool

    def run(self):
        self.fitness_cache = {}
        # Initialize best_solution_pool with a deepcopy of the first individual
        best_solution_pool = copy.deepcopy(self.population[0])
        best_overall_fitness = self._calculate_overall_fitness(best_solution_pool)
        print(f"Initial Avg Fitness for {'Frozen' if self.is_optimizing_frozen_racks else 'Non-Frozen'} Pool: {best_overall_fitness:.4f}")

        for generation in range(self.generations):
            # Calculate fitness for all individuals in the population
            pop_with_fitness = []
            for individual_pool in self.population:
                fitness = self._calculate_overall_fitness(individual_pool)
                pop_with_fitness.append((fitness, individual_pool))
            
            pop_with_fitness.sort(key=lambda x: x[0], reverse=True)
            self.population = [item[1] for item in pop_with_fitness] # Update population

            current_gen_best_fitness = pop_with_fitness[0][0]
            if current_gen_best_fitness > best_overall_fitness:
                best_overall_fitness = current_gen_best_fitness
                best_solution_pool = copy.deepcopy(pop_with_fitness[0][1])
                print(f"  Gen {generation}: New Best Avg Pool Fitness = {best_overall_fitness:.4f}")
            elif generation % 5 == 0:
                 print(f"  Gen {generation}: Current Avg Pool Fitness = {best_overall_fitness:.4f}")

            next_generation_population = []
            if self.elite_size > 0:
                next_generation_population.extend(self.population[:self.elite_size])

            while len(next_generation_population) < self.population_size:
                parent1 = self._tournament_selection()
                parent2 = self._tournament_selection()
                child1, child2 = self._crossover(parent1, parent2)
                
                next_generation_population.append(self._mutate(child1))
                if len(next_generation_population) < self.population_size:
                    next_generation_population.append(self._mutate(child2))
            
            self.population = next_generation_population[:self.population_size]
            self.fitness_cache = {} # Clear cache for the next generation

        print(f"Finished GA for {'Frozen' if self.is_optimizing_frozen_racks else 'Non-Frozen'} Pool. Best Avg Fitness: {best_overall_fitness:.4f}")
        return best_solution_pool


# --- Main Orchestration Logic ---
def get_rack_data_from_warehouse(warehouse_object, rack_id):
    # !! CRITICAL PLACEHOLDER !!
    # Replace this with logic to fetch a specific rack's data (id, is_frozen, layout)
    # from your actual 'warehouse_object'.
    # The layout should be [[L1_items], [L2_items], [L3_items]]
    rack_info = DUMMY_RACKS_DATA.get(rack_id)
    if rack_info:
        return copy.deepcopy(rack_info) # Return a copy to avoid modifying dummy data directly
    raise ValueError(f"Rack ID {rack_id} not found in dummy data.")

def get_all_rack_ids_from_warehouse(warehouse_object, frozen_only=None):
    # !! CRITICAL PLACEHOLDER !!
    # Replace this with logic to get all rack IDs from your 'warehouse_object'.
    # If frozen_only is True, return only frozen rack IDs.
    # If frozen_only is False, return only non-frozen rack IDs.
    # If frozen_only is None, return all (not used in this version).
    ids = []
    for r_id, r_data in DUMMY_RACKS_DATA.items():
        if frozen_only is True and r_data['is_frozen']:
            ids.append(r_id)
        elif frozen_only is False and not r_data['is_frozen']:
            ids.append(r_id)
    return ids

def evaluate_overall_efficiency_for_pool(rack_pool_layouts):
    if not rack_pool_layouts: return 0.0
    total_slots_used_pool = 0
    total_possible_slots_pool = 0
    for rack_data in rack_pool_layouts:
        rack_layout = rack_data['layout']
        total_possible_slots_pool += MAX_SLOTS_PER_SHELF * 3
        for shelf_items in rack_layout:
            total_slots_used_pool += sum(get_item_details(item_id)['slots'] for item_id in shelf_items)
    return total_slots_used_pool / total_possible_slots_pool if total_possible_slots_pool > 0 else 0.0


def run_warehouse_reordering_ga(warehouse_object):
    print("--- Starting Warehouse Reordering GA ---")
    all_optimized_racks = {}

    # --- Parameters for GA (can be tuned) ---
    ga_config = {
        "generations": 50,       # Number of generations
        "population_size": 20,   # Number of "entire warehouse states" in population
        "tournament_size": 3,
        "crossover_rate": 0.8,
        "mutation_rate": 0.15,   # Increased mutation for more exploration
        "elite_size": 2
    }

    # 1. Optimize Non-Frozen Racks
    print("\n--- Optimizing NON-FROZEN Rack Pool ---")
    non_frozen_rack_ids = get_all_rack_ids_from_warehouse(warehouse_object, frozen_only=False)
    if non_frozen_rack_ids:
        initial_non_frozen_pool = [get_rack_data_from_warehouse(warehouse_object, r_id) for r_id in non_frozen_rack_ids]
        print(f"Initial Non-Frozen Pool Efficiency: {evaluate_overall_efficiency_for_pool(initial_non_frozen_pool):.2%}")

        non_frozen_ga = GeneticAlgorithmPoolOptimizer(
            initial_rack_pool_layouts=initial_non_frozen_pool,
            is_optimizing_frozen_racks=False,
            **ga_config
        )
        best_non_frozen_pool_state = non_frozen_ga.run()
        for rack_data in best_non_frozen_pool_state:
            all_optimized_racks[rack_data['id']] = rack_data
        print(f"Final Optimized Non-Frozen Pool Efficiency: {evaluate_overall_efficiency_for_pool(best_non_frozen_pool_state):.2%}")
    else:
        print("No non-frozen racks to optimize.")

    # 2. Optimize Frozen Racks
    print("\n--- Optimizing FROZEN Rack Pool ---")
    frozen_rack_ids = get_all_rack_ids_from_warehouse(warehouse_object, frozen_only=True)
    if frozen_rack_ids:
        initial_frozen_pool = [get_rack_data_from_warehouse(warehouse_object, r_id) for r_id in frozen_rack_ids]
        print(f"Initial Frozen Pool Efficiency: {evaluate_overall_efficiency_for_pool(initial_frozen_pool):.2%}")
        
        frozen_ga = GeneticAlgorithmPoolOptimizer(
            initial_rack_pool_layouts=initial_frozen_pool,
            is_optimizing_frozen_racks=True,
            **ga_config # Can use different params for frozen if needed
        )
        best_frozen_pool_state = frozen_ga.run()
        for rack_data in best_frozen_pool_state:
            all_optimized_racks[rack_data['id']] = rack_data
        print(f"Final Optimized Frozen Pool Efficiency: {evaluate_overall_efficiency_for_pool(best_frozen_pool_state):.2%}")
    else:
        print("No frozen racks to optimize.")

    print("\n--- Warehouse Reordering Complete ---")
    return all_optimized_racks


if __name__ == "__main__":
    # This warehouse_object would be an instance of your actual Warehouse class
    # For testing, we pass None and rely on placeholder functions using DUMMY_RACKS_DATA
    dummy_warehouse_object = None 
    
    optimized_warehouse_state = run_warehouse_reordering_ga(dummy_warehouse_object)

    print("\n\n--- Final State of All Optimized Racks ---")
    if optimized_warehouse_state:
        for rack_id, rack_data in optimized_warehouse_state.items():
            is_frz = "(Frozen)" if rack_data['is_frozen'] else "(Non-Frozen)"
            eff = evaluate_overall_efficiency_for_pool([rack_data]) # Efficiency for this single rack
            print(f"Rack ID: {rack_id} {is_frz}, Layout: {rack_data['layout']}, Efficiency: {eff:.2%}")
    else:
        print("No optimization was performed.")