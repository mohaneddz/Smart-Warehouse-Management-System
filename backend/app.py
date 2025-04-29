from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from routes.optimize import optimize_route
from utils.config import DevelopmentConfig

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize the SQLAlchemy database connection
db = SQLAlchemy(app)

# Root route (basic health check)
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
    
    # Call the optimization function (you can modify this to interact with the DB if needed)
    result = optimize_route(data)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
