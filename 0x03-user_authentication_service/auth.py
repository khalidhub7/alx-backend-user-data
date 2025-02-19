#!/usr/bin/env python3
""" auth module """
from bcrypt import hashpw, gensalt


def _hash_password(password):
    """ hash password """
    return hashpw(password.encode('utf-8'),
                  salt=gensalt())
