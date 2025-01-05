#!/usr/bin/env python3
""" encrypting passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """ encrypting pass """
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check valid pass """
    return bcrypt.checkpw(password.encode('utf-8'),
                          hashed_password)
