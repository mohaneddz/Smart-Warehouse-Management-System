from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class FactsTable:
    """Schema for warehouse configuration and constraints.
    
    Attributes:
        name (str): Name of the warehouse
        location (str): Location of the warehouse
        warehouse_width (float): Width of the warehouse in meters
        warehouse_length (float): Length of the warehouse in meters
        warehouse_height (float): Height of the warehouse in meters
        n_racks (int): Number of racks
        n_shelfs_per_rack (int): Number of shelves per rack
        shelfs_max_height (List[float]): Maximum heights for each shelf level [z1,z2..]
        shelf_max_width (float): Maximum width of a shelf
        item_length (float): Standard item length
    """
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
    """Schema for warehouse transactions.
    
    Attributes:
        transaction_id (str): Primary key for the transaction
        transaction_type (str): Type of transaction (e.g., 'pickup', 'dropoff')
        item_id (str): Foreign key reference to ItemInformation
        quantity (int): Quantity of items involved
        date (datetime): Date and time of the transaction
    """
    transaction_id: str  # PK
    transaction_type: str
    item_id: str  # FK -> ItemInformation
    quantity: int
    date: datetime 