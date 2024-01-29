#!/usr/bin/env python3
""" Flask app api module
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def default_get_handler():
    """GET /
       Return:
        - Json payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def new_user_register():
    """POST /users
       Return:
        - Success: {"email": "<registered email>", "message": "user created"}
        - Error: 400
    """
    email = request.form.get("email")
    passwd = request.form.get("password")
    try:
        user = AUTH.register_user(email, passwd)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login_manager():
    """POST /sessions
       Return:
        - Success: {"email": "<user email>", "message": "logged in"}
        - Error: 401
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
