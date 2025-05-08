import random
import math
import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

class Candidate:
    """Represents a candidate solution with its state, cost, and efficiency metrics"""
    def __init__(self, state, value, efficiency):
        self.state = state
        self.value = value
        self.efficiency = efficiency

class Problem:
    """Defines the warehouse optimization problem with all constraints"""
    def __init__(self, filename):
        self.filename = filename
        self.items = []
        self.box_sizes = {
            'L': {'width': 180, 'bins': 3},
            'M': {'width': 120, 'bins': 2},
            'S': {'width': 60, 'bins': 1}
        }
        self.load_items()
        
        # Warehouse configuration
        self.num_racks = 36
        self.freezer_racks = {1, 2, 3, 4, 5, 6}
        self.normal_racks = set(range(7, 37))
        self.shelf_levels = 3
        self.bins_per_shelf = 5
        self.bin_size = 60
        self.shelf_length = self.bins_per_shelf * self.bin_size
        
        self.weight_limits = {1: 400, 2: 250, 3: 150}
        self.category_conflicts = {
            'food': ['chemicals'],
            'beverages': ['chemicals'],
            'chemicals': ['food', 'beverages'],
            'frozen': [],
            'household goods': []
        }

    def load_items(self):
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                size = row['item_size'][0].upper()
                if size not in self.box_sizes:
                    raise ValueError(f"Invalid item size '{row['item_size']}'")
                
                self.items.append({
                    'id': int(row['item_id']),
                    'name': row['item_name'],
                    'size': size,
                    'category': row['category'].lower(),
                    'weight': float(row['weight']),
                    'frequency': float(row['frequency']),
                    'is_frozen': row['category'].lower() == 'frozen'
                })

    def get_bin_requirements(self, size):
        """
        Get bin requirements for an item size
        
        Args:
            size: Item size ('L', 'M', or 'S')
            
        Returns:
            tuple: (bins_needed, possible_starting_positions)
        """
        bins = self.box_sizes[size]['bins']
        possible_starts = list(range(1, self.bins_per_shelf - bins + 2))
        return bins, possible_starts

    def generate_initial_state(self):
        """Generate initial random state respecting all constraints"""
        state = {}
        shelf_usage = defaultdict(set)  # {(rack, shelf): set of occupied bins}
        
        for item in self.items:
            placed = False
            attempts = 0
            bins_needed, possible_starts = self.get_bin_requirements(item['size'])
            
            while not placed and attempts < 100:
                # Choose appropriate racks
                valid_racks = self.freezer_racks if item['is_frozen'] else self.normal_racks
                rack = random.choice(list(valid_racks))
                shelf = random.randint(1, self.shelf_levels)
                
                # Find available consecutive bins
                available_starts = [
                    s for s in possible_starts
                    if all(b not in shelf_usage[(rack, shelf)] 
                      for b in range(s, s + bins_needed))
                ]
                
                if available_starts:
                    start = random.choice(available_starts)
                    positions = list(range(start, start + bins_needed))
                    
                    # Place the item
                    state[item['id']] = (rack, shelf, positions)
                    for pos in positions:
                        shelf_usage[(rack, shelf)].add(pos)
                    placed = True
                else:
                    attempts += 1
            
            if not placed:
                # Fallback placement (may violate constraints)
                valid_racks = self.freezer_racks if item['is_frozen'] else self.normal_racks
                rack = random.choice(list(valid_racks))
                shelf = random.randint(1, self.shelf_levels)
                start = random.randint(1, self.bins_per_shelf - bins_needed + 1)
                positions = list(range(start, start + bins_needed))
                state[item['id']] = (rack, shelf, positions)
        
        return state

    def calculate_efficiency(self, state):
        """
        Calculate shelf efficiency metrics
        
        Args:
            state: Current solution state
            
        Returns:
            tuple: (perfect_shelves, good_shelves, poor_shelves, utilization)
        """
        shelf_stats = defaultdict(lambda: {'used_bins': set(), 'weight': 0, 'categories': set()})
        
        # Track shelf usage
        for item_id, (rack, shelf, positions) in state.items():
            item = next(i for i in self.items if i['id'] == item_id)
            shelf_stats[(rack, shelf)]['used_bins'].update(positions)
            shelf_stats[(rack, shelf)]['weight'] += item['weight']
            shelf_stats[(rack, shelf)]['categories'].add(item['category'])
        
        perfect = good = poor = 0
        total_used = 0
        
        # Classify each shelf
        for (rack, shelf), stats in shelf_stats.items():
            used_width = len(stats['used_bins']) * self.bin_size
            remaining = self.shelf_length - used_width
            
            if remaining == 0:
                perfect += 1
            elif remaining <= self.bin_size:  # Can fit at least one S
                good += 1
            elif remaining >= (self.shelf_length / 2):  # More than half empty
                poor += 1
            
            total_used += used_width
        
        # Calculate overall utilization
        total_space = self.num_racks * self.shelf_levels * self.shelf_length
        utilization = total_used / total_space
        
        return (perfect, good, poor, utilization)

    def evaluate(self, state):
        """
        Evaluate the cost of a solution state
        
        Args:
            state: Solution state to evaluate
            
        Returns:
            tuple: (total_cost, efficiency_metrics)
        """
        cost = 0
        shelf_stats = defaultdict(lambda: {'used_bins': set(), 'weight': 0, 'categories': set(), 'items': []})
        
        # Check hard constraints
        for item_id, (rack, shelf, positions) in state.items():
            item = next(i for i in self.items if i['id'] == item_id)
            shelf_key = (rack, shelf)
            stats = shelf_stats[shelf_key]
            
            # Track shelf usage
            stats['used_bins'].update(positions)
            stats['weight'] += item['weight']
            stats['categories'].add(item['category'])
            stats['items'].append(item)
            
            # Frozen items must be in freezer racks
            if item['is_frozen'] and rack not in self.freezer_racks:
                cost += 10000
                
            # Check weight limits
            if stats['weight'] > self.weight_limits[shelf]:
                cost += 1000
                
            # Check category conflicts
            for other in stats['items']:
                if other['category'] in self.category_conflicts[item['category']]:
                    cost += 1000
        
        # Calculate soft costs
        for item_id, (rack, shelf, positions) in state.items():
            item = next(i for i in self.items if i['id'] == item_id)
            cost += item['frequency'] * shelf  # Accessibility cost
            cost += item['weight'] * shelf     # Weight distribution cost
        
        # Add efficiency metrics
        perfect, good, poor, utilization = self.calculate_efficiency(state)
        cost -= perfect * 50  # Reward perfect shelves
        cost += poor * 100    # Penalize poor shelves
        if utilization < 0.85:
            cost += 1000 * (0.85 - utilization)  # Utilization penalty
            
        return cost, (perfect, good, poor, utilization)

    def generate_neighbor(self, current_state):
        """Generate a valid neighboring state by moving one item"""
        new_state = current_state.copy()
        item_id = random.choice(list(new_state.keys()))
        item = next(i for i in self.items if i['id'] == item_id)
        
        # Try up to 20 random moves
        for _ in range(20):
            # Choose appropriate racks
            valid_racks = self.freezer_racks if item['is_frozen'] else self.normal_racks
            rack = random.choice(list(valid_racks))
            shelf = random.randint(1, self.shelf_levels)
            
            bins_needed, possible_starts = self.get_bin_requirements(item['size'])
            
            # Get current shelf usage
            used_bins = set()
            for other_id, (r, s, positions) in new_state.items():
                if r == rack and s == shelf:
                    used_bins.update(positions)
            
            # Find available consecutive bins
            available_starts = [
                s for s in possible_starts
                if all(b not in used_bins for b in range(s, s + bins_needed))
            ]
            
            if available_starts:
                start = random.choice(available_starts)
                positions = list(range(start, start + bins_needed))
                new_state[item_id] = (rack, shelf, positions)
                return new_state
        
        return current_state  # Return original if no valid move found


def simulated_annealing(problem, initial_temp, cooling_rate, iterations):
    """
    Perform simulated annealing optimization
    
    Args:
        problem: Problem instance
        initial_temp: Starting temperature
        cooling_rate: Temperature reduction factor
        iterations: Maximum iterations
        
    Returns:
        tuple: (best_state, best_cost, best_eff, cost_history, perfect_history, util_history, movement_log)
    """
    current_state = problem.generate_initial_state()
    current_cost, current_eff = problem.evaluate(current_state)
    best_state = current_state.copy()
    best_cost = current_cost
    best_eff = current_eff
    
    # Progress tracking
    cost_history = [current_cost]
    perfect_history = [current_eff[0]]
    util_history = [current_eff[3]]
    movement_log = []
    
    for i in range(iterations):
        temp = initial_temp * (cooling_rate ** i)
        if temp < 1e-6:
            break
            
        neighbor = problem.generate_neighbor(current_state)
        neighbor_cost, neighbor_eff = problem.evaluate(neighbor)
        
        # Acceptance probability
        if neighbor_cost < current_cost or random.random() < math.exp((current_cost - neighbor_cost)/temp):
            # Log changes
            changed_items = [
                item_id for item_id in current_state
                if current_state[item_id] != neighbor.get(item_id, None)
            ]
            
            for item_id in changed_items:
                item = next(i for i in problem.items if i['id'] == item_id)
                old_pos = current_state[item_id]
                new_pos = neighbor[item_id]
                reason = determine_move_reason(problem, item, old_pos, new_pos, neighbor_cost - current_cost)
                movement_log.append(create_movement_record(item, old_pos, new_pos, reason, neighbor_cost - current_cost, i))
            
            current_state = neighbor
            current_cost = neighbor_cost
            current_eff = neighbor_eff
            
            if neighbor_cost < best_cost:
                best_state = neighbor
                best_cost = neighbor_cost
                best_eff = neighbor_eff
        
        # Record progress
        cost_history.append(current_cost)
        perfect_history.append(current_eff[0])
        util_history.append(current_eff[3])
        
        if i % 100 == 0:
            print(f"Iter {i}: Cost={current_cost}, Perfect={current_eff[0]}, Util={current_eff[3]:.1%}")
    
    # Add initial to final movement records
    initial_state = problem.generate_initial_state()
    for item in problem.items:
        item_id = item['id']
        initial_pos = initial_state[item_id]
        final_pos = best_state.get(item_id, None)
        
        if final_pos and initial_pos != final_pos:
            reason = "Initial optimization"
            cost_impact = best_cost - cost_history[0]
            movement_log.append(create_movement_record(item, initial_pos, final_pos, reason, cost_impact, "Initial"))
    
    return best_state, best_cost, best_eff, cost_history, perfect_history, util_history, movement_log


def create_movement_record(item, old_pos, new_pos, reason, cost_impact, iteration):
    """
    Create a standardized movement record dictionary
    
    Args:
        item: Item being moved
        old_pos: Original position (rack, shelf, positions)
        new_pos: New position (rack, shelf, positions)
        reason: Reason for move
        cost_impact: Cost change from this move
        iteration: Iteration number
        
    Returns:
        dict: Movement record
    """
    return {
        'item_id': item['id'],
        'item_name': item['name'],
        'category': item['category'],
        'size': item['size'],
        'old_rack': old_pos[0],
        'old_shelf': old_pos[1],
        'old_positions': format_positions(old_pos[2]),
        'new_rack': new_pos[0],
        'new_shelf': new_pos[1],
        'new_positions': format_positions(new_pos[2]),
        'reason': reason,
        'cost_impact': cost_impact,
        'iteration': iteration
    }


def format_positions(positions):
    """
    Format position list as human-readable string
    
    Args:
        positions: List of bin positions
        
    Returns:
        str: Formatted position string (e.g., "2-4" for [2,3,4])
    """
    if len(positions) == 1:
        return str(positions[0])
    return f"{positions[0]}-{positions[-1]}"


def determine_move_reason(problem, item, old_pos, new_pos, cost_change):
    """
    Determine the reason for an item movement
    
    Args:
        problem: Problem instance
        item: Item being moved
        old_pos: Original position
        new_pos: New position
        cost_change: Cost impact of move
        
    Returns:
        str: Reason description
    """
    # Frozen items
    if item['is_frozen'] and new_pos[0] in problem.freezer_racks and old_pos[0] not in problem.freezer_racks:
        return "Moved to freezer rack"
    
    # Category conflicts
    # ... [category conflict checking logic] ...
    
    # Weight distribution
    if new_pos[1] < old_pos[1]:  # Moved to lower shelf
        return "Better weight distribution"
    
    # Space utilization
    old_gaps = calculate_gaps(old_pos[2], problem.bins_per_shelf)
    new_gaps = calculate_gaps(new_pos[2], problem.bins_per_shelf)
    if min(new_gaps) > min(old_gaps):
        return "Improved space utilization"
    
    return "General optimization" if cost_change < 0 else "Exploratory move"


def calculate_gaps(positions, total_bins):
    """
    Calculate gaps between occupied bins
    
    Args:
        positions: List of occupied bin positions
        total_bins: Total bins per shelf
        
    Returns:
        list: Sizes of gaps between occupied bins
    """
    occupied = set(positions)
    gaps = []
    current_gap = 0
    
    for bin in range(1, total_bins + 1):
        if bin in occupied:
            if current_gap > 0:
                gaps.append(current_gap)
            current_gap = 0
        else:
            current_gap += 1
    
    if current_gap > 0:
        gaps.append(current_gap)
    
    return gaps if gaps else [0]



def generate_movement_report(initial_state, best_state, problem, filename='item_movements.csv'):
    """Generate CSV with exact format requested"""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'item_id', 'name', 'category', 'size',
            'initial_position', 'new_position'
        ])
        
        for item in problem.items:
            item_id = item['id']
            old_pos = initial_state.get(item_id, (None, None, []))
            new_pos = best_state.get(item_id, (None, None, []))
            
            if old_pos[0] and new_pos[0]:  # Only include properly placed items
                writer.writerow([
                    item_id,
                    item['name'],
                    item['category'],
                    item['size'],
                    f"({old_pos[0]},{old_pos[1]},{format_positions(old_pos[2])})",
                    f"({new_pos[0]},{new_pos[1]},{format_positions(new_pos[2])})"
                ])

def generate_heatmaps(initial_state, best_state, problem):
    """Generate before/after heatmaps"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Prepare data
    def prepare_heatmap_data(state):
        heatmap = np.zeros((problem.shelf_levels, problem.num_racks))
        for (rack, shelf, _) in state.values():
            heatmap[shelf-1][rack-1] += 1
        return heatmap
    
    # Initial state heatmap
    im1 = ax1.imshow(prepare_heatmap_data(initial_state), cmap='YlOrRd')
    ax1.set_title('Initial Item Distribution')
    ax1.set_xlabel('Rack Number')
    ax1.set_ylabel('Shelf Level')
    fig.colorbar(im1, ax=ax1)
    
    # Optimized state heatmap
    im2 = ax2.imshow(prepare_heatmap_data(best_state), cmap='YlOrRd')
    ax2.set_title('Optimized Item Distribution')
    ax2.set_xlabel('Rack Number')
    ax2.set_ylabel('Shelf Level')
    fig.colorbar(im2, ax=ax2)
    
    plt.savefig('placement_heatmaps.png')

def format_positioSns(positions):
    """Improved bin formatting"""
    if not positions:
        return ""
    if len(positions) == 1:
        return str(positions[0])
    return f"{positions[0]}-{positions[-1]}"
def generate_visualization(cost_history, perfect_history, util_history):
    """
    Generate optimization progress plots
    
    Args:
        cost_history: List of cost values over iterations
        perfect_history: List of perfect shelf counts
        util_history: List of utilization percentages
    """
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.plot(cost_history)
    plt.title('Cost Reduction Over Time')
    plt.xlabel('Iteration')
    plt.ylabel('Total Cost')
    
    plt.subplot(1, 3, 2)
    plt.plot(perfect_history)
    plt.title('Perfect Shelves Over Time')
    plt.xlabel('Iteration')
    plt.ylabel('Count')
    
    plt.subplot(1, 3, 3)
    plt.plot(util_history)
    plt.title('Space Utilization Over Time')
    plt.xlabel('Iteration')
    plt.ylabel('Utilization %')
    
    plt.tight_layout()
    plt.savefig('optimization_progress.png')


def generate_text_report(problem, best_state, best_cost, best_eff):
    """
    Generate detailed text report of final solution
    
    Args:
        problem: Problem instance
        best_state: Optimal solution state
        best_cost: Solution cost
        best_eff: Efficiency metrics
    """
    shelf_details = defaultdict(list)
    for item_id, (rack, shelf, positions) in best_state.items():
        item = next(i for i in problem.items if i['id'] == item_id)
        shelf_details[(rack, shelf)].append((item, positions))
    
    report = [
        "="*80,
        "WAREHOUSE OPTIMIZATION REPORT",
        "="*80,
        f"\nFinal Statistics:",
        f"- Total Cost: {best_cost}",
        f"- Perfect Shelves: {best_eff[0]} (fully packed)",
        f"- Good Shelves: {best_eff[1]} (<60cm unused)",
        f"- Poor Shelves: {best_eff[2]} (>150cm unused)",
        f"- Space Utilization: {best_eff[3]:.1%}",
        "\n" + "="*80,
        "SHELF DETAILS (POORLY UTILIZED SHELVES):",
        "="*80
    ]
    
    # Show worst shelves
    poor_shelves = sorted(
        [(k, v) for k, v in shelf_details.items()],
        key=lambda x: problem.shelf_length - sum(problem.box_sizes[i['size']]['width'] for i, _ in x[1]),
        reverse=True
    )[:10]  # Top 10 worst
    
    for (rack, shelf), items in poor_shelves:
        used = sum(problem.box_sizes[i['size']]['width'] for i, _ in items)
        report.append(
            f"\nRack {rack} Shelf {shelf} (Used: {used}cm/{problem.shelf_length}cm):"
        )
        for item, positions in items:
            report.append(
                f"  - ID {item['id']}: {item['name']} ({item['size']}, "
                f"{item['weight']}kg, {item['category']}) "
                f"in positions {format_positions(positions)}"
            )
    
    with open('optimization_report.txt', 'w') as f:
        f.write("\n".join(report))



if __name__ == "__main__":
    try:
        # Initialize problem
        problem = Problem('items.csv')
        
        # Get initial state before optimization
        initial_state = problem.generate_initial_state()
        
        # Run optimization
        print("Starting optimization...")
        results = simulated_annealing(
            problem,
            initial_temp=1000,
            cooling_rate=0.995,
            iterations=5000
        )
        best_state, best_cost, best_eff, *_ = results
        
        # Generate outputs
        generate_movement_report(initial_state, best_state, problem)
        generate_heatmaps(initial_state, best_state, problem)
        generate_visualization(*results[3:6])  # Existing progress plots
        generate_text_report(problem, best_state, best_cost, best_eff)
        
        print("\nOptimization complete!")
        print(f"- Final cost: {best_cost}")
        print(f"- Space utilization: {best_eff[3]:.1%}")
        print("- CSV output: item_movements.csv")
        print("- Heatmaps: placement_heatmaps.png")
        print("- Progress plots: optimization_progress.png")
        print("- Report: optimization_report.txt")
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")