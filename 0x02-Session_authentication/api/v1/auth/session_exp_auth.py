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

    def create_session(self, user_id=None):
        """ create session with expiration tracking """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """ return 'session dict' based on a session id """

        expiration_date = created_at + timedelta(
            seconds=self.session_duration)

        try:
            session_dict = self.user_id_by_session_id.get(session_id)
            created_at = session_dict.get('created_at')
            user_id = session_dict.get('user_id')
            expiration_date = created_at + timedelta(
                seconds=self.session_duration)

            if datetime.now() > expiration_date:
                return None
            return user_id
        except Exception:
            return None
