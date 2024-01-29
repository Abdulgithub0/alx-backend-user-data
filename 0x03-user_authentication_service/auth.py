#!/usr/bin/env python3
"""auth module
"""
import bcrypt as b
from sqlalchemy.orm.exc import NoResultFound
from db import DB, User, InvalidRequestError
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """salt and hash a password
    """
    return b.hashpw(password.encode("utf-8"), b.gensalt())


def _generate_uuid() -> str:
    """generate uuid4
    """
    return str(uuid4())


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
        except (InvalidRequestError, NoResultFound):
            pass
        return False

    def create_session(self, email: str) -> str:
        """Generate a session_id for a user if found on DB
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                new_session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=new_session_id)
                return new_session_id
        except (ValueError, InvalidRequestError, NoResultFound):
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Retrieve a user from DB based on assigned session_id
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except (NoResultFound, InvalidRequestError):
                pass
        return None

    def destroy_session(self, user_id: int) -> None:
        """Terminate/remove a user session from DB
        """
        if user_id:
            try:
                user = self._db.find_user_by(user_id=user_id)
                if user.session_id:
                    self._db.update_user(user_id, user.session_id=None)
            except Exception:
                pass
        return None
