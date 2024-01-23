#!/usr/bin/env python3
""" handles all routes for the Session authentication.
"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import environ


@app_views.route("/auth_session/login",
                 methods=["POST"], strict_slashes=False)
def login_users():
    """POST /api/v1/auth_session/login
        JSON body:
            - email
            - password
        Return:
            - JSON representation of the login User
    """
    user_email = request.form.get("email")
    user_password = request.form.get("password")
    match_users = None
    user_found = None
    resp = None
    if user_email is None:
        return jsonify({"error": "email missing"}), 400
    if user_password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        match_users = User.search({"email": user_email})
    except Exception:
        pass  # logger here
    if match_users and len(match_users) > 0:
        for user in match_users:
            if user.is_valid_password(user_password):
                user_found = user
                break
        if user_found:
            from api.v1.app import auth
            cookie_name = environ.get("SESSION_NAME")
            _id = auth.create_session(user_found.id)
            resp = jsonify(user_found.to_json())
            resp.set_cookie(cookie_name, _id)
        else:
            return jsonify({"error": "wrong password"}), 401
    else:
        return jsonify({"error": "no user found for this email"}), 404
    return resp


@app_views.route("/auth_session/logout",
                 methods=["DELETE"], strict_slashes=False)
def logout_users():
    """DELETE /api/v1/auth_session/logout
        JSON body:
            - session_id
        Return:
            - Empty JSON
    """
    from api.v1.app import auth

    has_session = auth.destroy_session(request)
    if not has_session:
        abort(404)
    return jsonify({})
