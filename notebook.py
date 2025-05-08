from enum import Enum
from typing import Protocol, List, Optional, Dict, Tuple, Any
from datetime import datetime
from dataclasses import dataclass

# Enums -----------------------------------------------------------

class AgentStatus(Enum):
    """Possible states of an agent."""
    IDLE = "IDLE"
    MOVING = "MOVING"
    WORKING = "WORKING"
    CHARGING = "CHARGING"
    ERROR = "ERROR"

class AgentType(Enum):
    """Types of agents in the warehouse."""
    PICKER = "PICKER"
    TRANSPORTER = "TRANSPORTER"

class NodeType(Enum):
    """Types of nodes in the warehouse."""
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    NORMAL = "NORMAL"
    CENTER = "CENTER"

class TaskType(Enum):
    """Types of tasks in the warehouse."""
    PICK = "PICK"
    PLACE = "PLACE"
    MOVE = "MOVE"
    CHARGE = "CHARGE"

class TaskStatus(Enum):
    """Possible states of a task."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

# Interfaces -----------------------------------------------------------

class INode(Protocol):
    """Protocol defining the interface for a Node."""
    hash: str
    x: float
    y: float
    neighbours: Dict['INode', float]
    heuristic: float
    type: NodeType
    locked: bool
    is_goal: bool

class ITask(Protocol):
    """Protocol defining the interface for a Task."""
    hash_id: str
    initial_state: str
    goal_state: str
    job: TaskType
    priority: int

class IAgent(Protocol):
    """Interface for agent objects."""
    agent_id: int
    node: 'NodeType'
    weight: float
    status: AgentStatus
    goal_state: str
    mixer: Optional['IMixer']
    path: List['NodeType']
    battery: float
    agent_type: AgentType
    hash_id: str

class IMixer(Protocol):
    """Interface for mixer objects."""
    warehouse: 'IWarehouse'
    tasks: List['TaskType']
    priority_tasks: List['TaskType']
    agents: Dict[str, IAgent]
    logs: List[str]
    log_file: str

    def log_event(self, event_type: str, message: str, agent: Optional[IAgent] = None, task: Optional['Task'] = None) -> None:
        """Logs an event in the system."""
        pass

class IWarehouse(Protocol):
    """Interface for warehouse objects."""
    name: str
    location: str
    width: float
    length: float
    height: float
    racks: List['Rack']
    shelves: List['Shelf']
    items: Dict[str, 'ItemInformation']
    transactions: List['Transaction']

# Data Models -----------------------------------------------------------

@dataclass
class ItemInformation:
    """Data model for storing item information in the warehouse system."""
    item_id: str  # PK
    name: str
    category: str
    box_weight: float
    box_height: float
    box_price: float
    expiry: Optional[datetime]
    counter: int = 0

@dataclass
class ItemShelf:
    """Data model for mapping items to shelves in the warehouse."""
    item_id: str  # FK
    shelf_id: str  # FK
    order_in_shelf: int
    addition_date: datetime
    accessible_nodes: List[str]
    finale: bool = False

@dataclass
class Rack:
    """Data model for storage racks in the warehouse."""
    rack_id: str  # PK
    is_frozen: bool
    current_capacity: float
    start_coords: Tuple[float, float]  # [x,y]
    center_coords: Tuple[float, float]  # [x,y]
    end_coords: Tuple[float, float]    # [x,y]

@dataclass
class Shelf:
    """Data model for shelves within racks."""
    shelf_id: str  # PK
    rack_id: str   # FK -> Rack
    z_level: float
    current_weight: float
    is_locked: bool = False

@dataclass
class Transaction:
    """Data model for warehouse transactions."""
    transaction_id: str  # PK
    transaction_type: str
    item_id: str  # FK -> ItemInformation
    quantity: int
    date: datetime

@dataclass
class FactsTable:
    """Data model for warehouse configuration and constraints."""
    name: str
    location: str
    warehouse_width: float
    warehouse_length: float
    warehouse_height: float
    n_racks: int
    n_shelfs_per_rack: int
    shelfs_max_height: List[float]  # [z1,z2..]
    shelf_max_width: float
    item_length: float

    warehouse_height: float
    n_racks: int
    n_shelfs_per_rack: int
    shelfs_max_height: List[float]  # [z1,z2..]
    shelf_max_width: float
    item_length: float

from typing import Optional
import uuid

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

from typing import Dict, Optional, List
from enum import Enum, auto
from dataclasses import dataclass, field

@dataclass
class Node:
    """Represents a node in the warehouse grid.
    
    Attributes:
        x (int): X coordinate
        y (int): Y coordinate
        node_type (NodeType): Type of the node
        name (str): Name of the node (e.g., "A1", "B2")
        neighbours (Dict[Node, float]): Dictionary of neighboring nodes and their distances
        locked_by (Optional[str]): ID of the agent that has locked this node
    """
    x: int
    y: int
    node_type: NodeType
    name: str
    neighbours: Dict['Node', float] = field(default_factory=dict)
    locked_by: Optional[str] = None
    locked: bool = False
    is_goal: bool = False

    def add_neighbor(self, node: 'Node', distance: float = 1.0) -> None:
        """Adds a neighboring node with the given distance."""
        self.neighbours[node] = distance
        node.neighbours[self] = distance

    def is_locked(self) -> bool:
        """Returns whether the node is currently locked by an agent."""
        return self.locked

    def lock(self, agent_id: str) -> bool:
        """Attempts to lock the node for an agent.
        
        Args:
            agent_id (str): ID of the agent attempting to lock the node
            
        Returns:
            bool: True if the node was successfully locked, False otherwise
        """
        if not self.is_locked():
            self.locked = True
            self.locked_by = agent_id
            return True
        return False

    def unlock(self, agent_id: str) -> bool:
        """Attempts to unlock the node for an agent.
        
        Args:
            agent_id (str): ID of the agent attempting to unlock the node
            
        Returns:
            bool: True if the node was successfully unlocked, False otherwise
        """
        if self.locked and self.locked_by == agent_id:
            self.locked = False
            self.locked_by = None
            return True
        return False

    def __hash__(self) -> int:
        """Returns a hash value for the node."""
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        """Checks if two nodes are equal."""
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        """Returns a string representation of the node."""
        return f"{self.name} ({self.x}, {self.y})"

    def get_locking_agent(self) -> Optional[str]:
        """Gets the agent that currently has the node locked.

        Returns:
            Optional[str]: The agent that locked the node, or None if the node is not locked
        """
        return self.locked_by

    def set_type(self, node_type: NodeType) -> None:
        """Sets the type of the node.

        Args:
            node_type (NodeType): The new type for the node
        """
        self.node_type = node_type

    def set_goal(self, is_goal: bool = True) -> None:
        """Sets whether this node is a goal node.

        Args:
            is_goal (bool, optional): Whether this is a goal node. Defaults to True.
        """
        self.is_goal = is_goal


from typing import Dict, Optional, List, TYPE_CHECKING
from math import sqrt
from dataclasses import dataclass, field
import uuid
import json
import os

if TYPE_CHECKING:
    from backend.core.agent import Agent

@dataclass
class Warehouse:
    """Represents the warehouse environment.
    
    Attributes:
        facts (FactsTable): Warehouse configuration and facts
        nodes (Dict[str, Node]): All nodes in the warehouse, keyed by node name
        racks (Dict[str, Rack]): All racks in the warehouse, keyed by rack ID
        shelves (Dict[str, Shelf]): All shelves in the warehouse, keyed by shelf ID
        agents (Dict[str, Agent]): All agents in the warehouse
        tasks (List[Task]): All tasks in the warehouse
        goal (Optional[Node]): Current goal node for pathfinding
    """
    facts: FactsTable
    nodes: Dict[str, Node] = field(default_factory=dict)
    racks: Dict[str, Rack] = field(default_factory=dict)
    shelves: Dict[str, Shelf] = field(default_factory=dict)
    agents: Dict[str, 'Agent'] = field(default_factory=dict)
    tasks: List[Task] = field(default_factory=list)
    goal: Optional[Node] = None
    
    @classmethod
    def create_default(cls) -> 'Warehouse':
        """Creates a default warehouse configuration for testing/example purposes."""
        # Create facts table
        facts = FactsTable(
            name="Example Warehouse",
            location="Test Location",
            warehouse_width=20.0,
            warehouse_length=30.0,
            warehouse_height=5.0,
            n_racks=4,
            n_shelfs_per_rack=3,
            shelfs_max_height=[1.0, 2.0, 3.0],
            shelf_max_width=2.0,
            item_length=0.5
        )
        
        # Create a 5x5 grid of nodes
        nodes: Dict[str, Node] = {}
        for i in range(5):
            for j in range(5):
                node_hash = f"node_{i}_{j}"
                nodes[node_hash] = Node(float(i), float(j), node_hash, {}, 0.0)
        
        # Connect nodes (up, down, left, right)
        for i in range(5):
            for j in range(5):
                current = nodes[f"node_{i}_{j}"]
                neighbors = {}
                
                # Check all adjacent positions
                for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 5 and 0 <= nj < 5:
                        neighbor = nodes[f"node_{ni}_{nj}"]
                        neighbors[neighbor] = 1.0
                
                current.neighbours = neighbors
        
        # Create racks
        racks: Dict[str, Rack] = {}
        rack_positions = [(1, 1), (1, 3), (3, 1), (3, 3)]
        for i, (x, y) in enumerate(rack_positions):
            rack_id = f"rack_{i+1}"
            racks[rack_id] = Rack(
                rack_id=rack_id,
                is_frozen=False,
                current_capacity=0.0,
                start_coords=(float(x-0.5), float(y-0.5)),
                center_coords=(float(x), float(y)),
                end_coords=(float(x+0.5), float(y+0.5))
            )
            # Mark the node as a center
            nodes[f"node_{x}_{y}"].set_type(NodeType.CENTER)
        
        # Create shelves
        shelves: Dict[str, Shelf] = {}
        for rack_id, rack in racks.items():
            for level in range(3):
                shelf_id = f"{rack_id}_shelf_{level+1}"
                shelves[shelf_id] = Shelf(
                    shelf_id=shelf_id,
                    rack_id=rack_id,
                    z_level=float(level + 1),
                    current_weight=0.0,
                    is_locked=False
                )
        
        return cls(facts=facts, nodes=nodes, racks=racks, shelves=shelves)
    
    @classmethod
    def load_from_json(cls, json_path: str) -> 'Warehouse':
        """Loads warehouse configuration from a JSON file.
        
        Args:
            json_path (str): Path to the JSON configuration file
            
        Returns:
            Warehouse: A new Warehouse instance with the loaded configuration
            
        Raises:
            ValueError: If the JSON file is invalid or missing required fields
        """
        try:
            with open(json_path, 'r') as f:
                config = json.load(f)
                
            # Create default facts table
            facts = FactsTable(
                name="Warehouse",
                location="Default",
                warehouse_width=20.0,  # meters
                warehouse_length=30.0,  # meters
                warehouse_height=5.0,   # meters
                n_racks=5,             # number of racks
                n_shelfs_per_rack=3,   # shelves per rack
                shelfs_max_height=[1.0, 2.0, 3.0],  # height of each shelf level
                shelf_max_width=2.0,   # meters
                item_length=0.5        # meters
            )
                
            # Create warehouse instance with facts
            warehouse = cls(facts=facts)
            
            # Create nodes
            nodes = {}
            for node_name, node_data in config['nodes'].items():
                # Convert node type string to enum
                try:
                    node_type = NodeType[node_data['type']]
                except KeyError:
                    raise ValueError(f"Invalid node type: {node_data['type']}")
                    
                node = Node(
                    x=node_data['x'],
                    y=node_data['y'],
                    node_type=node_type,
                    name=node_name
                )
                nodes[node_name] = node
                
            # Create connections
            for node1_name, node2_name in config['connections']:
                node1 = nodes[node1_name]
                node2 = nodes[node2_name]
                node1.add_neighbor(node2)
                node2.add_neighbor(node1)
                
            warehouse.nodes = list(nodes.values())
            
            # Create racks and shelves
            for rack_id, rack_data in config['racks'].items():
                center_node = nodes[rack_data['center']]
                rack = Rack(
                    rack_id=rack_id,
                    is_frozen=False,
                    current_capacity=0.0,
                    start_coords=(center_node.x - 0.5, center_node.y - 0.5),
                    center_coords=(center_node.x, center_node.y),
                    end_coords=(center_node.x + 0.5, center_node.y + 0.5)
                )
                warehouse.racks.append(rack)
                
                # Create shelves for the rack
                for shelf_id in rack_data['shelves']:
                    shelf = Shelf(
                        shelf_id=shelf_id,
                        rack_id=rack.rack_id,
                        z_level=len(rack.shelves) + 1,
                        current_weight=0.0,
                        is_locked=False
                    )
                    warehouse.shelves.append(shelf)
                    
            return warehouse
            
        except Exception as e:
            raise ValueError(f"Failed to load warehouse from {json_path}: {str(e)}")
    
    def get_node(self, x: int, y: int) -> Optional[Node]:
        """Returns the node at the given coordinates."""
        for node in self.nodes.values():
            if node.x == x and node.y == y:
                return node
        return None

    def get_node_by_name(self, name: str) -> Optional[Node]:
        """Returns the node with the given name."""
        return self.nodes.get(name)

    def get_rack_at_node(self, node: Node) -> Optional[Rack]:
        """Returns the rack at the given node."""
        for rack in self.racks.values():
            if rack.center_node == node:
                return rack
        return None

    def get_shelves_for_rack(self, rack: Rack) -> List[Shelf]:
        """Returns all shelves in the given rack."""
        return list(rack.shelves.values())

    def get_distance(self, n1: Node, n2: Node) -> float:
        """Calculates Euclidean distance between two nodes.

        Args:
            n1 (Node): First node.
            n2 (Node): Second node.

        Returns:
            float: Euclidean distance between n1 and n2.
        """
        return sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2)

    def get_actions(self, node: Node) -> Dict[str, float]:
        """Returns a dictionary of possible actions (neighboring nodes) from a given node.

        Args:
            node (Node): The node to get actions from.

        Returns:
            Dict[str, float]: Dictionary of neighboring nodes and their distances.
        """
        return {k: v for k, v in node.neighbours.items() if k != node.parent}

    def assign_heuristics(self):
        """Assigns heuristic values to nodes based on the goal location."""
        if not self.goal:
            return
        for node in self.nodes.values():
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

    def calculate_heuristics(self, goal_node: Node, agent_type: AgentType) -> Dict[str, float]:
        """Calculates heuristic values for all nodes based on the goal and agent type."""
        heuristics = {}
        
        for node_name, node in self.nodes.items():
            # Base heuristic is Manhattan distance
            distance = abs(node.x - goal_node.x) + abs(node.y - goal_node.y)
            
            # Adjust heuristic based on agent type
            if agent_type == AgentType.PICKER:
                # Pickers prefer paths with fewer obstacles
                if node.type == NodeType.CENTER:
                    distance += 2  # Penalize rack centers
                elif node.type == NodeType.ENTRY or node.type == NodeType.EXIT:
                    distance -= 1  # Favor entry/exit points
            elif agent_type == AgentType.TRANSPORTER:
                # Transporters prefer straight paths
                if node.type == NodeType.CENTER:
                    distance += 3  # Strongly penalize rack centers
                elif node.type == NodeType.ENTRY or node.type == NodeType.EXIT:
                    distance -= 2  # Strongly favor entry/exit points
            
            heuristics[node_name] = distance
            
        return heuristics

    def __repr__(self):
        """String representation of the Warehouse map."""
        return f"Warehouse(Agents: {len(self.agents)}, Tasks: {len(self.tasks)})"


from typing import List, Optional
from dataclasses import dataclass, field
import uuid

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

from typing import List, Dict, Optional, Any
from queue import Queue
import json
import os
from datetime import datetime
import uuid

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


import random
import math
import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

class Candidate:
    """Represents a candidate solution with its state, cost, and efficiency metrics"""
    def __init__(self, state, value, efficiency):
        self.state = state
        self.value = value
        self.efficiency = efficiency

class Problem:
    """Defines the warehouse optimization problem with all constraints"""
    def __init__(self, filename):
        self.filename = filename
        self.items = []
        self.box_sizes = {
            'L': {'width': 180, 'bins': 3},
            'M': {'width': 120, 'bins': 2},
            'S': {'width': 60, 'bins': 1}
        }
        self.load_items()
        
        # Warehouse configuration
        self.num_racks = 36
        self.freezer_racks = {1, 2, 3, 4, 5, 6}
        self.normal_racks = set(range(7, 37))
        self.shelf_levels = 3
        self.bins_per_shelf = 5
        self.bin_size = 60
        self.shelf_length = self.bins_per_shelf * self.bin_size
        
        self.weight_limits = {1: 400, 2: 250, 3: 150}
        self.category_conflicts = {
            'food': ['chemicals'],
            'beverages': ['chemicals'],
            'chemicals': ['food', 'beverages'],
            'frozen': [],
            'household goods': []
        }

    def load_items(self):
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                size = row['item_size'][0].upper()
                if size not in self.box_sizes:
                    raise ValueError(f"Invalid item size '{row['item_size']}'")
                
                self.items.append({
                    'id': int(row['item_id']),
                    'name': row['item_name'],
                    'size': size,
                    'category': row['category'].lower(),
                    'weight': float(row['weight']),
                    'frequency': float(row['frequency']),
                    'is_frozen': row['category'].lower() == 'frozen'
                })

    def get_bin_requirements(self, size):
        """
        Get bin requirements for an item size
        
        Args:
            size: Item size ('L', 'M', or 'S')
            
        Returns:
            tuple: (bins_needed, possible_starting_positions)
        """
        bins = self.box_sizes[size]['bins']
        possible_starts = list(range(1, self.bins_per_shelf - bins + 2))
        return bins, possible_starts

    def generate_initial_state(self):
        """Generate initial random state respecting all constraints"""
        state = {}
        shelf_usage = defaultdict(set)  # {(rack, shelf): set of occupied bins}
        
        for item in self.items:
            placed = False
            attempts = 0
            bins_needed, possible_starts = self.get_bin_requirements(item['size'])
            
            while not placed and attempts < 100:
                # Choose appropriate racks
                valid_racks = self.freezer_racks if item['is_frozen'] else self.normal_racks
                rack = random.choice(list(valid_racks))
                shelf = random.randint(1, self.shelf_levels)
                
                # Find available consecutive bins
                available_starts = [
                    s for s in possible_starts
                    if all(b not in shelf_usage[(rack, shelf)] 
                      for b in range(s, s + bins_needed))
                ]
                
                if available_starts:
                    start = random.choice(available_starts)
                    positions = list(range(start, start + bins_needed))
                    
                    # Place the item
                    state[item['id']] = (rack, shelf, positions)
                    for pos in positions:
                        shelf_usage[(rack, shelf)].add(pos)
                    placed = True
                else:
                    attempts += 1
            
            if not placed:
                # Fallback placement (may violate constraints)
                valid_racks = self.freezer_racks if item['is_frozen'] else self.normal_racks
                rack = random.choice(list(valid_racks))
                shelf = random.randint(1, self.shelf_levels)
                start = random.randint(1, self.bins_per_shelf - bins_needed + 1)
                positions = list(range(start, start + bins_needed))
                state[item['id']] = (rack, shelf, positions)
        
        return state

    def calculate_efficiency(self, state):
        """
        Calculate shelf efficiency metrics
        
        Args:
            state: Current solution state
            
        Returns:
            tuple: (perfect_shelves, good_shelves, poor_shelves, utilization)
        """
        shelf_stats = defaultdict(lambda: {'used_bins': set(), 'weight': 0, 'categories': set()})
        
        # Track shelf usage
        for item_id, (rack, shelf, positions) in state.items():
            item = next(i for i in self.items if i['id'] == item_id)
            shelf_stats[(rack, shelf)]['used_bins'].update(positions)
            shelf_stats[(rack, shelf)]['weight'] += item['weight']
            shelf_stats[(rack, shelf)]['categories'].add(item['category'])
        
        perfect = good = poor = 0
        total_used = 0
        
        # Classify each shelf
        for (rack, shelf), stats in shelf_stats.items():
            used_width = len(stats['used_bins']) * self.bin_size
            remaining = self.shelf_length - used_width
            
            if remaining == 0:
                perfect += 1
            elif remaining <= self.bin_size:  # Can fit at least one S
                good += 1
            elif remaining >= (self.shelf_length / 2):  # More than half empty
                poor += 1
            
            total_used += used_width
        
        # Calculate overall utilization
        total_space = self.num_racks * self.shelf_levels * self.shelf_length
        utilization = total_used / total_space
        
        return (perfect, good, poor, utilization)

    def evaluate(self, state):
        """
        Evaluate the cost of a solution state
        
        Args:
            state: Solution state to evaluate
            
        Returns:
            tuple: (total_cost, efficiency_metrics)
        """
        cost = 0
        shelf_stats = defaultdict(lambda: {'used_bins': set(), 'weight': 0, 'categories': set(), 'items': []})
        
        # Check hard constraints
        for item_id, (rack, shelf, positions) in state.items():
            item = next(i for i in self.items if i['id'] == item_id)
            shelf_key = (rack, shelf)
            stats = shelf_stats[shelf_key]
            
            # Track shelf usage
            stats['used_bins'].update(positions)
            stats['weight'] += item['weight']
            stats['categories'].add(item['category'])
            stats['items'].append(item)
            
            # Frozen items must be in freezer racks
            if item['is_frozen'] and rack not in self.freezer_racks:
                cost += 10000
                
            # Check weight limits
            if stats['weight'] > self.weight_limits[shelf]:
                cost += 1000
                
            # Check category conflicts
            for other in stats['items']:
                if other['category'] in self.category_conflicts[item['category']]:
                    cost += 1000
        
        # Calculate soft costs
        for item_id, (rack, shelf, positions) in state.items():
            item = next(i for i in self.items if i['id'] == item_id)
            cost += item['frequency'] * shelf  # Accessibility cost
            cost += item['weight'] * shelf     # Weight distribution cost
        
        # Add efficiency metrics
        perfect, good, poor, utilization = self.calculate_efficiency(state)
        cost -= perfect * 50  # Reward perfect shelves
        cost += poor * 100    # Penalize poor shelves
        if utilization < 0.85:
            cost += 1000 * (0.85 - utilization)  # Utilization penalty
            
        return cost, (perfect, good, poor, utilization)

    def generate_neighbor(self, current_state):
        """Generate a valid neighboring state by moving one item"""
        new_state = current_state.copy()
        item_id = random.choice(list(new_state.keys()))
        item = next(i for i in self.items if i['id'] == item_id)
        
        # Try up to 20 random moves
        for _ in range(20):
            # Choose appropriate racks
            valid_racks = self.freezer_racks if item['is_frozen'] else self.normal_racks
            rack = random.choice(list(valid_racks))
            shelf = random.randint(1, self.shelf_levels)
            
            bins_needed, possible_starts = self.get_bin_requirements(item['size'])
            
            # Get current shelf usage
            used_bins = set()
            for other_id, (r, s, positions) in new_state.items():
                if r == rack and s == shelf:
                    used_bins.update(positions)
            
            # Find available consecutive bins
            available_starts = [
                s for s in possible_starts
                if all(b not in used_bins for b in range(s, s + bins_needed))
            ]
            
            if available_starts:
                start = random.choice(available_starts)
                positions = list(range(start, start + bins_needed))
                new_state[item_id] = (rack, shelf, positions)
                return new_state
        
        return current_state  # Return original if no valid move found


def simulated_annealing(problem, initial_temp, cooling_rate, iterations):
    """
    Perform simulated annealing optimization
    
    Args:
        problem: Problem instance
        initial_temp: Starting temperature
        cooling_rate: Temperature reduction factor
        iterations: Maximum iterations
        
    Returns:
        tuple: (best_state, best_cost, best_eff, cost_history, perfect_history, util_history, movement_log)
    """
    current_state = problem.generate_initial_state()
    current_cost, current_eff = problem.evaluate(current_state)
    best_state = current_state.copy()
    best_cost = current_cost
    best_eff = current_eff
    
    # Progress tracking
    cost_history = [current_cost]
    perfect_history = [current_eff[0]]
    util_history = [current_eff[3]]
    movement_log = []
    
    for i in range(iterations):
        temp = initial_temp * (cooling_rate ** i)
        if temp < 1e-6:
            break
            
        neighbor = problem.generate_neighbor(current_state)
        neighbor_cost, neighbor_eff = problem.evaluate(neighbor)
        
        # Acceptance probability
        if neighbor_cost < current_cost or random.random() < math.exp((current_cost - neighbor_cost)/temp):
            # Log changes
            changed_items = [
                item_id for item_id in current_state
                if current_state[item_id] != neighbor.get(item_id, None)
            ]
            
            for item_id in changed_items:
                item = next(i for i in problem.items if i['id'] == item_id)
                old_pos = current_state[item_id]
                new_pos = neighbor[item_id]
                reason = determine_move_reason(problem, item, old_pos, new_pos, neighbor_cost - current_cost)
                movement_log.append(create_movement_record(item, old_pos, new_pos, reason, neighbor_cost - current_cost, i))
            
            current_state = neighbor
            current_cost = neighbor_cost
            current_eff = neighbor_eff
            
            if neighbor_cost < best_cost:
                best_state = neighbor
                best_cost = neighbor_cost
                best_eff = neighbor_eff
        
        # Record progress
        cost_history.append(current_cost)
        perfect_history.append(current_eff[0])
        util_history.append(current_eff[3])
        
        if i % 100 == 0:
            print(f"Iter {i}: Cost={current_cost}, Perfect={current_eff[0]}, Util={current_eff[3]:.1%}")
    
    # Add initial to final movement records
    initial_state = problem.generate_initial_state()
    for item in problem.items:
        item_id = item['id']
        initial_pos = initial_state[item_id]
        final_pos = best_state.get(item_id, None)
        
        if final_pos and initial_pos != final_pos:
            reason = "Initial optimization"
            cost_impact = best_cost - cost_history[0]
            movement_log.append(create_movement_record(item, initial_pos, final_pos, reason, cost_impact, "Initial"))
    
    return best_state, best_cost, best_eff, cost_history, perfect_history, util_history, movement_log


def create_movement_record(item, old_pos, new_pos, reason, cost_impact, iteration):
    """
    Create a standardized movement record dictionary
    
    Args:
        item: Item being moved
        old_pos: Original position (rack, shelf, positions)
        new_pos: New position (rack, shelf, positions)
        reason: Reason for move
        cost_impact: Cost change from this move
        iteration: Iteration number
        
    Returns:
        dict: Movement record
    """
    return {
        'item_id': item['id'],
        'item_name': item['name'],
        'category': item['category'],
        'size': item['size'],
        'old_rack': old_pos[0],
        'old_shelf': old_pos[1],
        'old_positions': format_positions(old_pos[2]),
        'new_rack': new_pos[0],
        'new_shelf': new_pos[1],
        'new_positions': format_positions(new_pos[2]),
        'reason': reason,
        'cost_impact': cost_impact,
        'iteration': iteration
    }


def format_positions(positions):
    """
    Format position list as human-readable string
    
    Args:
        positions: List of bin positions
        
    Returns:
        str: Formatted position string (e.g., "2-4" for [2,3,4])
    """
    if len(positions) == 1:
        return str(positions[0])
    return f"{positions[0]}-{positions[-1]}"


def determine_move_reason(problem, item, old_pos, new_pos, cost_change):
    """
    Determine the reason for an item movement
    
    Args:
        problem: Problem instance
        item: Item being moved
        old_pos: Original position
        new_pos: New position
        cost_change: Cost impact of move
        
    Returns:
        str: Reason description
    """
    # Frozen items
    if item['is_frozen'] and new_pos[0] in problem.freezer_racks and old_pos[0] not in problem.freezer_racks:
        return "Moved to freezer rack"
    
    # Category conflicts
    # ... [category conflict checking logic] ...
    
    # Weight distribution
    if new_pos[1] < old_pos[1]:  # Moved to lower shelf
        return "Better weight distribution"
    
    # Space utilization
    old_gaps = calculate_gaps(old_pos[2], problem.bins_per_shelf)
    new_gaps = calculate_gaps(new_pos[2], problem.bins_per_shelf)
    if min(new_gaps) > min(old_gaps):
        return "Improved space utilization"
    
    return "General optimization" if cost_change < 0 else "Exploratory move"


def calculate_gaps(positions, total_bins):
    """
    Calculate gaps between occupied bins
    
    Args:
        positions: List of occupied bin positions
        total_bins: Total bins per shelf
        
    Returns:
        list: Sizes of gaps between occupied bins
    """
    occupied = set(positions)
    gaps = []
    current_gap = 0
    
    for bin in range(1, total_bins + 1):
        if bin in occupied:
            if current_gap > 0:
                gaps.append(current_gap)
            current_gap = 0
        else:
            current_gap += 1
    
    if current_gap > 0:
        gaps.append(current_gap)
    
    return gaps if gaps else [0]



def generate_movement_report(initial_state, best_state, problem, filename='item_movements.csv'):
    """Generate CSV with exact format requested"""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'item_id', 'name', 'category', 'size',
            'initial_position', 'new_position'
        ])
        
        for item in problem.items:
            item_id = item['id']
            old_pos = initial_state.get(item_id, (None, None, []))
            new_pos = best_state.get(item_id, (None, None, []))
            
            if old_pos[0] and new_pos[0]:  # Only include properly placed items
                writer.writerow([
                    item_id,
                    item['name'],
                    item['category'],
                    item['size'],
                    f"({old_pos[0]},{old_pos[1]},{format_positions(old_pos[2])})",
                    f"({new_pos[0]},{new_pos[1]},{format_positions(new_pos[2])})"
                ])

def generate_heatmaps(initial_state, best_state, problem):
    """Generate before/after heatmaps"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Prepare data
    def prepare_heatmap_data(state):
        heatmap = np.zeros((problem.shelf_levels, problem.num_racks))
        for (rack, shelf, _) in state.values():
            heatmap[shelf-1][rack-1] += 1
        return heatmap
    
    # Initial state heatmap
    im1 = ax1.imshow(prepare_heatmap_data(initial_state), cmap='YlOrRd')
    ax1.set_title('Initial Item Distribution')
    ax1.set_xlabel('Rack Number')
    ax1.set_ylabel('Shelf Level')
    fig.colorbar(im1, ax=ax1)
    
    # Optimized state heatmap
    im2 = ax2.imshow(prepare_heatmap_data(best_state), cmap='YlOrRd')
    ax2.set_title('Optimized Item Distribution')
    ax2.set_xlabel('Rack Number')
    ax2.set_ylabel('Shelf Level')
    fig.colorbar(im2, ax=ax2)
    
    plt.savefig('placement_heatmaps.png')

def format_positioSns(positions):
    """Improved bin formatting"""
    if not positions:
        return ""
    if len(positions) == 1:
        return str(positions[0])
    return f"{positions[0]}-{positions[-1]}"
def generate_visualization(cost_history, perfect_history, util_history):
    """
    Generate optimization progress plots
    
    Args:
        cost_history: List of cost values over iterations
        perfect_history: List of perfect shelf counts
        util_history: List of utilization percentages
    """
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.plot(cost_history)
    plt.title('Cost Reduction Over Time')
    plt.xlabel('Iteration')
    plt.ylabel('Total Cost')
    
    plt.subplot(1, 3, 2)
    plt.plot(perfect_history)
    plt.title('Perfect Shelves Over Time')
    plt.xlabel('Iteration')
    plt.ylabel('Count')
    
    plt.subplot(1, 3, 3)
    plt.plot(util_history)
    plt.title('Space Utilization Over Time')
    plt.xlabel('Iteration')
    plt.ylabel('Utilization %')
    
    plt.tight_layout()
    plt.savefig('optimization_progress.png')


def generate_text_report(problem, best_state, best_cost, best_eff):
    """
    Generate detailed text report of final solution
    
    Args:
        problem: Problem instance
        best_state: Optimal solution state
        best_cost: Solution cost
        best_eff: Efficiency metrics
    """
    shelf_details = defaultdict(list)
    for item_id, (rack, shelf, positions) in best_state.items():
        item = next(i for i in problem.items if i['id'] == item_id)
        shelf_details[(rack, shelf)].append((item, positions))
    
    report = [
        "="*80,
        "WAREHOUSE OPTIMIZATION REPORT",
        "="*80,
        f"\nFinal Statistics:",
        f"- Total Cost: {best_cost}",
        f"- Perfect Shelves: {best_eff[0]} (fully packed)",
        f"- Good Shelves: {best_eff[1]} (<60cm unused)",
        f"- Poor Shelves: {best_eff[2]} (>150cm unused)",
        f"- Space Utilization: {best_eff[3]:.1%}",
        "\n" + "="*80,
        "SHELF DETAILS (POORLY UTILIZED SHELVES):",
        "="*80
    ]
    
    # Show worst shelves
    poor_shelves = sorted(
        [(k, v) for k, v in shelf_details.items()],
        key=lambda x: problem.shelf_length - sum(problem.box_sizes[i['size']]['width'] for i, _ in x[1]),
        reverse=True
    )[:10]  # Top 10 worst
    
    for (rack, shelf), items in poor_shelves:
        used = sum(problem.box_sizes[i['size']]['width'] for i, _ in items)
        report.append(
            f"\nRack {rack} Shelf {shelf} (Used: {used}cm/{problem.shelf_length}cm):"
        )
        for item, positions in items:
            report.append(
                f"  - ID {item['id']}: {item['name']} ({item['size']}, "
                f"{item['weight']}kg, {item['category']}) "
                f"in positions {format_positions(positions)}"
            )
    
    with open('optimization_report.txt', 'w') as f:
        f.write("\n".join(report))



if __name__ == "__main__":
    try:
        # Initialize problem
        problem = Problem('items.csv')
        
        # Get initial state before optimization
        initial_state = problem.generate_initial_state()
        
        # Run optimization
        print("Starting optimization...")
        results = simulated_annealing(
            problem,
            initial_temp=1000,
            cooling_rate=0.995,
            iterations=5000
        )
        best_state, best_cost, best_eff, *_ = results
        
        # Generate outputs
        generate_movement_report(initial_state, best_state, problem)
        generate_heatmaps(initial_state, best_state, problem)
        generate_visualization(*results[3:6])  # Existing progress plots
        generate_text_report(problem, best_state, best_cost, best_eff)
        
        print("\nOptimization complete!")
        print(f"- Final cost: {best_cost}")
        print(f"- Space utilization: {best_eff[3]:.1%}")
        print("- CSV output: item_movements.csv")
        print("- Heatmaps: pbackend/functions/items.csvlacement_heatmaps.png")
        print("- Progress plots: optimization_progress.png")
        print("- Report: optimization_report.txt")
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy
import json
import csv
import random
import math
import pandas as pd

# --- CONFIGURATION & CONSTANTS ---
MAX_SLOTS_PER_SHELF = 5
SHELF_LEVELS = 3
HEAVY_ITEM_THRESHOLD = 20 # For weight placement heuristic (distinct from max shelf weight)

# Heuristic Weights - TUNE THESE!
DISTANCE_BASE_FACTOR = 0.1 # Base sensitivity to distance. Lower = more sensitive.
FREQUENCY_DISTANCE_MULTIPLIER = 5.0 # How much more sensitive high-frequency items are to distance.
MAX_DISTANCE_SCORE_CONTRIBUTION = 5.0 # Cap any distance related bonus/penalty

COMPATIBILITY_MATRIX = {
    'food':           {'food': 1.0, 'beverages': 0.8, 'household goods': 0.2, 'chemicals': 0.0, 'frozen': 0.1},
    'beverages':      {'food': 0.8, 'beverages': 1.0, 'household goods': 0.3, 'chemicals': 0.0, 'frozen': 0.1},
    'household goods':{'food': 0.2, 'beverages': 0.3, 'household goods': 1.0, 'chemicals': 0.1, 'frozen': 0.05},
    'chemicals':      {'food': 0.0, 'beverages': 0.0, 'household goods': 0.1, 'chemicals': 1.0, 'frozen': 0.0},
    'frozen':         {'food': 0.1, 'beverages': 0.1, 'household goods': 0.05, 'chemicals': 0.0, 'frozen': 1.0},
}
CATEGORY_COLORS = {
    'food': 'lightgreen', 'beverages': 'lightblue', 'household goods': 'lightcoral',
    'chemicals': 'gold', 'frozen': 'lightcyan', 'default': 'lightgrey'
}

# Globals to be loaded from facts.json
ENTRANCE_COORDS = None
FROZEN_ENTRANCE_COORDS = None
MAX_WEIGHT_PER_LEVEL = None # List: [w_L0, w_L1, w_L2]
SHELFS_MAX_HEIGHT = None    # List: [h_L0, h_L1, h_L2]

# --- DATA GENERATION FUNCTIONS ---
def generate_dummy_item_csv(filename="dummy_items.csv", num_items=30):
    categories = list(COMPATIBILITY_MATRIX.keys())
    items_data = []
    for i in range(num_items):
        item_id = f"item{str(i+1).zfill(3)}" # Simpler ID generation
        category = random.choice(categories)
        name = f"{random.choice(['Premium', 'Value', 'Eco'])} {category.capitalize()} {random.choice(['Pack', 'Unit', 'Box'])}"
        weight = round(random.uniform(1, 75), 1) # Increased max weight for testing shelf limits
        slots = random.randint(1, 3)
        retrieval_counter = random.randint(0, 100)
        insertion_counter = random.randint(1, 20) # Start at 1 to avoid div by zero for new items
        items_data.append([item_id, name, weight, category, slots, retrieval_counter, insertion_counter])

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'name', 'weight', 'category', 'slots', 'retrieval_counter', 'insertion_counter'])
        writer.writerows(items_data)
    print(f"Generated {filename} with {len(items_data)} items (incl. counters).")

def generate_dummy_rack_layout_csv(filename="dummy_rack_layout.csv", rack_ids=None, item_ids_for_layout=None):
    # (Same as v4 - for brevity, not repeating the whole function. Ensure it works with the new item CSV format if needed for slot info)
    if rack_ids is None: rack_ids = [f"R{str(i+1).zfill(2)}" for i in range(8)]
    if item_ids_for_layout is None:
        try: temp_df = pd.read_csv("dummy_items.csv"); item_ids_for_layout = list(temp_df['id'])
        except: item_ids_for_layout = [f"item{str(i+1).zfill(3)}" for i in range(30)]
    layout_data = []; item_slots_map = {}
    try: df_items = pd.read_csv("dummy_items.csv"); item_slots_map = dict(zip(df_items['id'], df_items['slots']))
    except: pass
    for rack_id in rack_ids:
        for shelf_level in range(SHELF_LEVELS):
            num_items_on_shelf = random.randint(0,1) # Make layout more sparse
            current_slots, items_placed = 0,0
            shuffled_items = random.sample(item_ids_for_layout, len(item_ids_for_layout))
            for item_id in shuffled_items:
                if items_placed >= num_items_on_shelf: break
                slots_needed = item_slots_map.get(item_id, random.randint(1,2))
                if current_slots + slots_needed <= MAX_SLOTS_PER_SHELF:
                    layout_data.append([rack_id, shelf_level, item_id])
                    current_slots += slots_needed; items_placed +=1
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile); writer.writerow(['rack_id', 'shelf_level', 'item_id']); writer.writerows(layout_data)
    print(f"Generated {filename} with initial layout.")

# --- HELPER FUNCTIONS ---
def euclidean_distance(p1, p2):
    if p1 is None or p2 is None: return float('inf') # Cannot calculate distance
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# --- CLASSES ---
class Item:
    def __init__(self, item_id, name, weight, category, slots, retrieval_counter=0, insertion_counter=1):
        self.id, self.name, self.weight, self.category, self.slots_required = item_id, name, weight, category, slots
        self.retrieval_counter = int(retrieval_counter)
        self.insertion_counter = max(1, int(insertion_counter)) # Ensure at least 1
        self.is_frozen = (category == 'frozen')

    @property
    def frequency_metric(self):
        # Higher value means more frequently retrieved relative to insertions
        return self.retrieval_counter / self.insertion_counter

    def __repr__(self):
        return f"Item({self.id},'{self.name}',W:{self.weight},S:{self.slots_required},Fq:{self.frequency_metric:.2f})"

class Shelf:
    def __init__(self, level, max_slots=MAX_SLOTS_PER_SHELF):
        self.level, self.max_slots = level, max_slots
        self.items = []
        self.occupied_slots = 0
        self.current_weight = 0.0 # NEW: Track current weight on shelf

    @property
    def available_slots(self): return self.max_slots - self.occupied_slots

    def can_add_item(self, item: Item, max_weight_for_level: float): # NEW: takes max_weight
        if self.available_slots < item.slots_required:
            return False, "slot_capacity"
        if self.current_weight + item.weight > max_weight_for_level:
            return False, "weight_limit"
        # Conceptual height check (if item_height and SHELFS_MAX_HEIGHT[self.level] were used)
        # if item.height > SHELFS_MAX_HEIGHT[self.level]: return False, "height_limit"
        return True, "ok"

    def add_item(self, item: Item, max_weight_for_level: float):
        can_add_flag, reason = self.can_add_item(item, max_weight_for_level)
        if can_add_flag:
            self.items.append(item)
            self.occupied_slots += item.slots_required
            self.current_weight += item.weight # NEW: Update weight
            return True
        return False

    def __repr__(self):
        return f"Sh(L{self.level},{self.occupied_slots}/{self.max_slots}s,{self.current_weight:.1f}kg)"

class Rack: # Mostly same, passes max_weight_for_level down
    def __init__(self, rack_id, is_frozen=False, center_coords=None):
        self.id, self.is_frozen, self.center_coords = rack_id, is_frozen, tuple(center_coords) if center_coords else (0,0)
        self.shelves = [Shelf(level=i) for i in range(SHELF_LEVELS)]
    def get_shelf(self, level): return self.shelves[level] if 0 <= level < SHELF_LEVELS else None
    def __repr__(self): return f"Rk({self.id},F:{self.is_frozen},C:{self.center_coords})"


class Warehouse:
    def __init__(self, facts_file="facts.json"):
        self.racks, self._item_db_dict = {}, {}
        self.entrance_coords, self.frozen_entrance_coords = None, None
        self.max_weight_per_level, self.shelfs_max_height = None, None
        self._load_facts(facts_file)

    def _load_facts(self, facts_file):
        global ENTRANCE_COORDS, FROZEN_ENTRANCE_COORDS, MAX_WEIGHT_PER_LEVEL, SHELFS_MAX_HEIGHT
        try:
            with open(facts_file, 'r') as f: facts = json.load(f)
            self.entrance_coords = ENTRANCE_COORDS = tuple(facts["entrance_coords"])
            self.frozen_entrance_coords = FROZEN_ENTRANCE_COORDS = tuple(facts["frozen_entrance_coords"])
            self.max_weight_per_level = MAX_WEIGHT_PER_LEVEL = facts["max_weight_per_level"]
            self.shelfs_max_height = SHELFS_MAX_HEIGHT = facts["shelfs_max_height"]
            for rack_id, info in facts.get("racks_info", {}).items():
                self.racks[rack_id] = Rack(rack_id, info.get("is_frozen",False), info.get("center_coords"))
            print(f"Loaded facts: Entrances, {len(self.racks)} racks, weight/height limits.")
        except Exception as e: print(f"FATAL Error loading facts '{facts_file}': {e}. Cannot continue without facts.") ; exit()


    def load_items_from_csv(self, items_csv_file="dummy_items.csv"):
        try:
            df = pd.read_csv(items_csv_file)
            for _, row in df.iterrows():
                self._item_db_dict[row['id']] = {
                    'name':row['name'],'weight':float(row['weight']), 'category':row['category'],
                    'slots':int(row['slots']), 'retrieval_counter':int(row['retrieval_counter']),
                    'insertion_counter':int(row['insertion_counter'])
                }
            print(f"Loaded {len(self._item_db_dict)} items from {items_csv_file}.")
        except Exception as e: print(f"Error loading items CSV '{items_csv_file}': {e}")

    def _get_item_details(self, item_id_str) -> Item | None:
        details = self._item_db_dict.get(item_id_str)
        if details: return Item(item_id_str, **details) # Unpack dict to Item constructor
        return None

    def populate_layout_from_csv(self, layout_csv_file="dummy_rack_layout.csv"):
        # Ensure MAX_WEIGHT_PER_LEVEL is loaded before calling this
        if not self.max_weight_per_level:
            print("Cannot populate layout: MAX_WEIGHT_PER_LEVEL not loaded from facts.")
            return
        try:
            df = pd.read_csv(layout_csv_file); items_added = 0
            for _, row in df.iterrows():
                rack_id, shelf_level, item_id = row['rack_id'], int(row['shelf_level']), row['item_id']
                if rack_id in self.racks:
                    rack_obj = self.racks[rack_id]
                    shelf_obj = rack_obj.get_shelf(shelf_level)
                    if shelf_obj:
                        item_obj = self._get_item_details(item_id)
                        if item_obj:
                            valid_frozen = not (item_obj.is_frozen and not rack_obj.is_frozen) and \
                                           not (not item_obj.is_frozen and rack_obj.is_frozen and shelf_obj.items)
                            if valid_frozen and shelf_obj.add_item(item_obj, self.max_weight_per_level[shelf_level]):
                                items_added += 1
                            # else: print(f"Layout: Cannot add {item_id} to {rack_id}-L{shelf_level} due to constraints.") # Optional detailed log
            print(f"Populated layout from {layout_csv_file} with {items_added} items.")
        except Exception as e: print(f"Error populating layout CSV '{layout_csv_file}': {e}")


    def evaluate_placement(self, item_to_place: Item, rack: Rack, shelf: Shelf):
        score_breakdown = {
            "base": 0.0, "slot_capacity_penalty": 0.0, "shelf_weight_limit_penalty": 0.0,
            "frozen_penalty": 0.0, "compatibility": 0.0, "weight_item_placement": 0.0,
            "space_utilization": 0.0, "distance_freq_bonus": 0.0
        }
        current_score_contrib = 0

        # Hard Constraints
        can_add_flag, reason = shelf.can_add_item(item_to_place, self.max_weight_per_level[shelf.level])
        if not can_add_flag:
            if reason == "slot_capacity": score_breakdown["slot_capacity_penalty"] = -float('inf')
            elif reason == "weight_limit": score_breakdown["shelf_weight_limit_penalty"] = -float('inf')
            return -float('inf'), score_breakdown

        if item_to_place.is_frozen and not rack.is_frozen:
            score_breakdown["frozen_penalty"] = -float('inf'); return -float('inf'), score_breakdown
        if not item_to_place.is_frozen and rack.is_frozen and shelf.items:
            score_breakdown["frozen_penalty"] = -float('inf'); return -float('inf'), score_breakdown
        elif not item_to_place.is_frozen and rack.is_frozen and not shelf.items:
             score_breakdown["frozen_penalty"] = -10.0 # Heavier penalty for NF in empty F rack

        # Soft Preferences
        # 1. Category Compatibility
        cat_comp_score = sum(COMPATIBILITY_MATRIX.get(item_to_place.category,{}).get(ex.category,0.0) for ex in shelf.items)
        cat_comp_score = (cat_comp_score/len(shelf.items))*2.0 if shelf.items else 1.0 # x2 if existing, base 1 if empty
        score_breakdown["compatibility"] = cat_comp_score; current_score_contrib += cat_comp_score

        # 2. Weight Item Placement (Heavy item on lower shelf heuristic)
        weight_item_score = 0
        if item_to_place.weight > HEAVY_ITEM_THRESHOLD:
            if shelf.level == 0: weight_item_score = 1.5
            elif shelf.level == 1: weight_item_score = 0.5
            else: weight_item_score = -1.0
        else:
            if shelf.level == 2: weight_item_score = 0.2
        score_breakdown["weight_item_placement"] = weight_item_score; current_score_contrib += weight_item_score
        
        # 3. Space Utilization
        new_occ_ratio = (shelf.occupied_slots + item_to_place.slots_required) / shelf.max_slots
        space_util_score = 0.3 if new_occ_ratio > 0.75 else 0
        if new_occ_ratio == 1.0: space_util_score += 0.5 # Bonus for perfect fill
        score_breakdown["space_utilization"] = space_util_score; current_score_contrib += space_util_score
        
        # 4. Distance & Frequency Bonus
        target_entrance = self.frozen_entrance_coords if rack.is_frozen else self.entrance_coords
        dist_freq_score = 0
        if target_entrance and rack.center_coords != (0,0):
            dist = euclidean_distance(rack.center_coords, target_entrance)
            dist = max(dist, 0.1) # Min distance to avoid huge scores / div by zero
            
            # Base distance score (closer is better)
            base_dist_score = (1 / dist) * (1 / DISTANCE_BASE_FACTOR)
            
            # Frequency multiplier
            # item_freq_metric = 0 -> normal distance sensitivity
            # item_freq_metric = 1 (ret=ins) -> 1 + 1*FM = (1+FM) times base_dist_score
            # item_freq_metric = 10 (ret >> ins) -> 1 + 10*FM = (1+10*FM) times base_dist_score
            freq_multiplier = 1.0 + (item_to_place.frequency_metric * FREQUENCY_DISTANCE_MULTIPLIER)
            dist_freq_score = base_dist_score * freq_multiplier
            
            dist_freq_score = min(dist_freq_score, MAX_DISTANCE_SCORE_CONTRIBUTION) # Cap total contribution
            # Can also be negative if dist is large and base_factor makes (1/dist) small.
            # If dist_freq_score is intended as pure bonus, ensure it's positive or handle negative as penalty.
            # Current formula: closer = smaller dist = larger (1/dist) = larger bonus.
        score_breakdown["distance_freq_bonus"] = dist_freq_score; current_score_contrib += dist_freq_score
        
        final_score = score_breakdown["base"] + \
                      (score_breakdown["frozen_penalty"] if score_breakdown["frozen_penalty"] != -float('inf') else 0) + \
                      current_score_contrib
        return final_score, score_breakdown

    def find_best_spot_for_item(self, item_id_to_place_str: str): # Same detailed printing as v4
        item_to_place = self._get_item_details(item_id_to_place_str)
        if not item_to_place: print(f"Cannot analyze {item_id_to_place_str}: not in DB."); return None, -float('inf'), {}
        all_eval_spots = []
        print(f"\n--- Evaluating Placements for: {item_to_place} ---")
        print("-" * 90)
        print(f"{'Location':<12} | {'Score':>7} | {'Reason/Breakdown':<60}")
        print("-" * 90)
        for r_id, rack in self.racks.items():
            for s_lvl in range(SHELF_LEVELS):
                shelf = rack.get_shelf(s_lvl)
                score, details = self.evaluate_placement(item_to_place, rack, shelf)
                loc_str = f"{r_id}-L{s_lvl}"; all_eval_spots.append({"s":score,"p_t":(r_id,s_lvl),"p_s":loc_str,"b":details})
                bd_parts = []
                for comp, val in details.items():
                    if val == -float('inf'): bd_parts.append(f"{comp.split('_')[0].capitalize()}:FAIL")
                    elif val != 0.0: bd_parts.append(f"{comp.split('_')[0].capitalize()}:{val:.2f}")
                print(f"{loc_str:<12} | {score:7.2f} | {'; '.join(bd_parts)}")
        print("-" * 90)
        valid_spots = [s for s in all_eval_spots if s["s"] > -float('inf')]
        if not valid_spots:
            print(f"NO VALID SPOT FOUND for {item_to_place.id}. Top reasons for failure:")
            # Summarize failures
            fail_reasons = {}
            for spot_eval in all_eval_spots: # Iterate through all, even -inf
                for comp, val in spot_eval["b"].items():
                    if val == -float('inf'):
                        reason_key = comp.replace("_penalty","").replace("_", " ")
                        fail_reasons[reason_key] = fail_reasons.get(reason_key, 0) + 1
            for reason, count in sorted(fail_reasons.items(), key=lambda item: item[1], reverse=True):
                print(f"  - {reason.capitalize()} failed at {count} locations.")
            return None, -float('inf'), {}
        valid_spots.sort(key=lambda x:x["s"], reverse=True); best = valid_spots[0]
        print(f"\nSELECTED BEST: {best['p_s']} | Score: {best['s']:.2f}")
        print("  Best Spot Breakdown:")
        for comp, val in best['b'].items():
            if val != 0.0 and val != -float('inf'): print(f"    - {comp.split('_')[0].capitalize()}: {val:.2f}")
        return best['p_t'], best['s'], best['b']

    def place_item_at_spot(self, item_id_to_place_str, placement):
        if not placement or not self.max_weight_per_level: return False
        item = self._get_item_details(item_id_to_place_str);
        if not item: return False
        r_id, s_lvl = placement
        if r_id in self.racks:
            rack, shelf = self.racks[r_id], self.racks[r_id].get_shelf(s_lvl)
            if shelf and shelf.add_item(item, self.max_weight_per_level[s_lvl]): # Pass max_weight
                print(f"Successfully placed {item.id} in {r_id}-L{s_lvl}.")
                return True
        print(f"Failed to place {item_id_to_place_str} at {placement}.")
        return False

    def visualize_warehouse_state(self, title="Warehouse State", highlight_item_id=None, highlight_rack_id=None, highlight_shelf_level=None):
        num_racks = len(self.racks)
        if num_racks == 0: print("No racks to visualize."); return
        cols = 4; rows = (num_racks + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(cols * 4.5, rows * 4.5), squeeze=False) # Slightly taller for legend
        axes_flat = axes.flatten()
        rack_ids_sorted = sorted(self.racks.keys())

        for i, rack_id in enumerate(rack_ids_sorted):
            ax = axes_flat[i]; rack_obj = self.racks[rack_id]
            ax.set_xlim(-0.5, MAX_SLOTS_PER_SHELF + 0.5); ax.set_ylim(-0.5, SHELF_LEVELS -0.5 +1)
            ax.set_xticks(range(MAX_SLOTS_PER_SHELF + 1)); ax.set_yticks(range(SHELF_LEVELS))
            ax.set_yticklabels([f"L{j}\n({self.max_weight_per_level[j]}kg)" for j in range(SHELF_LEVELS)]); # Show max weight
            ax.grid(True, linestyle='--', alpha=0.7)
            title_str = f"R {rack_obj.id}{' (F)' if rack_obj.is_frozen else ''}"
            ax.set_title(title_str, fontsize=9)
            for shelf_idx, shelf_obj in enumerate(rack_obj.shelves):
                current_x_offset = 0
                for item_obj in shelf_obj.items:
                    item_w, item_h = item_obj.slots_required, 0.8
                    rect_c = CATEGORY_COLORS.get(item_obj.category, CATEGORY_COLORS['default'])
                    is_hl = (item_obj.id==highlight_item_id and rack_obj.id==highlight_rack_id and shelf_obj.level==highlight_shelf_level)
                    edge_c, line_w = ('red',2.5) if is_hl else ('black',1)
                    rect = patches.Rectangle((current_x_offset, shelf_idx+(1-item_h)/2), item_w, item_h, fc=rect_c, ec=edge_c, lw=line_w, alpha=0.8, label=f"_{item_obj.category}") # Underscore to hide individual labels
                    ax.add_patch(rect)
                    ax.text(current_x_offset+item_w/2, shelf_idx+0.5, f"{item_obj.id[:5]}\n{item_obj.weight}kg", ha='center', va='center', fontsize=5.5, color='black')
                    current_x_offset += item_w
            # Target spot visualization (same as v4)
            if highlight_item_id and highlight_rack_id == rack_obj.id and highlight_shelf_level is not None:
                shelf_to_hl = rack_obj.get_shelf(highlight_shelf_level)
                item_on_shelf = any(it.id == highlight_item_id for it in shelf_to_hl.items) if shelf_to_hl else False
                if not item_on_shelf:
                    target_item = self._get_item_details(highlight_item_id)
                    if target_item and shelf_to_hl:
                        can_place_flag, _ = shelf_to_hl.can_add_item(target_item, self.max_weight_per_level[highlight_shelf_level])
                        if can_place_flag:
                            rect_ph = patches.Rectangle((shelf_to_hl.occupied_slots, highlight_shelf_level+(1-0.8)/2),
                                                        target_item.slots_required, 0.8, fc='yellow', ec='red', lw=2, alpha=0.5, ls='--')
                            ax.add_patch(rect_ph)
                            ax.text(shelf_to_hl.occupied_slots+target_item.slots_required/2, highlight_shelf_level+0.5,
                                    f"TARGET\n{target_item.id[:5]}", ha='center', va='center', fontsize=5, color='red')
        for j in range(i + 1, len(axes_flat)): fig.delaxes(axes_flat[j])

        # Create legend handles and labels
        legend_handles = [patches.Patch(color=color, label=category) for category, color in CATEGORY_COLORS.items() if category != 'default']
        fig.legend(handles=legend_handles, loc='lower center', ncol=len(legend_handles), bbox_to_anchor=(0.5, 0.01), fontsize='small')
        
        fig.suptitle(title, fontsize=16); plt.tight_layout(rect=[0, 0.05, 1, 0.96]); # Adjust rect for legend
        plt.show()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("--- Generating Dummy Data ---")
    generate_dummy_item_csv("dummy_items.csv", num_items=50) # More items for simulation
    try:
        with open("facts.json", 'r') as f: facts_content = json.load(f)
        rack_ids_from_facts = list(facts_content.get("racks_info", {}).keys())
        item_ids_for_layout_gen = list(pd.read_csv("dummy_items.csv")['id'])
    except Exception as e:
        rack_ids_from_facts = [f"R{str(i+1).zfill(2)}" for i in range(8)]
        item_ids_for_layout_gen = [f"item{str(i+1).zfill(3)}" for i in range(50)]
    generate_dummy_rack_layout_csv("dummy_rack_layout.csv", rack_ids=rack_ids_from_facts, item_ids_for_layout=item_ids_for_layout_gen[:10]) # Sparse initial layout
    print("-" * 30)

    warehouse = Warehouse(facts_file="facts.json") # This will exit if facts.json is bad
    warehouse.load_items_from_csv("dummy_items.csv")
    warehouse.populate_layout_from_csv("dummy_rack_layout.csv")

    print("\n--- Initial Warehouse State ---")
    warehouse.visualize_warehouse_state("Initial Warehouse State")

    # Select 10 items to insert
    all_item_ids_in_db = list(warehouse._item_db_dict.keys())
    placed_item_ids = set()
    for rack in warehouse.racks.values():
        for shelf in rack.shelves:
            for item_in_shelf in shelf.items: placed_item_ids.add(item_in_shelf.id)
    
    items_to_attempt_placement = [id for id in all_item_ids_in_db if id not in placed_item_ids]
    random.shuffle(items_to_attempt_placement) # Shuffle to get variety
    items_to_insert_list = items_to_attempt_placement[:10] # Get up to 10

    if not items_to_insert_list:
        print("No new items from DB to insert. Warehouse might be full or DB matches layout.")

    for i, item_id_to_add in enumerate(items_to_insert_list):
        print(f"\n\n{'='*15} ATTEMPTING INSERTION {i+1}/{len(items_to_insert_list)} FOR ITEM: {item_id_to_add} {'='*15}")
        item_details = warehouse._get_item_details(item_id_to_add)
        if not item_details:
            print(f"Item {item_id_to_add} details not found. Skipping.")
            continue
        
        best_spot_tuple, best_score, _ = warehouse.find_best_spot_for_item(item_id_to_add)
        
        if best_spot_tuple:
            # Visualize target on a copy BEFORE actual placement
            wh_copy_viz = copy.deepcopy(warehouse)
            wh_copy_viz.visualize_warehouse_state(
                f"Target ({i+1}): {item_details.id} @ {best_spot_tuple[0]}-L{best_spot_tuple[1]}",
                highlight_item_id=item_id_to_add, highlight_rack_id=best_spot_tuple[0], highlight_shelf_level=best_spot_tuple[1]
            )
            
            print(f"\n--- Placing {item_id_to_add} at {best_spot_tuple} ---")
            if warehouse.place_item_at_spot(item_id_to_add, best_spot_tuple):
                # Visualize state AFTER actual placement on the main warehouse object
                warehouse.visualize_warehouse_state(
                    f"Placed ({i+1}): {item_details.id} @ {best_spot_tuple[0]}-L{best_spot_tuple[1]}",
                    highlight_item_id=item_id_to_add, highlight_rack_id=best_spot_tuple[0], highlight_shelf_level=best_spot_tuple[1]
                )
                # Update insertion counter for the placed item in the DB (for next potential run if item is re-evaluated)
                if item_id_to_add in warehouse._item_db_dict:
                    warehouse._item_db_dict[item_id_to_add]['insertion_counter'] +=1
            else:
                print(f"Placement failed for {item_id_to_add} despite a spot being found. This indicates an issue.")
        else:
            print(f"===> No suitable spot found for item {item_id_to_add}. Item not placed. <===")
            # Optional: visualize current state even if no placement to see why
            warehouse.visualize_warehouse_state(f"No spot for {item_id_to_add} ({i+1}) - Warehouse State")
        
    print("\n--- Final Warehouse State After All Attempts ---")
    warehouse.visualize_warehouse_state("Final Warehouse State")

import json
import heapq
import os
import matplotlib.pyplot as plt
import pandas as pd

# --- Helper Functions ---
def load_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON from {file_path}: {e}")
        return None
warehouse_map = load_json_file('map.json')
lookup_table = load_json_file('lookup_table.json')

def get_node_coordinates(node_id, graph_nodes):
    node = graph_nodes.get(node_id)
    return (node['x'], node['y']) if node else (None, None)

def heuristic_manhattan(n1, n2, nodes):
    x1, y1 = get_node_coordinates(n1, nodes)
    x2, y2 = get_node_coordinates(n2, nodes)
    return abs(x1 - x2) + abs(y1 - y2) if None not in (x1, y1, x2, y2) else float('inf')

def get_goal_node_from_lookup(item_id, table):
    return table.get(item_id, {}).get("goal_node")

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from and came_from[current]:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def greedy_search(start, goal, nodes, heuristic):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal, nodes), start))
    came_from = {start: None}
    explored = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in explored:
            continue
        explored.add(current)
        
        if current == goal:
            return reconstruct_path(came_from, current), explored

        for neighbor in nodes.get(current, {}).get("neighbours", []):  # Safely access neighbors
            if neighbor not in explored and nodes.get(neighbor, {}).get("locked", False) is False:
                came_from[neighbor] = current
                heapq.heappush(open_set, (heuristic(neighbor, goal, nodes), neighbor))

    return None, explored


def plot_statistics(path_ids, explored, warehouse_nodes, item_id):
    heuristics = [
        heuristic_manhattan(n, path_ids[-1], warehouse_nodes)
        for n in path_ids[:-1]
    ]
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))
    fig.suptitle(f"Greedy Search Haul Statistics for {item_id}")

    axs[0].bar(["Path Length", "Explored Nodes"], [len(path_ids), len(explored)], color=["blue", "orange"])
    axs[0].set_ylabel("Count")
    axs[0].set_title("Path and Explored Nodes")

    axs[1].plot(range(1, len(heuristics) + 1), heuristics, marker='o', color="green")
    axs[1].set_xlabel("Step in Path")
    axs[1].set_ylabel("Heuristic to Goal")
    axs[1].set_title("Heuristic Values Along Path")

    plt.tight_layout()
    plt.show()

# --- Main ---
PLOT = False  # Toggle this to enable/disable plots

def run():
    if not warehouse_map or not lookup_table:
        print("Map or lookup table could not be loaded.")
        return

    nodes = warehouse_map.get("nodes", {})
    agent_start_node = "N2-4"

    for entry in lookup_table:
        item_id = entry.get("item_id")
        goal_node = entry.get("goal_node")

        if not item_id or not goal_node or goal_node not in nodes:
            print(f"Invalid goal node for item {item_id}. Skipping...")
            continue

        print(f"Searching from {agent_start_node} to {goal_node} for item {item_id}")
        path, explored = greedy_search(agent_start_node, goal_node, nodes, heuristic_manhattan)

        if path:
            print(f"✅ Path found for {item_id}: {' -> '.join(path)}")
            if PLOT:
                plot_statistics(path, explored, nodes, item_id)
        else:
            print(f"❌ No path found for {item_id}.")

run()

