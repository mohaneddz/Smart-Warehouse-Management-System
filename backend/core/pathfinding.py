from typing import List, Dict, Optional
from queue import PriorityQueue
from core.node import Node

def manhattan_distance(node1: Node, node2: Node) -> float:
    """Calculates the Manhattan distance between two nodes."""
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)

def a_star_search(start: Node, goal: Node, heuristics: Dict[str, float]) -> Optional[List[Node]]:
    """Finds the optimal path from start to goal using A* search with heuristics.
    
    Args:
        start (Node): Starting node
        goal (Node): Goal node
        heuristics (Dict[str, float]): Heuristic values for each node
        
    Returns:
        Optional[List[Node]]: List of nodes forming the path, or None if no path exists
    """
    # Priority queue for open nodes (f_score, node)
    open_set = PriorityQueue()
    open_set.put((0, start))
    
    # Dictionary to store the most efficient previous step
    came_from = {}
    
    # Dictionary to store the cost from start to each node
    g_score = {start.name: 0}
    
    # Dictionary to store the total estimated cost from start to goal through each node
    f_score = {start.name: heuristics[start.name]}
    
    # Set of nodes already evaluated
    closed_set = set()
    
    while not open_set.empty():
        current = open_set.get()[1]
        
        if current == goal:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path
            
        closed_set.add(current)
        
        for neighbor, distance in current.neighbours.items():
            if neighbor in closed_set:
                continue
                
            # Calculate tentative g_score
            tentative_g_score = g_score[current.name] + distance
            
            if neighbor.name not in g_score or tentative_g_score < g_score[neighbor.name]:
                # This path to neighbor is better than any previous one
                came_from[neighbor] = current
                g_score[neighbor.name] = tentative_g_score
                f_score[neighbor.name] = tentative_g_score + heuristics[neighbor.name]
                
                if neighbor not in [item[1] for item in open_set.queue]:
                    open_set.put((f_score[neighbor.name], neighbor))
    
    # No path found
    return None

def find_path(start: Node, goal: Node, heuristics: Dict[str, float]) -> List[Node]:
    """Finds a path from start to goal using A* search.
    
    Args:
        start (Node): Starting node
        goal (Node): Goal node
        heuristics (Dict[str, float]): Heuristic values for each node
        
    Returns:
        List[Node]: List of nodes forming the path
        
    Raises:
        ValueError: If no path exists between start and goal
    """
    path = a_star_search(start, goal, heuristics)
    if path is None:
        raise ValueError(f"No path found from {start.name} to {goal.name}")
    return path 