#!/usr/bin/env python3
""" Flask app module
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/", strict_slashes=False)
def get_handler():
    """Handle / default get request
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
