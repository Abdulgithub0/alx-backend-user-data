#!/usr/bin/env python3
"""Implementation of Session for Stateful authencation
"""

from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """define session protocols needed for the app services
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """handle the creation of unique session per user id
        """
        if user_id and type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retrive user_id from store session_id
        """
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None
