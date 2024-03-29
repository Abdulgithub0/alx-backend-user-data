#!/usr/bin/env python3
"""Implement Authorization for the api server
"""
from flask import request
from typing import TypeVar, List
from models.user import User
from os import environ


class Auth:
    """Template for all authentication system used in api server
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Define which routes don't need authentication"""
        real = True
        if path and excluded_paths:
            if path[-1] != "/":
                path = path + "/"
            real = path not in excluded_paths
        return real

    def authorization_header(self, request: TypeVar('request') = None) -> str:
        """validate all requests to secure the API"""
        auth_value = request.headers.get("Authorization") if request else None
        return auth_value

    def current_user(self, request=None) -> TypeVar('User'):
        """later also"""
        return None

    def session_cookie(self, request=None):
        """retrieve a cookie value from a request then return
        """
        if request:
            my_session = environ.get("SESSION_NAME")
            return request.cookies.get(my_session)
        return None
