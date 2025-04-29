from functions.a_star import a_star_algorithm
from functions.genetic import genetic_algorithm
from functions.greedy import greedy_algorithm
from functions.simulated_annealing import simulated_annealing_algorithm
from typing import Dict, Any
import logging
from data.database import db
from models import Warehouse, Task, Agent

# Set up logging for better tracking and debugging
logging.basicConfig(level=logging.INFO)

def optimize_route(data: Dict[str, Any]) -> Dict[str, Any]:
    """Optimizes the route using the specified algorithm.

    Args:
        data (dict): Input data containing 'algorithm_type', 'warehouse_layout', 'tasks', and 'agents'.
    
    Returns:
        dict: Result of the optimization with status, algorithm used, and optimized result.
    """
    # Validate and extract parameters from the incoming data
    algorithm_type = data.get('algorithm_type', 'greedy')  # Default to greedy if not specified
    
    # Fetch warehouse layout, tasks, and agents from the database if not provided
    warehouse_layout = Warehouse.query.first()  # You can filter for a specific warehouse if necessary
    tasks = Task.query.all()
    agents = Agent.query.all()

    # Check if any essential data is missing
    if not warehouse_layout or not tasks or not agents:
        return {"status": "error", "message": "Incomplete data. Ensure 'warehouse_layout', 'tasks', and 'agents' are present."}

    # Logging for tracking
    logging.info(f"Optimization started using {algorithm_type} algorithm.")

    # Algorithm mapping
    algorithm_map = {
        'a_star': a_star_algorithm,
        'genetic': genetic_algorithm,
        'simulated_annealing': simulated_annealing_algorithm,
        'greedy': greedy_algorithm
    }

    if algorithm_type not in algorithm_map:
        return {"status": "error", "message": f"Invalid algorithm type: {algorithm_type}. Please use 'a_star', 'genetic', 'simulated_annealing', or 'greedy'."}
    
    try:
        # Call the corresponding algorithm function
        result = algorithm_map[algorithm_type](warehouse_layout.layout, tasks, agents)
        
        # Handle empty result
        if not result:
            return {"status": "error", "message": "No valid result from the optimization algorithm."}

        # Example: After optimization, you might want to update agent states or task assignments in the DB
        for agent in agents:
            agent.state = "optimized"  # Update agent state (this is just an example)
            db.session.commit()  # Commit changes to the database
        
        # Return the result of the optimization process
        return {
            "status": "success",
            "algorithm_used": algorithm_type,
            "optimized_result": result
        }
    
    except Exception as e:
        logging.error(f"Error during optimization: {str(e)}")
        return {"status": "error", "message": f"An error occurred during optimization: {str(e)}"}
