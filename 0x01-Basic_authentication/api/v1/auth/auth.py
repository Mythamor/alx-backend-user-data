#!/usr/bin/env python3

"""
Module: auth.py
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    Class that manages the API authentication
        Methods:
                require_auth
                authorization_header
                current_user
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if auth is required in given path
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Extraction of authoriczation header from flask request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve info about current user from flask request
        """
        return None
