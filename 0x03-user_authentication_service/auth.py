#!/usr/bin/env python3

"""
Moudle: auth.py
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Returns bytes of the hashed password
    """
    hashed_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_pass
