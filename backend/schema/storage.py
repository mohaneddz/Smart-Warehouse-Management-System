from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Rack:
    """Schema for storage racks in the warehouse.
    
    Attributes:
        rack_id (str): Primary key for the rack
        is_frozen (bool): Whether the rack is for frozen goods
        current_capacity (float): Current capacity utilization
        start_coords (Tuple[float, float]): Starting coordinates [x,y]
        center_coords (Tuple[float, float]): Center coordinates [x,y]
        end_coords (Tuple[float, float]): End coordinates [x,y]
    """
    rack_id: str  # PK
    is_frozen: bool
    current_capacity: float
    start_coords: Tuple[float, float]  # [x,y]
    center_coords: Tuple[float, float]  # [x,y]
    end_coords: Tuple[float, float]    # [x,y]

@dataclass
class Shelf:
    """Schema for shelves within racks.
    
    Attributes:
        shelf_id (str): Primary key for the shelf
        rack_id (str): Foreign key reference to Rack
        z_level (float): Vertical level in the rack
        current_weight (float): Current weight on the shelf
        is_locked (bool): Whether the shelf is locked for operations
    """
    shelf_id: str  # PK
    rack_id: str   # FK -> Rack
    z_level: float
    current_weight: float
    is_locked: bool = False 