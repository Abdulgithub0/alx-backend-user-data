#!/usr/bin/env python3
"""Implement Authorization for the api server
"""
from flask import request
from typing import TypeVar, List
from models.user import User


class Auth:
    """Template for all authentication system used in api server
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Define which routes don't need authentication"""
        if path and excluded_paths:
            for i in excluded_paths:
                if i.endswith('*') and path.startswith(i[:-1]):
                    return False
                elif i in {path, path + '/'}:
                    return False
        return True

    def authorization_header(self, request: TypeVar('request') = None) -> str:
        """validate all requests to secure the API"""
        auth_value = request.headers.get("Authorization") if request else None
        return auth_value

    def current_user(self, request=None) -> TypeVar('User'):
        """later also"""
        return None
