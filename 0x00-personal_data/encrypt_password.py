#!/usr/bin/env python3
"""Encrypt user passwords
"""

import bcrypt as b


def hash_password(psword: str) -> bytes:
    """return salted byte encrypted version of pword"""
    return b.hashpw(psword.encode("utf-8"), b.gensalt())
