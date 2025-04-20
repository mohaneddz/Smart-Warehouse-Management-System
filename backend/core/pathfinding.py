import numpy as np
from typing import List, Tuple, Optional
import heapq

class PathfindingSimulation:
    """Simulates pathfinding on a grid with start, goal, and obstacles."""
    def __init__(self, grid_size: Tuple[int, int] = (10, 10)):
        """Initializes the simulation grid, start, goal, and obstacles.

        Args:
            grid_size (Tuple[int, int], optional): Size of the grid. Defaults to (10, 10).
        """
        self.grid_size = grid_size
        self.grid = np.zeros(grid_size, dtype=int)
        self.start = None
        self.goal = None
        self.obstacles = set()
        
    def set_start(self, position: Tuple[int, int]):
        """Set the start position on the grid.

        Args:
            position (Tuple[int, int]): The (x, y) coordinates for the start.
        """
        if self._is_valid_position(position):
            self.start = position
            self.grid[position] = 2  # 2 represents start
            
    def set_goal(self, position: Tuple[int, int]):
        """Set the goal position on the grid.

        Args:
            position (Tuple[int, int]): The (x, y) coordinates for the goal.
        """
        if self._is_valid_position(position):
            self.goal = position
            self.grid[position] = 3  # 3 represents goal
            
    def add_obstacle(self, position: Tuple[int, int]):
        """Add an obstacle at the given position.

        Args:
            position (Tuple[int, int]): The (x, y) coordinates for the obstacle.
        """
        if self._is_valid_position(position):
            self.obstacles.add(position)
            self.grid[position] = 1  # 1 represents obstacle
            
    def _is_valid_position(self, position: Tuple[int, int]) -> bool:
        """Check if a position is valid and not an obstacle.

        Args:
            position (Tuple[int, int]): The (x, y) coordinates to check.
        Returns:
            bool: True if valid, False otherwise.
        """
        x, y = position
        return (0 <= x < self.grid_size[0] and 
                0 <= y < self.grid_size[1] and 
                position not in self.obstacles)
                
    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Calculate the Manhattan distance between two points.

        Args:
            a (Tuple[int, int]): First point.
            b (Tuple[int, int]): Second point.
        Returns:
            float: Manhattan distance.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
    def find_path(self) -> Optional[List[Tuple[int, int]]]:
        """Find a path from start to goal using greedy best-first search.

        Returns:
            Optional[List[Tuple[int, int]]]: The path as a list of coordinates, or None if not found.
        """
        if not self.start or not self.goal:
            return None
            
        frontier = []
        heapq.heappush(frontier, (0, self.start))
        came_from = {self.start: None}
        
        while frontier:
            _, current = heapq.heappop(frontier)
            
            if current == self.goal:
                break
                
            for next_pos in self._get_neighbors(current):
                if next_pos not in came_from:
                    priority = self._heuristic(next_pos, self.goal)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current
                    
        return self._reconstruct_path(came_from)
        
    def _get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions for a given position.

        Args:
            pos (Tuple[int, int]): The (x, y) coordinates.
        Returns:
            List[Tuple[int, int]]: List of valid neighbor positions.
        """
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (x + dx, y + dy)
            if self._is_valid_position(new_pos):
                neighbors.append(new_pos)
        return neighbors
        
    def _reconstruct_path(self, came_from: dict) -> List[Tuple[int, int]]:
        """Reconstruct the path from start to goal.

        Args:
            came_from (dict): Dictionary mapping positions to their predecessors.
        Returns:
            List[Tuple[int, int]]: The reconstructed path.
        """
        current = self.goal
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path