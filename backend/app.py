from flask import Flask, jsonify, request
from routes.optimize import optimize_route
from core.agent_system import Mixer
from core.warehouse import Warehouse

warehouse = Warehouse()
mixer = Mixer(warehouse, [])



app = Flask(__name__)

# Root route (just a basic health check)
@app.route('/')
def home():
    return jsonify({"message": "Warehouse Optimization API is running!"})

# Route to optimize warehouse layout or task allocation
@app.route('/optimize', methods=['POST'])
def optimize():
    # Get input data (e.g., warehouse layout, tasks, agent data)
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided!"}), 400
    
    # Call optimize function (to be implemented in optimize.py)
    result = optimize_route(data)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
