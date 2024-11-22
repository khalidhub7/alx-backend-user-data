#!/usr/bin/env python3
""" hashing password """
from bcrypt import hashpw, gensalt


def _hash_password(
        password: str) -> bytes:
    """ hashes using bcrypt """
    return hashpw(
        password.encode('utf-8'), gensalt())
