#!/usr/bin/env python3
""" session authentication Module """
import os
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