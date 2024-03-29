#!/usr/bin/env python3

"""
Module: basic_auth.py
"""

from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


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

        credentials = decoded_base64_authorization_header

        # Split credentials on first colon only
        col_index = credentials.find(':')
        if col_index == -1:
            return None

        user = credentials[:col_index]
        password = credentials[col_index + 1:]

        return user, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]
        if user.is_valid_password(user_pwd):
            return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)

        if not base64_header:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if not decoded_header:
            return None

        credentials = self.extract_user_credentials(decoded_header)
        if not credentials:
            return None

        user_email, user_pwd = credentials
        return self.user_object_from_credentials(user_email, user_pwd)
