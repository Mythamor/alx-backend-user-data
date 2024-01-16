#!/usr/bin/env python3

"""
Module: basic_auth.py
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Inherits from Auth
        Methods:
                extract_base64_authorization_header
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Implements Base64 on Authorization header
        """
        if authorization_header is None or not\
                isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(' ')[1]
