#!/usr/bin/env python3
""" session authentication Module """
import os
from models.user import User
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Manages session ID """
    user_id_by_session_id = {}

    def create_session(
            self, user_id: str = None
    ) -> str:
        """ Generates a new session ID """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[
            session_id] = user_id
        return session_id

    def user_id_for_session_id(
            self, session_id: str = None) -> str:
        """
returns a User ID based on a Session ID """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        value = SessionAuth.user_id_by_session_id.get(
            session_id)
        return value

    def current_user(self, request=None):
        """ returns a User instance
based on a cookie value """
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)
