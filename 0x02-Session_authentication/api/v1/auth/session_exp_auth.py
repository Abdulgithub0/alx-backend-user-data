#!/usr/bin/env python3
"""implement expiration date
"""
from os import environ
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """define various methods for setting expiration of session
    """

    def __init__(self) ->:
        """ constructor method
        """
        duration = environ.get("SESSION_DURATION")
        try:
            duration = int(duration)
        except exception:
            duration = 0

        self.session_duration = duration

    def create_session(self, user_id=None) -> str:
        """create wrapped around super().create_session method
        """
        session_id = super().create_session(user_id) if user_id else None
        if session_id is None:
            return None
        session_dict = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """wrapped super().user_id_for_session_id
        """
        session_dict = (self.user_id_by_session_id.get(session_id)
                        if session_id else None)
        if session_dict:
            if self.session_duration <= 0:
                return session_dict.get("user_id")
            created_at = session_dict.get("created_at")
            if created_at:
                time_left = timedelta(seconds=self.session_duration)
                if time_left + created_at > datetime.now():
                    return session_dict.get("user_id")
        return None
