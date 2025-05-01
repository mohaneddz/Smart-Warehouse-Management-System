from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from core.mixer import Mixer
from core.warehouse import Warehouse
from core.agent import Agent, AgentType, AgentStatus
from core.pathfinding import find_path
from core.types import NodeType
from typing import Dict, List
import traceback
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Basic configuration
class Config:
    # Use SQLite temporarily
    SQLALCHEMY_DATABASE_URI = 'sqlite:///warehouse.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False  # Preserve JSON order

app.config.from_object(Config)
db = SQLAlchemy(app)

# Create the warehouse from JSON configuration
try:
    map_path = os.path.join(os.path.dirname(__file__), 'data', 'map.json')
    warehouse = Warehouse.load_from_json(map_path)
    logger.info("Warehouse loaded successfully from map.json")
except Exception as e:
    logger.error(f"Failed to load warehouse: {str(e)}")
    raise

# Initialize the Mixer with the warehouse
mixer = Mixer(warehouse=warehouse)
logger.info("Mixer initialized successfully")

# Create some example agents
agents: Dict[int, Agent] = {}

def create_initial_agents():
    """Creates some example agents in the warehouse."""
    try:
        # Create a picker agent at A1
        start_node = warehouse.get_node_by_name("A1")
        if start_node:
            agent1 = Agent(
                agent_id=1,
                node=start_node,
                weight=1.0,
                status=AgentStatus.IDLE,
                mixer=mixer,
                agent_type=AgentType.PICKER
            )
            agents[1] = agent1
            logger.info(f"Created picker agent at A1: {agent1}")
        
        # Create a transporter agent at E5
        end_node = warehouse.get_node_by_name("E5")
        if end_node:
            agent2 = Agent(
                agent_id=2,
                node=end_node,
                weight=1.5,
                status=AgentStatus.IDLE,
                mixer=mixer,
                agent_type=AgentType.TRANSPORTER
            )
            agents[2] = agent2
            logger.info(f"Created transporter agent at E5: {agent2}")
    except Exception as e:
        logger.error(f"Failed to create agents: {str(e)}")
        raise

# Initialize agents
create_initial_agents()

@app.route('/')
def home():
    """Basic health check endpoint."""
    return jsonify({
        "message": "Warehouse Optimization API is running!",
        "agents": len(agents),
        "nodes": len(warehouse.nodes),
        "status": "healthy"
    })

@app.route('/agents', methods=['GET'])
def list_agents():
    """Lists all agents and their current positions."""
    try:
        agent_info = []
        for agent in agents.values():
            agent_info.append({
                "id": agent.agent_id,
                "type": agent.agent_type.name,
                "status": agent.status.name,
                "position": {"x": agent.node.x, "y": agent.node.y, "name": agent.node.name},
                "battery": agent.battery
            })
        return jsonify({"agents": agent_info})
    except Exception as e:
        logger.error(f"Error in list_agents: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route('/move_agent', methods=['POST'])
def move_agent():
    """Moves an agent to a target node using A* pathfinding with heuristics."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        agent_id = data.get('agent_id')
        target_node_name = data.get('target_node')
        
        if not isinstance(agent_id, int):
            return jsonify({"error": "agent_id must be an integer"}), 400
            
        if not isinstance(target_node_name, str):
            return jsonify({"error": "target_node must be a string"}), 400
            
        agent = agents.get(agent_id)
        if not agent:
            return jsonify({"error": f"Agent {agent_id} not found"}), 404
            
        target_node = warehouse.get_node_by_name(target_node_name)
        if not target_node:
            return jsonify({"error": f"Node {target_node_name} not found"}), 404
            
        # Check if target node is a rack center
        if target_node.type == NodeType.CENTER:
            return jsonify({"error": "Cannot move to a rack position"}), 400
        
        # Calculate heuristics for the agent type
        heuristics = warehouse.calculate_heuristics(target_node, agent.agent_type)
        
        # Find path using A* with heuristics
        path = find_path(agent.node, target_node, heuristics)
        
        # Move agent along path
        moves = []
        for next_node in path[1:]:  # Skip first node (current position)
            success = agent.move(next_node)
            if not success:
                return jsonify({
                    "error": "Movement failed",
                    "reason": f"Could not move to node {next_node.name}",
                    "partial_path": moves
                }), 409
            moves.append({
                "x": next_node.x,
                "y": next_node.y,
                "name": next_node.name
            })
        
        return jsonify({
            "success": True,
            "agent_id": agent_id,
            "path": moves,
            "final_position": {
                "x": agent.node.x,
                "y": agent.node.y,
                "name": agent.node.name
            }
        })
        
    except Exception as e:
        logger.error(f"Error in move_agent: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route('/warehouse/map', methods=['GET'])
def get_warehouse_map():
    """Returns the warehouse map layout."""
    try:
        nodes = []
        for node in warehouse.nodes.values():
            nodes.append({
                "name": node.name,
                "x": node.x,
                "y": node.y,
                "type": node.type.name,
                "is_locked": node.is_locked(),
                "neighbors": [{"name": n.name, "distance": d} for n, d in node.neighbours.items()]
            })
        
        racks = []
        for rack in warehouse.racks.values():
            racks.append({
                "id": rack.rack_id,
                "center": rack.center_node.name,
                "is_frozen": rack.is_frozen,
                "capacity": rack.current_capacity
            })
        
        return jsonify({
            "nodes": nodes,
            "racks": racks,
            "dimensions": {
                "width": warehouse.facts.warehouse_width,
                "length": warehouse.facts.warehouse_length,
                "height": warehouse.facts.warehouse_height
            }
        })
    except Exception as e:
        logger.error(f"Error in get_warehouse_map: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
