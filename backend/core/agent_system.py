import time
from queue import Queue
from typing import Set, List, Dict, Any
from core.warehouse import Node
from core.task import Task
from warehouse import Warehouse

# --- Agent Class Definition ---
class Agent:
    """Represents an agent in the warehouse system, capable of moving, setting goals, and completing tasks."""
    def __init__(self, node: 'Node', weight: float, state: str, goal: str, battery: float, agent_type: str, mixer: 'Mixer'):
        """Initializes an Agent with its node, weight, state, goal, battery, type, and mixer reference.

        Args:
            node (Node): The node where the agent is located.
            weight (float): The weight of the agent.
            state (str): The current state of the agent (e.g., 'idle', 'busy').
            goal (str): The current goal description (e.g., target node hash).
            battery (float): The current battery level of the agent.
            agent_type (str): The type designation of the agent (e.g., 'picker', 'charger').
            mixer (Mixer): The mixer instance responsible for coordination and logging.
        """
        self.node = node
        self.weight = weight
        self.state = state # Example states: 'idle', 'moving_to_task', 'performing_task', 'charging'
        self.goal = goal   # Example goals: 'Node_A', 'Task_Pickup_123', 'Charging_Station_1'
        self.battery = battery
        self.agent_type = agent_type
        self.mixer = mixer # Store the mixer reference

    def move(self, new_node: 'Node'):
        """Moves the agent to a new node and logs the action via the mixer.

        Args:
            new_node (Node): The node to move the agent to.
        """
        old_node_repr = str(self.node) # Get representation before moving
        self.node = new_node
        # Consume battery during movement (example logic, adjust as needed)
        # self.battery -= distance_cost_or_fixed_amount
        if self.mixer:
            # Log the move action using the mixer
            self.mixer.log_agent(self, f"moved from {old_node_repr} to {new_node}")

    def set_goal(self, goal: str):
        """Sets a new goal for the agent and logs the action via the mixer.

        Args:
            goal (str): The new goal to set for the agent.
        """
        self.goal = goal
        # Update agent state when a goal is set (example)
        if goal:
             self.state = 'busy' # Or more specific like 'moving_to_goal'
        else:
             self.state = 'idle'

        if self.mixer:
            # Log the goal setting action using the mixer
            self.mixer.log_agent(self, f"goal set to '{goal}', state changed to '{self.state}'")

    def complete_task(self, task: 'Task'):
        """Completes the given task, updates state, and logs the completion via the mixer.

        Args:
            task (Task): The task to complete.
        """
        # Update agent state upon completion
        self.state = 'idle'
        self.goal = "" # Clear goal after completion

        if self.mixer:
            # Log both the task completion and the agent action using the mixer
            self.mixer.log_task(task, "completed")
            self.mixer.log_agent(self, f"completed task: {task.job} (Goal: {task.goal_state}), state changed to '{self.state}'")

    def update_battery(self, change: float):
        """Updates the agent's battery level and logs if necessary."""
        self.battery += change
        self.battery = max(0.0, min(100.0, self.battery)) # Clamp between 0 and 100 (assuming percentage)
        # Optionally log significant battery events (e.g., low battery)
        # if self.battery < 20 and self.mixer:
        #    self.mixer.log_event("Low Battery", f"Agent {self} battery low: {self.battery:.1f}%")

    def __str__(self):
        """Return a simple string representation for logging."""
        # Consider adding a unique ID if agents need distinct identification beyond type/node
        return f"Agent(type={self.agent_type}, node={self.node}, state={self.state})"

    # Add __repr__ for similar reasons, often useful for debugging
    def __repr__(self):
        return (f"Agent(node={self.node!r}, weight={self.weight}, state='{self.state}', "
                f"goal='{self.goal}', battery={self.battery:.1f}, agent_type='{self.agent_type}', "
                f"mixer_exists={self.mixer is not None})") # Avoid infinitely recursing if mixer logs Agent repr

# --- Mixer Class Definition (incorporating Monitor functionality) ---

class Mixer:
    """Handles task assignment, prioritization, and logging for agents in the warehouse system."""
    def __init__(self, warehouse, agents: Set[Agent]):
        """Initializes the Mixer with a warehouse, a set of agents, and logging capabilities.

        Args:
            warehouse: The warehouse instance (type depends on your Warehouse implementation).
            agents (Set[Agent]): The set of agents managed by the mixer.
        """
        self.warehouse = warehouse
        self.tasks = Queue()  # Regular tasks queue (Queue stores dictionaries)
        self.priority_tasks = Queue()  # High-priority tasks queue (Queue stores dictionaries)
        self.agents = agents # Store the set of agent objects

        # Initialize logging lists (formerly in Monitor)
        self.task_log: List[Dict[str, Any]] = []
        self.agent_log: List[Dict[str, Any]] = []
        self.event_log: List[Dict[str, Any]] = []

        # Assign this mixer instance to all agents it manages
        # Ensures agents created before the mixer is fully initialized still get the reference
        for agent in self.agents:
            if agent.mixer is None: # Assign only if not already set
                agent.mixer = self

    def add_agent(self, agent: Agent):
        """Adds a new agent to the mixer's management and assigns the mixer reference."""
        if agent not in self.agents:
            self.agents.add(agent)
            agent.mixer = self
            self.log_event("Agent Added", f"Agent {agent} added to the system.")

    def remove_agent(self, agent: Agent):
         """Removes an agent from the mixer's management."""
         if agent in self.agents:
             self.agents.remove(agent)
             agent.mixer = None # Optional: Clear the reference
             self.log_event("Agent Removed", f"Agent {agent} removed from the system.")

    def order(self, task: Task, specific_agent: Agent = None):
        """
        Places a task in the appropriate queue. Can optionally target a specific agent.

        Args:
            task (Task): The task to queue.
            specific_agent (Agent, optional): If specified, only this agent can be assigned this task
                                              (Note: assign_task needs modification to handle this).
                                              Currently, the agent reference is stored but not strictly enforced
                                              in the basic assign_task logic provided. Defaults to None.
        """
        # Basic implementation: Store task details for any available agent matching criteria later
        # Advanced: Could store agent preference or requirement
        task_data = {
            # Store agent reference if specified, otherwise None
            'specific_agent': specific_agent,
            'goal': task.goal_state,
            'type': task.job,
            'task_obj': task # Store the task object itself for later use (e.g., completion logging)
        }

        if task.priority == 1:  # High priority tasks (priority 1 means high)
            self.priority_tasks.put(task_data)
            agent_target = f" for Agent {specific_agent}" if specific_agent else ""
            self.log_event("Task Queued", f"High-priority Task {task.job} (Goal: {task.goal_state}){agent_target} added to priority queue.")
        else:
            self.tasks.put(task_data)
            agent_target = f" for Agent {specific_agent}" if specific_agent else ""
            self.log_event("Task Queued", f"Regular Task {task.job} (Goal: {task.goal_state}){agent_target} added to regular queue.")


    def assign_task_to_agent(self, agent: Agent):
        """
        Attempts to assign a task from the queues to a specific agent if the agent is idle.

        Args:
            agent (Agent): The agent requesting a task.

        Returns:
            bool: True if a task was successfully assigned, False otherwise.
        """
        if agent.state != 'idle':
            # Optional: Log that agent is busy
            # self.log_event("Task Assignment Skipped", f"Agent {agent} is busy ({agent.state}), cannot assign task.")
            return False

        task_assigned = False
        task_info = None

        # --- Check Priority Queue ---
        # Simple approach: Check if the first item is for this agent or for anyone
        # More complex: Might need to iterate queue if specific assignments are buried
        temp_priority_list = []
        while not self.priority_tasks.empty():
            potential_task = self.priority_tasks.get()
            # Check if task is generic OR specifically for this agent
            if potential_task['specific_agent'] is None or potential_task['specific_agent'] == agent:
                task_info = potential_task
                task_assigned = True
                # Put remaining tasks back (maintaining order as much as possible)
                for item in reversed(temp_priority_list):
                    self.priority_tasks.put(item)
                temp_priority_list.clear() # Clear the temp list
                break # Found a suitable task
            else:
                # Task is for someone else, hold it temporarily
                temp_priority_list.append(potential_task)

        # If no task found yet, put back the ones checked
        if not task_assigned:
            for item in reversed(temp_priority_list):
                self.priority_tasks.put(item)

        # --- Check Regular Queue (if no priority task assigned) ---
        if not task_assigned:
            temp_regular_list = []
            while not self.tasks.empty():
                potential_task = self.tasks.get()
                if potential_task['specific_agent'] is None or potential_task['specific_agent'] == agent:
                    task_info = potential_task
                    task_assigned = True
                    for item in reversed(temp_regular_list):
                         self.tasks.put(item)
                    temp_regular_list.clear()
                    break
                else:
                    temp_regular_list.append(potential_task)

            if not task_assigned:
                 for item in reversed(temp_regular_list):
                    self.tasks.put(item)

        # --- Finalize Assignment ---
        if task_assigned and task_info:
            agent.set_goal(task_info['goal']) # This triggers agent's state change and logging
            self.log_event("Task Assigned", f"Assigned Task {task_info['type']} (Goal: {task_info['goal']}) to Agent {agent}.")
            # Optionally log task status update here if needed
            # self.log_task(task_info['task_obj'], "assigned")
            return True
        else:
             # Only log if the agent was actually idle and eligible
             if agent.state == 'idle':
                 self.log_event("Task Assignment", f"No suitable tasks available for Agent {agent}.")
             return False


    def find_idle_agent(self, agent_type: str = None) -> Agent | None:
        """Finds an idle agent, optionally matching a specific type."""
        for agent in self.agents:
            if agent.state == 'idle':
                if agent_type is None or agent.agent_type == agent_type:
                    return agent
        return None # No suitable idle agent found

    # --- Logging Methods (Moved from Monitor) ---
    def log_event(self, event: str, details: str):
        """Logs a custom event with details (e.g., collision, assignment, queue status)."""
        event_entry = {
            "event": event,
            "details": details,
            "timestamp": time.time()  # Use timestamp for real-time tracking
        }
        self.event_log.append(event_entry)
        # print(f"EVENT LOGGED: [{event}] {details}") # Optional: print logs immediately for debugging

    def log_task(self, task: 'Task', status: str):
        """Logs task updates (e.g., assigned, completed, failed)."""
        task_entry = {
            # Storing task representation or relevant details
            "task_id": task.hash_id,
            "task_job": task.job,
            "task_goal": task.goal_state,
            "task_priority": task.priority,
            "status": status,
            "timestamp": time.time()
        }
        self.task_log.append(task_entry)
        # print(f"TASK LOGGED: [Task {task.hash_id} ({task.job})] Status: {status}") # Optional print

    def log_agent(self, agent: 'Agent', action: str):
        """Logs actions or state changes of an agent."""
        agent_entry = {
            # Storing agent representation or relevant details
            # Consider adding agent ID if you implement one on the Agent class
            "agent_type": agent.agent_type,
            "agent_node": str(agent.node), # Store node representation
            "agent_state": agent.state,
            "agent_battery": f"{agent.battery:.1f}%", # Log battery state with action
            "action": action,
            "timestamp": time.time()
        }
        self.agent_log.append(agent_entry)
        # print(f"AGENT LOGGED: [Agent {agent}] Action: {action}") # Optional print

    # --- Reporting Methods (Moved from Monitor) ---

    def report(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate a summary dictionary containing all monitoring logs."""
        return {
            "tasks": self.task_log,
            "agents": self.agent_log,
            "events": self.event_log
        }

    def get_latest(self) -> Dict[str, Any | None]:
        """Returns a dictionary with the most recent log entry for each category (or None)."""
        return {
            "latest_task": self.task_log[-1] if self.task_log else None,
            "latest_agent": self.agent_log[-1] if self.agent_log else None,
            "latest_event": self.event_log[-1] if self.event_log else None
        }

    def get_queue_status(self) -> Dict[str, int]:
         """Returns the current size of the task queues."""
         return {
             "priority_tasks_count": self.priority_tasks.qsize(),
             "regular_tasks_count": self.tasks.qsize()
         }
