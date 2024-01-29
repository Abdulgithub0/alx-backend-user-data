#!/usr/bin/env python3
""" Flask app api module
"""
from flask import Flask, jsonify, request, abort, redirect
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


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout_manager():
    """DELETE /sessions
       Return:
        - Success: redirect to "/" route - 302
        - Error: 403
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
    abort(403)


@app.route("/profile", strict_slashes=False)
def profile_manager():
    """ GET /profile
        Return:
            - Success: {"email": "<user email>"}
           -  Error: 403
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def reset_password_token():
    """POST /reset_password
       Return:
        - Success: {"email": "<user email>", "reset_token": "<reset token>"}
        - Error: 403
    """
    email = request.form.get("email")
    token = None
    try:
        token = AUTH.reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
