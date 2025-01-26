#!/usr/bin/env python3
""" session authentication """
from uuid import uuid4
from models.user import User
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ manages user sessions """

    user_id_by_session_id = {}

    def __init__(self):
        pass

    def create_session(
            self, user_id: str = None) -> str:
        """ store user_id with session_id \
            in user_id_by_session_id """
        if isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(
            self, session_id: str = None) -> str:
        """ return User id based on a session id """
        if isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        """ returns user based on a cookie value """
        try:
            session_id = self.session_cookie(request)
            user_id = self.user_id_for_session_id(session_id)
            return User.get(user_id)
        except Exception:
            return None
