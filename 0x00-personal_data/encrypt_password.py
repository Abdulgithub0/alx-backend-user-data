#!/usr/bin/env python3
"""Encrypt user passwords
"""
import bcrypt as b


def hash_password(password: str) -> bytes:
    """return a salted byte encrypted version of password
    """
    return b.hashpw(password.encode("utf-8"), b.gensalt())


def is_valid(hashed_password: bytes, password: str) - bool:
    """validate that the provided password matches the hashed password
    """
    return b.checkpw(password.encode("utf-8"), hashed_password)
