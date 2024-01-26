#!/usr/bin/env python3

"""
Moudle: auth.py
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    Returns bytes of the hashed password
    """
    hashed_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_pass


def _generate_uuid() -> str:
    """
    Private method
    Returns a string repe of a new UUID
    """
    new_uuid = uuid.uuid4()
    return str(new_uuid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Constructor method to setup object
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with an email and passwd
        """

        # Check if user email exists
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        # Hash password
        hashed_password = _hash_password(password)

        # Create new user object
        new_user = User(email=email, hashed_password=password)

        self._db.add_user(email, password)

        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check the validity of the password
        """

        # Check if user exists
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        # If user exists check password
        hashed_pass = _hash_password(user.hashed_password)

        e_password = password.encode('utf-8')

        # Check if passwords match
        return bcrypt.checkpw(e_password, hashed_pass)
