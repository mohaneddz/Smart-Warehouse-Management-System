from typing import List, Dict, Optional, Any
from queue import Queue
from core.task import Task
import json
import os
from datetime import datetime
import uuid
from core.agent import Agent
from core.types import IMixer, IAgent, ITask

class Mixer(IMixer):
    """Handles task assignment, prioritization, and monitoring for agents in the warehouse system.
    Also plays the role of Monitor.
    
    Attributes:
        warehouse (Dict[str, Any]): Reference to the warehouse configuration
        tasks (Queue): Regular tasks queue
        priority_tasks (Queue): High-priority tasks queue
        agents (List[Agent]): List of agents in the system
    """
    
    _instance = None
    LOG_BATCH_SIZE = 100  # Number of logs to accumulate before saving
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Mixer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, warehouse: Any = None, agents: List[IAgent] = None):
        if self._initialized:
            return
            
        self.warehouse = warehouse  # FK
        self.tasks = Queue()  # Regular tasks queue
        self.priority_tasks = Queue()  # High-priority tasks queue
        self.agents = agents or []  # FK
        self.logs = []  # List to store all system logs
        self._log_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'logs')
        self._ensure_log_directory()
        self._initialized = True

    def _ensure_log_directory(self) -> None:
        """Ensures the log directory exists."""
        os.makedirs(self._log_file_path, exist_ok=True)

    def _get_log_file_path(self) -> str:
        """Returns the path to the current log file."""
        timestamp = datetime.now().strftime("%Y%m%d")
        return os.path.join(self._log_file_path, f"warehouse_logs_{timestamp}.json")

    def _save_logs(self) -> None:
        """Saves the current logs to a file."""
        if not self.logs:
            return

        log_file = self._get_log_file_path()
        try:
            # Read existing logs if file exists
            existing_logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    existing_logs = json.load(f)

            # Append new logs
            existing_logs.extend(self.logs)
            
            # Save all logs
            with open(log_file, 'w') as f:
                json.dump(existing_logs, f, indent=2)
            
            # Clear the in-memory logs
            self.logs = []
            
        except Exception as e:
            print(f"Error saving logs: {e}")

    def log_event(self, event_type: str, message: str, agent: Optional[IAgent] = None, task: Optional[ITask] = None) -> None:
        """Logs an event in the system and saves logs if batch size is reached.
        
        Args:
            event_type (str): Type of event (e.g., 'movement', 'task', 'deadlock')
            message (str): Description of the event
            agent (Agent, optional): Agent involved in the event
            task (Task, optional): Task involved in the event
        """
        log_entry = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'message': message,
            'agent_id': agent.hash_id if agent else None,
            'task_id': task.hash_id if task else None
        }
        self.logs.append(log_entry)
        print(f"[{log_entry['timestamp']}] {event_type}: {message}")

        # Save logs if batch size is reached
        if len(self.logs) >= self.LOG_BATCH_SIZE:
            self._save_logs()

    def get_logs(self, event_type: Optional[str] = None, agent_id: Optional[str] = None, task_id: Optional[str] = None) -> List[Dict]:
        """Retrieves logs based on filters.
        
        Args:
            event_type (str, optional): Filter by event type
            agent_id (str, optional): Filter by agent ID
            task_id (str, optional): Filter by task ID
            
        Returns:
            List[dict]: Filtered log entries
        """
        filtered_logs = self.logs
        if event_type:
            filtered_logs = [log for log in filtered_logs if log['type'] == event_type]
        if agent_id:
            filtered_logs = [log for log in filtered_logs if log['agent_id'] == agent_id]
        if task_id:
            filtered_logs = [log for log in filtered_logs if log['task_id'] == task_id]
        return filtered_logs

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

    def assign_task(self, agent: IAgent) -> None:
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
