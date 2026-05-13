from flask import Flask, render_template, request, make_response, jsonify
import redis
import os
import socket
import random
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Redis connection
def get_redis():
    redis_host = os.environ.get("REDIS_HOST", "redis")
    redis_port = int(os.environ.get("REDIS_PORT", 6379))
    return redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)

option_a = os.environ.get("OPTION_A", "Cats")
option_b = os.environ.get("OPTION_B", "Dogs")
hostname = socket.gethostname()

@app.route("/", methods=["GET", "POST"])
def index():
    voter_id = request.cookies.get("voter_id")
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None
    if request.method == "POST":
        vote = request.form.get("vote")
        if vote:
            try:
                r = get_redis()
                data = json.dumps({"voter_id": voter_id, "vote": vote})
                r.rpush("votes", data)
                app.logger.info(f"Vote cast: {vote} by {voter_id}")
            except Exception as e:
                app.logger.error(f"Redis error: {e}")
                return jsonify({"error": "Could not connect to Redis"}), 500

    resp = make_response(render_template(
        "index.html",
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote
    ))
    resp.set_cookie("voter_id", voter_id, max_age=31536000)
    return resp

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "vote"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
