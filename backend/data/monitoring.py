import time
<<<<<<< HEAD
from typing import List, Dict, Optional
from backend.data.task import Task
from backend.data.agent import Agent
=======
from typing import List
from backend.core.task import Task
from backend.core.agent_system import Agent
>>>>>>> 44f3fed3189b8acefe8f743d628efdc4045e9242

class Monitor:
    """Singleton class responsible for logging all events, tasks, metrics, and stats."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Monitor, cls).__new__(cls)
            cls._instance.task_log: List[Dict] = []
            cls._instance.agent_log: List[Dict] = []
            cls._instance.event_log: List[Dict] = []
            cls._instance.metrics: Dict[str, List[Dict]] = {}
            cls._instance.stats: Dict[str, any] = {}
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'Monitor':
        """Get the singleton instance of the Monitor."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def log_event(self, event: str, details: str) -> None:
        """Logs a custom event with details (e.g., collision, start/finish).

        Args:
            event (str): The event to log.
            details (str): Details of the event.
        """
        event_entry = {
            "event": event,
            "details": details,
            "timestamp": time.time()
        }
        self.event_log.append(event_entry)

    def log_task(self, task: 'Task', status: str) -> None:
        """Logs task updates (started, completed, etc.).

        Args:
            task (Task): The task to log.
            status (str): The task's status (e.g., "started", "completed").
        """
        task_entry = {
            "task": task,
            "status": status,
            "timestamp": time.time()
        }
        self.task_log.append(task_entry)

    def log_agent(self, agent: 'Agent', action: str) -> None:
        """Logs actions of an agent (moving, completing a task, etc.).

        Args:
            agent (Agent): The agent performing the action.
            action (str): The action performed by the agent.
        """
        agent_entry = {
            "agent": agent,
            "action": action,
            "timestamp": time.time()
        }
        self.agent_log.append(agent_entry)

    def log_metric(self, name: str, value: float) -> None:
        """Logs a metric value.

        Args:
            name (str): The name of the metric.
            value (float): The metric value to log.
        """
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append({
            "value": value,
            "timestamp": time.time()
        })

    def update_stat(self, name: str, value: any) -> None:
        """Updates a statistic value.

        Args:
            name (str): The name of the statistic.
            value (any): The value to update.
        """
        self.stats[name] = value

    def report(self) -> Dict[str, any]:
        """Generate a summary of all logs and metrics.

        Returns:
            dict: Summary of all logs, metrics, and stats.
        """
        return {
            "tasks": self.task_log,
            "agents": self.agent_log,
            "events": self.event_log,
            "metrics": self.metrics,
            "stats": self.stats
        }

    def get_latest(self) -> Dict[str, any]:
        """Returns the most recent log entries and current stats.

        Returns:
            dict: Latest task, agent, event, metrics, and stats.
        """
        return {
            "latest_task": self.task_log[-1] if self.task_log else None,
            "latest_agent": self.agent_log[-1] if self.agent_log else None,
            "latest_event": self.event_log[-1] if self.event_log else None,
            "current_metrics": {name: values[-1] if values else None 
                                for name, values in self.metrics.items()},
            "current_stats": self.stats
        }
