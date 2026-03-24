from flask import Flask, jsonify, request
import logging
import os
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

# Get environment
APP_ENV = os.getenv("APP_ENV", "dev")

# Sample data
USERS = [
    {"id": 1, "name": "Praveen"},
    {"id": 2, "name": "DevOps"}
]

# Middleware-like logging
@app.before_request
def log_request_info():
    logger.info(f"{request.remote_addr} - {request.method} {request.path}")

@app.route("/")
def welcome_message():
    response = jsonify({
        "message": "Welcome to the Flask API!",
        "env": APP_ENV,
        "timestamp": datetime.utcnow().isoformat()
    })
    # Health check endpoint
    return response

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "OK",
        "env": APP_ENV,
        "timestamp": datetime.utcnow().isoformat()
    }), 200

# Users endpoint
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(USERS), 200

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)