from typing import Dict, Optional, List, TYPE_CHECKING
from math import sqrt
from core.node import Node

if TYPE_CHECKING:
    from core.agent_system import Agent
    from data.monitoring import Monitor

class Task:
    """Represents a task with an initial state, goal state, job type, and priority."""
    def __init__(self, initial_state: str, goal_state: str, job: str, priority: int = 0):
        """Initializes a Task with states, job, and priority.

        Args:
            initial_state (str): The starting state for the task.
            goal_state (str): The goal state for the task.
            job (str): The type of job/task.
            priority (int, optional): Task priority (lower is higher priority). Defaults to 0.
        """
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.job = job
        self.priority = priority

    def assign_task(self, agent: 'Agent', monitor: 'Monitor'):
        """Assign the task to an agent and log the event.

        Args:
            agent (Agent): The agent to assign the task to.
            monitor (Monitor): The monitor to log the assignment.
        """
        if monitor:
            monitor.log_task(self, "assigned to agent")
        agent.set_goal(self.goal_state)


class WarehouseMap:
    """Manages the warehouse layout, tasks, and agents."""
    def __init__(self, nodes: Optional[Dict[str, Node]] = None):
        """Initializes the warehouse map with nodes, agents, and tasks.

        Args:
            nodes (Optional[Dict[str, Node]], optional): Dictionary of nodes. Defaults to None.
        """
        if nodes is None:
            from utils.helpers import load_nodes_from_json
            nodes = load_nodes_from_json("data/facts/nodes.json")

        self.map = nodes or {}  # Dictionary of nodes in the warehouse
        self.goal: Optional[Node] = None  # Goal node for pathfinding algorithms
        self.agents: Dict[str, 'Agent'] = {}  # Dictionary of agents in the warehouse
        self.tasks: List[Task] = []  

    def get_distance(self, n1: Node, n2: Node) -> float:
        """Calculates Euclidean distance between two nodes.

        Args:
            n1 (Node): First node.
            n2 (Node): Second node.
        Returns:
            float: Euclidean distance.
        """
        return sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2)

    def get_actions(self, node: Node) -> Dict[str, float]:
        """Returns a dictionary of possible actions (neighboring nodes) from a given node.

        Args:
            node (Node): The node to get actions from.
        Returns:
            Dict[str, float]: Neighboring nodes and their distances.
        """
        return {k: v for k, v in node.neighbours.items() if k != node.parent}

    def assign_heuristics(self):
        """Assigns heuristic values to nodes based on the goal location."""
        if not self.goal:
            return
        for node in self.map.values():
            node.set_heuristic(self.get_distance(node, self.goal))

    def add_task(self, task: Task):
        """Adds a task to the warehouse task list.

        Args:
            task (Task): The task to add.
        """
        self.tasks.append(task)

    def assign_task(self, agent: 'Agent'):
        """Assigns the highest priority task to an agent.

        Args:
            agent (Agent): The agent to assign the task to.
        """
        if self.tasks:
            # Sort tasks by priority (lower priority value means higher priority)
            self.tasks.sort(key=lambda x: x.priority)
            task = self.tasks.pop(0)  # Get the highest priority task
            agent.set_goal(task.goal_state)
            print(f"Assigned Task {task.job} to Agent {agent}.")
        else:
            print(f"No tasks available for Agent {agent}.")

    def __repr__(self):
        """String representation of the Warehouse map."""
        return f"WarehouseMap(Agents: {len(self.agents)}, Tasks: {len(self.tasks)})"
