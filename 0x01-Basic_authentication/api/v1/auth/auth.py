#!/usr/bin/env python3
"""Implement Basic access Authorization for the server app
"""
from flask import request
from typing import TypeVar, List
from models.user import User


class Auth:
    """Template for all authentication system used in flask app instance.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """will """
        return False

    def authorization_header(self, request: TypeVar('request') = None) -> str:
        """ later """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """later also"""
        return None
