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


def _generate_uuid() -> str:
    """ generate uuid """
    from uuid import uuid4
    return str(uuid4())


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
            stored_pswd = user.hashed_password.encode() if isinstance(
                user.hashed_password, str) else user.hashed_password

            return checkpw(password.encode(), stored_pswd)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ create session """
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(
                user.id, session_id=sess_id)
            return sess_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ return user by session_id """
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
