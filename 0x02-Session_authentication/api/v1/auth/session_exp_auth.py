#!/usr/bin/env python3
""" session expiration module """
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ session expiration class """

    def __init__(self, *args, **kwargs):
        """ overload __init__ """
        try:
            from os import getenv
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ overload create_session """
        session_id = super().create_session(user_id)
        if session_id:
            from datetime import datetime
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id, 'created_at': datetime.now()
            }
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """ overload user_id_for_session_id """
        if session_id and session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id.get(session_id)
            user_id = session_dict.get('user_id')
            if session_dict and user_id:
                if self.session_duration <= 0:
                    return user_id
                created_at = session_dict.get('created_at')
                if created_at:
                    from datetime import timedelta, datetime
                    expiration_date = created_at + timedelta(
                        seconds=self.session_duration)
                    if expiration_date > datetime.now():
                        return user_id
        return None
