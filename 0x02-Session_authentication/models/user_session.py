#!/usr/bin/env python3
"""store users' session into db
"""

from models.base import Base


class UserSession(Base):
    """ Model user sessions
    """

    def __init__(self, *args: list, **kwargs: dict):
        """construtor method
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
