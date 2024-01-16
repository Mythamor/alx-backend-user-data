#!/usr/bin/env python3

"""
Module: basic_auth.py
"""

from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes auth_header ad returns Base64 String
        """
        if base64_authorization_header is None or not\
                isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_auth = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_auth.decode('utf-8')
            return decoded_str
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None or not\
                isinstance(decoded_base64_authorization_header, str) or\
                ':' not in decoded_base64_authorization_header:
            return None, None

        user, password = decoded_base64_authorization_header.split(':')
        return user, password
