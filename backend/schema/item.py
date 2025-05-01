from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ItemInformation:
    """Schema for storing item information in the warehouse system.
    
    Attributes:
        item_id (str): Primary key for the item
        name (str): Name of the item
        category (str): Category of the item
        box_weight (float): Weight of the item box in kg
        box_height (float): Height of the item box in cm
        box_price (float): Price of the item
        expiry (Optional[datetime]): Expiry date of the item if applicable
        counter (int): Counter for inventory tracking
    """
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
    """Schema for mapping items to shelves in the warehouse.
    
    Attributes:
        item_id (str): Foreign key reference to ItemInformation
        shelf_id (str): Foreign key reference to Shelf
        order_in_shelf (int): Position order in the shelf
        addition_date (datetime): Date when item was added to shelf
        accessible_nodes (list[str]): List of accessible node hashes
        finale (bool): Whether this is the final position
    """
    item_id: str  # FK
    shelf_id: str  # FK
    order_in_shelf: int
    addition_date: datetime
    accessible_nodes: list[str]
    finale: bool = False 