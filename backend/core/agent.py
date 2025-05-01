from typing import List, Optional
from dataclasses import dataclass, field
import uuid
from core.types import AgentStatus, AgentType, IMixer, IAgent
from core.node import Node
from core.task import Task

@dataclass
class Agent(IAgent):
    """Represents an agent in the warehouse system.
    
    Attributes:
        agent_id (int): Unique identifier for the agent
        node (Node): Current node where the agent is located
        weight (float): Weight of the agent (used for priority)
        status (AgentStatus): Current status of the agent
        goal_state (str): Target state/location for the agent
        mixer (Optional[IMixer]): Reference to the global mixer instance
        path (List[Node]): Current planned path
        battery (float): Current battery level (0-100)
        agent_type (AgentType): Type of agent
    """
    agent_id: int
    node: Node
    weight: float
    status: AgentStatus = AgentStatus.IDLE
    goal_state: str = ""
    mixer: Optional[IMixer] = None
    path: List[Node] = field(default_factory=list)
    battery: float = 100.0
    agent_type: AgentType = AgentType.PICKER
    hash_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        """Initializes an Agent with its node and registers with the mixer."""
        if not self.node:
            raise ValueError("Agent must be initialized with a valid node")
            
        # Add initial node to path
        self.path.append(self.node)
        if not self.node.lock(self):
            raise RuntimeError(f"Failed to lock initial node {self.node}")
            
        # Register with the global Mixer if available
        if self.mixer:
            self.mixer.log_event('agent_creation', f"Agent {self.agent_id} created at {self.node}", self)

    def move(self, new_node: Node) -> bool:
        """Moves the agent to a new node and logs the action."""
        if not new_node:
            if self.mixer:
                self.mixer.log_event('movement_failed', "Cannot move to None node", self)
            return False
            
        # Try to lock the new node
        if not new_node.lock(self):
            if self.mixer:
                self.mixer.log_event('movement_failed', f"Failed to move to {new_node} - node locked", self)
            return False
            
        # Unlock the current node
        self.node.unlock(self)
        
        # Update node and path
        self.node = new_node
        self.path.append(new_node)
        
        # Log the movement if mixer is available
        if self.mixer:
            self.mixer.log_event('movement', f"Moved to {new_node}", self)
        return True

    def backtrack(self, steps: int = 1) -> bool:
        """Moves the agent back along its path history.
        
        Args:
            steps (int): Number of steps to backtrack
            
        Returns:
            bool: True if backtrack was successful, False otherwise
        """
        if steps <= 0:
            if self.mixer:
                self.mixer.log_event('backtrack_failed', f"Invalid number of steps: {steps}", self)
            return False
            
        if len(self.path) <= steps:
            if self.mixer:
                self.mixer.log_event('backtrack_failed', f"Not enough path history to backtrack {steps} steps", self)
            return False
            
        # Get the target node to backtrack to
        target_node = self.path[-steps-1]
        
        # Try to lock the target node
        if not target_node.lock(self):
            if self.mixer:
                self.mixer.log_event('backtrack_failed', f"Failed to backtrack to {target_node} - node locked", self)
            return False
            
        # Unlock the current node
        self.node.unlock(self)
        
        # Update node and path history
        self.node = target_node
        self.path = self.path[:-steps]
        
        # Log the backtrack if mixer is available
        if self.mixer:
            self.mixer.log_event('backtrack', f"Backtracked {steps} steps to {target_node}", self)
        return True

    def set_goal(self, goal: str) -> None:
        """Sets a new goal state for the agent."""
        if not goal:
            raise ValueError("Goal cannot be empty")
            
        self.goal_state = goal
        if self.mixer:
            self.mixer.log_event('goal_change', f"Goal set to {goal}", self)

    def complete_task(self, task: Task) -> None:
        """Completes the given task and logs the completion.
        
        Args:
            task (Task): The task to complete
        """
        if not task:
            raise ValueError("Task cannot be None")
            
        if self.mixer:
            self.mixer.log_event('task_completion', f"Completed task: {task.job} to goal {task.goal_state}", self, task)

    def get_last_node(self) -> Optional[Node]:
        """Returns the last node in the path history.
        
        Returns:
            Optional[Node]: The last node in the path history, or None if history is empty
        """
        return self.path[-1] if self.path else None

    def clear_path_history(self) -> None:
        """Clears the path history, keeping only the current node."""
        if self.path:
            current_node = self.path[-1]
            self.path = [current_node]
            
    def update_battery(self, level: float) -> None:
        """Updates the agent's battery level.
        
        Args:
            level (float): New battery level (0-100)
            
        Raises:
            ValueError: If battery level is not between 0 and 100
        """
        if not 0 <= level <= 100:
            raise ValueError("Battery level must be between 0 and 100")
        self.battery = level
        
        if self.mixer and level < 20:
            self.mixer.log_event('battery_low', f"Battery low ({level}%)", self)

    def __str__(self) -> str:
        """Returns a string representation of the agent."""
        return f"Agent({self.agent_id}, {self.status.name}, {self.node})"