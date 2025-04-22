from functions.a_star import a_star_algorithm
from functions.genetic import genetic_algorithm
from functions.greedy import greedy_algorithm
from functions.simulated_annealing import simulated_annealing_algorithm

def optimize_route(data):
    # Validate and extract parameters from the incoming data
    algorithm_type = data.get('algorithm_type', 'greedy')  # Default to greedy if not specified
    warehouse_layout = data.get('warehouse_layout', {})
    tasks = data.get('tasks', [])
    agents = data.get('agents', [])

    # Validate required fields
    if not warehouse_layout or not tasks or not agents:
        return {"status": "error", "message": "Incomplete data. Ensure 'warehouse_layout', 'tasks', and 'agents' are provided."}

    # Based on the algorithm type, run the respective function
    if algorithm_type == 'a_star':
        result = a_star_algorithm(warehouse_layout, tasks, agents)
    elif algorithm_type == 'genetic':
        result = genetic_algorithm(warehouse_layout, tasks, agents)
    elif algorithm_type == 'simulated_annealing':
        result = simulated_annealing_algorithm(warehouse_layout, tasks, agents)
    elif algorithm_type == 'greedy':  # Default to greedy if none specified
        result = greedy_algorithm(warehouse_layout, tasks, agents)
    else:
        return {"status": "error", "message": f"Invalid algorithm type: {algorithm_type}. Please use 'a_star', 'genetic', 'simulated_annealing', or 'greedy'."}

    # Return the result of the optimization process
    return {
        "status": "success",
        "algorithm_used": algorithm_type,
        "optimized_result": result
    }
