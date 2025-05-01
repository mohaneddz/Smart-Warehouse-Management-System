from typing import Optional
import uuid
from core.types import TaskType, ITask

class Task(ITask):
    """Represents a task to be performed by an agent within the warehouse environment.
    
    Attributes:
        hash_id (str): Unique identifier for the task
        initial_state (str): Starting state/location of the task
        goal_state (str): Target state/location for the task
        job (TaskType): Type of job to be performed
        priority (int): Priority level of the task (0 = normal, 1 = high)
    """

    def __init__(self, goal_state: str, job: TaskType, priority: int = 0, initial_state: str = "", hash_id: Optional[str] = None):
        """Initializes a Task instance.

        Args:
            goal_state (str): Description or identifier of the target state/location for the task.
            job (TaskType): The type of job to be performed
            priority (int, optional): The priority level of the task (0 = normal, 1 = high)
            initial_state (str, optional): Description or identifier of the starting state/location
            hash_id (Optional[str], optional): A unique identifier (Primary Key) for the task

        Raises:
            ValueError: If goal_state or job is empty, or if priority is negative
        """
        if not goal_state:
            raise ValueError("Goal state cannot be empty")
        if not job:
            raise ValueError("Job type cannot be empty")
        if priority < 0:
            raise ValueError("Priority cannot be negative")

        self.hash_id: str = hash_id if hash_id is not None else str(uuid.uuid4())
        self.initial_state: str = initial_state
        self.goal_state: str = goal_state
        self.job: TaskType = job
        self.priority: int = priority

    def __str__(self) -> str:
        """Return a string representation of the task.
        
        Returns:
            str: A human-readable string representation of the task
        """
        return f"Task(Job='{self.job.name}', Goal='{self.goal_state}', Priority={self.priority}, ID='{self.hash_id}')"

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging.
        
        Returns:
            str: A detailed string representation of the task
        """
        return (f"Task(hash_id='{self.hash_id}', initial_state='{self.initial_state}', "
                f"goal_state='{self.goal_state}', job='{self.job.name}', priority={self.priority})")

    def __eq__(self, other: object) -> bool:
        """Check if two tasks are equal based on their unique hash_id.
        
        Args:
            other (object): The object to compare with
            
        Returns:
            bool: True if the tasks are equal, False otherwise
        """
        if not isinstance(other, Task):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __hash__(self) -> int:
        """Return a hash based on the task's unique hash_id.
        
        Returns:
            int: A hash value computed from the task's hash_id
        """
        return hash(self.hash_id)