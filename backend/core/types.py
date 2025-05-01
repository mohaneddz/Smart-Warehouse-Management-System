from enum import Enum, auto
from typing import Protocol, List, Optional, Dict, Tuple, Any
from datetime import datetime
from dataclasses import dataclass
from backend.core import Node
from backend.core import Task
from backend.core import Warehouse

# Enums
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

# Protocols
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

class IAgent(Protocol):
    """Interface for agent objects."""
    agent_id: int
    node: 'Node'
    weight: float
    status: AgentStatus
    goal_state: str
    mixer: Optional['IMixer']
    path: List['Node']
    battery: float
    agent_type: AgentType
    hash_id: str

class IMixer(Protocol):
    """Interface for mixer objects."""
    warehouse: 'Warehouse'
    tasks: List['Task']
    priority_tasks: List['Task']
    agents: Dict[str, IAgent]
    logs: List[str]
    log_file: str

    def log_event(self, event_type: str, message: str, agent: Optional[IAgent] = None, task: Optional['Task'] = None) -> None:
        """Logs an event in the system."""
        pass

class ITask(Protocol):
    """Protocol defining the interface for a Task."""
    hash_id: str
    initial_state: str
    goal_state: str
    job: TaskType
    priority: int

# Schema Classes
@dataclass
class ItemInformation:
    """Schema for storing item information in the warehouse system."""
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
    """Schema for mapping items to shelves in the warehouse."""
    item_id: str  # FK
    shelf_id: str  # FK
    order_in_shelf: int
    addition_date: datetime
    accessible_nodes: List[str]
    finale: bool = False

@dataclass
class Rack:
    """Schema for storage racks in the warehouse."""
    rack_id: str  # PK
    is_frozen: bool
    current_capacity: float
    start_coords: Tuple[float, float]  # [x,y]
    center_coords: Tuple[float, float]  # [x,y]
    end_coords: Tuple[float, float]    # [x,y]

@dataclass
class Shelf:
    """Schema for shelves within racks."""
    shelf_id: str  # PK
    rack_id: str   # FK -> Rack
    z_level: float
    current_weight: float
    is_locked: bool = False

@dataclass
class FactsTable:
    """Schema for warehouse configuration and constraints."""
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

@dataclass
class Transaction:
    """Schema for warehouse transactions."""
    transaction_id: str  # PK
    transaction_type: str
    item_id: str  # FK -> ItemInformation
    quantity: int
    date: datetime 