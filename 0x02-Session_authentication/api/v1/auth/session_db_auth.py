#!/usr/bin/env python3
"""create a db to store user sessions
"""

from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """create a db engine for user sessions
    """

    def create_session(self, user_id=None) -> str:
        """create and return user session upon login
        """
        return super().create_session(user_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ return user id based on session_id
        """
        return super().user_id_for_session_id(session_id)

    def destroy_session(self, request=None):
        """remove user session from db upon logout
        """
        return super().destroy_session(request)
