#!/usr/bin/env python3
""" manages session expiration """
from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session authentication with expiration """

    def __init__(self):
        """ initialize sess duration """
        super()
        self.session_duration = int(getenv('SESSION_DURATION', '0'))

    def create_session(self, user_id: str = None) -> str:
        """Create session method
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ return 'session dict' based on a session id """
        session_dict = self.user_id_by_session_id.get(session_id)
        created_at = session_dict.get('created_at')
        user_id = session_dict.get('user_id')

        if session_dict and created_at and user_id:
            if self.session_duration <= 0:
                return user_id
            expiration_date = created_at + timedelta(
                seconds=self.session_duration)

            if datetime.now() > expiration_date:
                return None
            return user_id
        return None
