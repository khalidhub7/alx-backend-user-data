#!/usr/bin/env python3
""" session authentication module """
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session Auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create session for a given user_id """
        if user_id and isinstance(user_id, str):
            from uuid import uuid4
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None
