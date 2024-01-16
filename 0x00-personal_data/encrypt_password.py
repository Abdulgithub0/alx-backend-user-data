#!/usr/bin/env python3
"""Encrypt user passwords
"""
import bcrypt as b


def hash_password(password: str) -> bytes:
    """return a salted byte encrypted version of password
    """
    return b.hashpw(password.encode("utf-8"), b.gensalt())
