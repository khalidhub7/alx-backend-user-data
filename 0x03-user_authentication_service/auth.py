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
    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """ get session ID """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        except Exception:
            pass

    def get_user_from_session_id(
            self, session_id: str) -> User:
        """ find user by session ID """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(
                session_id=session_id)
            return user
        except Exception:
            return None
        finally:
            pass

    def destroy_session(
            self, user_id: int) -> None:
        """ destroy session """
        try:
            user = self._db.find_user_by(
                id=user_id)
            user.session_id = None
            self._db._session.commit()
            return user.session_id
        except Exception:
            return None

    def get_reset_password_token(
            self, email: str) -> str:
        """ reset password token """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(
                user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            return ValueError
