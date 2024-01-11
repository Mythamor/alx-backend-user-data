#!/usr/bin/env python3

"""
Module: encrypt_password.py
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with bcrypt
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                    bcrypt.gensalt())

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate hashed_password matches provided password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
