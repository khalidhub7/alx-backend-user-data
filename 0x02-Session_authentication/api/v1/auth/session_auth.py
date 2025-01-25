#!/usr/bin/env python3
""" session authentication """
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ manages user sessions """

    user_id_by_session_id = {}

    def __init__(self):
        pass

    def create_session(
            self, user_id: str = None) -> str:
        """ create and store a session ID for a user """
        if isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None
