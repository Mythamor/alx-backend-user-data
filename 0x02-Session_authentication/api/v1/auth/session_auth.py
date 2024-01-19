#!/usr/bin/env python3

"""
Module: session_auth.py
    Authenticates the session.

    Provides a class for session-based authentication,
     extending the base Auth class.

    Classes:
    - SessionAuth: Handles session-based authentication.

    Methods:
    - __init__(self): Initializes a new instance of SessionAuth.
    - current_user(self, request=None): Retrieves the current user
      based on the session.
    - create_session(self, user_id=None): Creates a new session
      for the given user ID.
    - destroy_session(self, request=None): Destroys the current session.
"""

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Class for Session-based authentication.

    Inherits from the base Auth class and provides methods
    for session-based authentication.

    Methods:
    - __init__(self): Initializes a new instance of SessionAuth.
    - current_user(self, request=None):
      Retrieves the current user based on the session.
    - create_session(self, user_id=None):
      Creates a new session for the given user ID.
    - destroy_session(self, request=None):
      Destroys the current session.
    """
    pass
