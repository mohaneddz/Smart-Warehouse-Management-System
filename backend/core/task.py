import uuid
from typing import Optional

class Task:
    """Represents a task to be performed by an agent within the warehouse environment."""

    def __init__(self, goal_state: str, job: str, priority: int = 0, initial_state: str = "", hash_id: Optional[str] = None):
        """Initializes a Task instance.

        Args:
            goal_state (str): Description or identifier of the target state/location for the task.
            job (str): The type of job to be performed (e.g., 'pickup', 'dropoff', 'charge').
            priority (int, optional): The priority level of the task. Higher values might indicate higher priority
                                      (or use 1 for high as in Mixer). Defaults to 0.
            initial_state (str, optional): Description or identifier of the starting state/location. Defaults to "".
            hash_id (Optional[str], optional): A unique identifier (Primary Key) for the task.
                                               If None, a unique ID will be generated. Defaults to None.
        """
        # Use provided hash_id or generate a new UUID string if None
        self.hash_id: str = hash_id if hash_id is not None else str(uuid.uuid4())

        # Schema Attributes
        self.initial_state: str = initial_state
        self.goal_state: str = goal_state
        self.job: str = job # Could potentially be replaced/validated with an Enum later
        self.priority: int = priority

    def __str__(self) -> str:
        """Return a string representation of the task."""
        # Simple representation focusing on key details
        return f"Task(Job='{self.job}', Goal='{self.goal_state}', Priority={self.priority}, ID='{self.hash_id}')"

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (f"Task(hash_id='{self.hash_id}', initial_state='{self.initial_state}', "
                f"goal_state='{self.goal_state}', job='{self.job}', priority={self.priority})")

    def __eq__(self, other) -> bool:
        """Check if two tasks are equal based on their unique hash_id."""
        if not isinstance(other, Task):
            return NotImplemented # Standard practice for non-comparable types
        return self.hash_id == other.hash_id

    def __hash__(self) -> int:
        """Return a hash based on the task's unique hash_id."""
        # Hashing based on the primary key ensures uniqueness in sets/dicts
        return hash(self.hash_id)