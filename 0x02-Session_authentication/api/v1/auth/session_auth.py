#!/usr/bin/env python3

"""
Module: session_auth.py
    Provides a class for session-based authentication,
    extending the base Auth class.

    Classes:
        SessionAuth: Handles session-based authentication.
"""


from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """
    Class for Session-based authentication.

    Inherits from the base Auth class and provides methods
    for session-based authentication.

    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
