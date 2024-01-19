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
    user_id_by_session_id
    pass
