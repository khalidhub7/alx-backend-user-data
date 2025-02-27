#!/usr/bin/env python3
""" auth module """
from db import DB
from user import User
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ hash password """
    return hashpw(password.encode('utf-8'),
                  salt=gensalt())


class Auth:
    """ Auth class to interact \
with the authentication database. """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str
                      ) -> User:
        """ register_user method """
        if email and password:
            try:
                user = self._db.find_user_by(email=email)
                raise ValueError(f"User <{email}> already exists")
            except NoResultFound:
                return self._db.add_user(
                    email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """ credentials validation method """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode(),
                           user.hashed_password.encode())
        except Exception:
            return False
