#!/usr/bin/env python3

"""
Module: auth.py
"""

from flask import request
from typing import List, TypeVar
import fnmatch


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
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        """
        # Ensure slash tolerance
        path_with_slash = path if path.endswith('/') else path + '/'
        epath_with_slash = [p if p.endswith('/') else p + '/' or p + '*'
                            for p in excluded_paths]

        return path_with_slash not in epath_with_slash
        """

        for ex_path in excluded_paths:
            if ex_path.startswith(path):
                return False
            elif path.startswith(ex_path):
                return False
            elif ex_path[-1] == "*":
                if path.startswith(ex_path[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Extraction of authoriczation header from flask request
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve info about current user from flask request
        """
        return None
