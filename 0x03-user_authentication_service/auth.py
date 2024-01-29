#!/usr/bin/env python3
"""auth module
"""
import bcrypt as b
from sqlalchemy.orm.exc import NoResultFound
from db import DB, User


def _hash_password(password: str) -> bytes:
    """salt and hash a password
    """
    return b.hashpw(password.encode("utf-8"), b.gensalt())


class Auth:
    """Auth class implement authentical interfaces to DB class.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """regsiter new user to DB
        """
        try:
            new_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Verify if a User given User and password exist on the DB
        """
        try:
            fs = self._db.find_user_by(email=email)
            if fs:
                return b.checkpw(password.encode("utf-8"), fs.hashed_password)
        except (ValueError, NoResultFound):
            pass
        return False
