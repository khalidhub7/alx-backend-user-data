#!/usr/bin/env python3
""" hashing password """
from db import DB
from user import User
from uuid import uuid4
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(
        password: str) -> bytes:
    """ hashes using bcrypt """
    return hashpw(
        password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """ generate uuids """
    return str(uuid4)


class Auth:
    """Auth class
to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str,
                      password: str) -> User:
        """ register a new user """
        try:
            user = self._db.find_user_by(email=email)
            # if not user in db the NoResultFound should be raised
            raise ValueError("User {} already exists"
                             .format(email))
        except NoResultFound:
            passwd = _hash_password(password)
            return self._db.add_user(email, passwd)

    def valid_login(self, email: str,
                    password: str) -> bool:
        """ validate login """
        try:
            user = self._db.find_user_by(
                email=email)
            if user:
                paswd = user.hashed_password
                if checkpw(password.encode('utf-8'), paswd):
                    return True
        except Exception:
            pass
        return False
