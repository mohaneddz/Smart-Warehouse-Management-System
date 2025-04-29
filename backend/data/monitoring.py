import time
from typing import List
from backend.core.task import Task
from backend.core.agent_system import Agent

class Monitor:
    def __init__(self):
        self.task_log = []  # To store task updates
        self.agent_log = []  # To store agent actions
        self.event_log = []  # To store general events

    def log_event(self, event: str, details: str):
        """Logs a custom event with details (e.g., collision, start/finish)"""
        event_entry = {
            "event": event,
            "details": details,
            "timestamp": time.time()  # Use timestamp for real-time tracking
        }
        self.event_log.append(event_entry)

    def log_task(self, task: 'Task', status: str):
        """Logs task updates (started, completed, etc.)"""
        task_entry = {
            "task": task,
            "status": status,
            "timestamp": time.time()
        }
        self.task_log.append(task_entry)

    def log_agent(self, agent: 'Agent', action: str):
        """Logs actions of an agent (moving, completing a task, etc.)"""
        agent_entry = {
            "agent": agent,
            "action": action,
            "timestamp": time.time()
        }
        self.agent_log.append(agent_entry)

    def report(self):
        """Generate a summary of the monitoring logs (tasks, agents, events)"""
        return {
            "tasks": self.task_log,
            "agents": self.agent_log,
            "events": self.event_log
        }

    def get_latest(self):
        """Returns the most recent log entries for tasks, agents, and events"""
        return {
            "latest_task": self.task_log[-1] if self.task_log else None,
            "latest_agent": self.agent_log[-1] if self.agent_log else None,
            "latest_event": self.event_log[-1] if self.event_log else None
        }
