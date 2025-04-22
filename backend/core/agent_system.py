from queue import Queue
from typing import Set
from core.warehouse import Node
from schemas.task import Task
from core.warehouse import Node

class Agent:
    """Represents an agent in the warehouse system, capable of moving, setting goals, and completing tasks."""
    def __init__(self, node: 'Node', weight: float, state: str, goal: str, mixer=None, monitor=None):
        """Initializes an Agent with its node, weight, state, goal, and optional mixer and monitor.

        Args:
            node (Node): The node where the agent is located.
            weight (float): The weight of the agent.
            state (str): The current state of the agent.
            goal (str): The goal of the agent.
            mixer: Optional mixer instance.
            monitor: Optional monitor instance to log actions.
        """
        self.node = node
        self.weight = weight
        self.state = state
        self.goal = goal
        self.mixer = mixer
        self.monitor = monitor  # The monitor instance to log actions

    def move(self, new_node: 'Node'):
        """Moves the agent to a new node and logs the action if a monitor is present.

        Args:
            new_node (Node): The node to move the agent to.
        """
        self.node = new_node
        if self.monitor:
            self.monitor.log_agent(self, f"moved to {new_node}")

    def set_goal(self, goal: str):
        """Sets a new goal for the agent and logs the action if a monitor is present.

        Args:
            goal (str): The new goal to set for the agent.
        """
        self.goal = goal
        if self.monitor:
            self.monitor.log_agent(self, f"goal set to {goal}")
    
    def complete_task(self, task: 'Task'):
        """Completes the given task and logs the completion if a monitor is present.

        Args:
            task (Task): The task to complete.
        """
        if self.monitor:
            self.monitor.log_task(task, "completed")
            self.monitor.log_agent(self, f"completed task: {task.job} to goal {task.goal_state}")

class Mixer:
    """Handles task assignment and prioritization for agents in the warehouse system."""
    def __init__(self, warehouse, agents: Set[Agent]):
        """Initializes the Mixer with a warehouse and a set of agents.

        Args:
            warehouse: The warehouse instance.
            agents (Set[Agent]): The set of agents managed by the mixer.
        """
        self.warehouse = warehouse
        self.tasks = Queue()  # Regular tasks queue
        self.priority_tasks = Queue()  # High-priority tasks queue
        self.agents = agents

    def order(self, agent: Agent, task: Task):
        """Assigns a task to an agent and places it in the appropriate queue based on priority.

        Args:
            agent (Agent): The agent to assign the task to.
            task (Task): The task to assign.
        """
        if task.priority == 1:  # High priority tasks (priority 1 means high)
            self.priority_tasks.put({
                'agent': agent,
                'goal': task.goal_state,
                'type': task.job
            })
        else:
            self.tasks.put({
                'agent': agent,
                'goal': task.goal_state,
                'type': task.job
            })

    def assign_task(self, agent: Agent):
        """Assigns tasks from the priority queue first, then from the regular queue to the given agent.

        Args:
            agent (Agent): The agent to assign a task to.
        """
        task_assigned = False

        # Try assigning from the priority queue first
        if not self.priority_tasks.empty():
            task = self.priority_tasks.get()
            agent.set_goal(task['goal'])
            task_assigned = True
            print(f"Assigned high-priority Task {task['type']} to Agent {agent}.")
        
        # If no high-priority tasks, assign from the regular queue
        if not task_assigned and not self.tasks.empty():
            task = self.tasks.get()
            agent.set_goal(task['goal'])
            print(f"Assigned Task {task['type']} to Agent {agent}.")
