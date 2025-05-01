from typing import Dict, Optional, List, TYPE_CHECKING
from math import sqrt
from core.node import Node, NodeType
from core.task import Task
from schema.warehouse import FactsTable
from schema.storage import Rack, Shelf
from dataclasses import dataclass, field
import uuid
import json
import os
from core.types import AgentType

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
