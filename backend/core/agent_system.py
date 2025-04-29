from typing import List
from queue import Queue
from core.warehouse import Node
from schemas.task import Task
from data.monitoring import Monitor
from dataclasses import dataclass, field
import json
import os

@dataclass
class Agent:
    """Represents an agent in the warehouse system, capable of moving, setting goals, and completing tasks."""
    node: Node
    weight: float
    state: str
    goal: str
    path_history: List[Node] = field(default_factory=list)
    
    def __post_init__(self):
        """Initializes an Agent with its node, weight, state, goal."""
        self.monitor = Monitor.get_instance()
        # Add initial node to path history and lock it
        self.path_history.append(self.node)
        self.node.lock(self)

    def move(self, new_node: 'Node') -> bool:
        """Moves the agent to a new node and logs the action.
        
        Args:
            new_node (Node): The node to move to.
            
        Returns:
            bool: True if the move was successful, False if the target node was locked.
        """
        # Try to lock the new node
        if not new_node.lock(self):
            return False
            
        # Unlock the current node
        self.node.unlock(self)
        
        # Update node and path history
        self.node = new_node
        self.path_history.append(new_node)
        self.monitor.log_agent(self, f"moved to {new_node}")
        return True

    def backtrack(self, steps: int = 1) -> bool:
        """Moves the agent back along its path history.
        
        Args:
            steps (int): Number of steps to backtrack. Defaults to 1.
            
        Returns:
            bool: True if backtracking was successful, False if not enough history or target node is locked.
        """
        if len(self.path_history) <= steps:
            return False
            
        # Get the target node to backtrack to
        target_node = self.path_history[-steps-1]
        
        # Try to lock the target node
        if not target_node.lock(self):
            return False
            
        # Unlock the current node
        self.node.unlock(self)
        
        # Update node and path history
        self.node = target_node
        self.path_history = self.path_history[:-steps]
        self.monitor.log_agent(self, f"backtracked to {target_node}")
        return True

    def set_goal(self, goal: str):
        """Sets a new goal for the agent and logs the action."""
        self.goal = goal
        self.monitor.log_agent(self, f"goal set to {goal}")
    
    def complete_task(self, task: 'Task'):
        """Completes the given task and logs the completion."""
        self.monitor.log_task(task, "completed")
        self.monitor.log_agent(self, f"completed task: {task.job} to goal {task.goal_state}")

    def get_last_node(self) -> Node:
        """Returns the last node in the path history."""
        return self.path_history[-1] if self.path_history else None

    def clear_path_history(self):
        """Clears the path history, keeping only the current node."""
        if self.path_history:
            current_node = self.path_history[-1]
            self.path_history = [current_node]


class Mixer:
    """Handles task assignment, prioritization, and deadlock resolution for agents in the warehouse system."""
    
    def __init__(self, warehouse, agents: List[Agent]):
        """Initializes the Mixer with a warehouse and a set of agents."""
        self.warehouse = warehouse
        self.tasks = Queue()  # Regular tasks queue
        self.priority_tasks = Queue()  # High-priority tasks queue
        self.agents = agents
        self.deadlock_table = self._load_deadlock_table()

    def _load_deadlock_table(self) -> dict:
        """Loads the deadlock table from the JSON file."""
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'deadlock_table.json')
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: deadlock_table.json not found. Using default deadlock handling.")
            return {
                "deadlock_scenarios": {
                    "agent_blocked": {
                        "action": "move_agent_back",
                        "parameters": {"steps": 1}
                    }
                },
                "default_resolution": {
                    "action": "move_agent_back",
                    "parameters": {"steps": 1}
                }
            }

    def _enqueue(self, agent: Agent, task: Task):
        """Helper method to enqueue tasks based on priority."""
        queue = self.priority_tasks if task.priority == 1 else self.tasks
        queue.put({
            'agent': agent,
            'goal': task.goal_state,
            'job': task.job
        })

    def order(self, agent: Agent, task: Task):
        """Orders a task for an agent by enqueuing it into the appropriate queue."""
        self._enqueue(agent, task)

    def assign_task(self, agent: Agent):
        """Assigns tasks from the priority queue first, then from the regular queue."""
        task_assigned = False

        if not self.priority_tasks.empty():
            task = self.priority_tasks.get()
            agent.set_goal(task['goal'])
            task_assigned = True
            print(f"Assigned high-priority Task {task['job']} to Agent {agent}.")
        
        if not task_assigned and not self.tasks.empty():
            task = self.tasks.get()
            agent.set_goal(task['goal'])
            print(f"Assigned Task {task['job']} to Agent {agent}.")

    def detect_and_resolve_deadlock(self):
        """Detects deadlock and resolves it using the deadlock table."""
        blocked_agents = [agent for agent in self.agents if agent.state == "blocked"]

        if len(blocked_agents) > 0:
            # Identify deadlock scenario based on blocked agents
            deadlock_type = self.identify_deadlock_type(blocked_agents)
            scenario = self.deadlock_table["deadlock_scenarios"].get(deadlock_type)
            
            if scenario:
                print(f"Deadlock detected: {scenario['description']}")
                print(f"Resolution: {scenario['resolution']}")
                self.resolve_deadlock(deadlock_type, blocked_agents, scenario)
            else:
                # Use default resolution if scenario not found
                default = self.deadlock_table["default_resolution"]
                print(f"Deadlock detected. Using default resolution: {default['action']}")
                self.resolve_deadlock(deadlock_type, blocked_agents, default)

    def identify_deadlock_type(self, blocked_agents: List[Agent]) -> str:
        """Identifies the type of deadlock based on the blocked agents' situation."""
        if len(blocked_agents) == 1:
            return "agent_blocked"
        elif len(blocked_agents) > 1:
            return "agents_blocked"
        else:
            return "path_blocked"

    def resolve_deadlock(self, deadlock_type: str, blocked_agents: List[Agent], scenario: dict):
        """Resolves the deadlock based on the deadlock type and blocked agents."""
        action = scenario["action"]
        params = scenario.get("parameters", {})

        if action == "move_agent_back":
            self.move_agent_back(blocked_agents, params)
        elif action == "switch_agent_positions":
            self.switch_agent_positions(blocked_agents, params)
        elif action == "recalculate_path":
            self.recalculate_path(blocked_agents, params)
        elif action == "break_circular_wait":
            self.break_circular_wait(blocked_agents, params)
        elif action == "release_resources":
            self.release_resources(blocked_agents, params)

    def move_agent_back(self, agents: List[Agent], params: dict):
        """Moves a blocked agent back along its path history."""
        agent = agents[0]
        steps = params.get("steps", 1)
        
        # Try to backtrack the specified number of steps
        success = agent.backtrack(steps)
        if not success:
            print(f"Warning: Could not backtrack {steps} steps for {agent}. Not enough path history.")
            # If we can't backtrack, try to move back one step at a time
            for _ in range(steps):
                if not agent.backtrack(1):
                    break

    def switch_agent_positions(self, agents: List[Agent], params: dict):
        """Switches positions between two blocked agents."""
        max_agents = params.get("max_agents", 2)
        if len(agents) > max_agents:
            agents = agents[:max_agents]
            
        agent1, agent2 = agents
        # Store current positions
        pos1 = agent1.node
        pos2 = agent2.node
        
        # Move agents to each other's positions
        agent1.move(pos2)
        agent2.move(pos1)
        
        print(f"Switched positions between {agent1} and {agent2}.")

    def recalculate_path(self, agents: List[Agent], params: dict):
        """Recalculates the path for blocked agents."""
        algorithm = params.get("algorithm", "A*")
        max_attempts = params.get("max_attempts", 3)
        print(f"Recalculating path for {agents} using {algorithm} (max attempts: {max_attempts})")

    def break_circular_wait(self, agents: List[Agent], params: dict):
        """Breaks circular wait by moving the lowest weight agent back."""
        priority = params.get("priority", "lowest_weight")
        if priority == "lowest_weight":
            agent = min(agents, key=lambda a: a.weight)
            self.move_agent_back([agent], {"steps": 1})
            print(f"Broke circular wait by moving lowest weight agent: {agent}")

    def release_resources(self, agents: List[Agent], params: dict):
        """Releases and reacquires resources for deadlocked agents."""
        timeout = params.get("timeout", 5)
        retry_interval = params.get("retry_interval", 1)
        print(f"Releasing resources for {agents} (timeout: {timeout}s, retry interval: {retry_interval}s)")
