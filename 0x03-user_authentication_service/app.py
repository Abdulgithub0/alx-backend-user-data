#!/usr/bin/env python3
""" Flask app api module
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def get_handler():
    """GET /
       Return:
        - Json payload
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
