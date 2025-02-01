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
        """
return 'user_id' based on session_id, session_dict """
        try:
            if session_id:
                session_dict = self.user_id_by_session_id.get(session_id)
                user_id = session_dict.get('user_id')
                # no expiration
                if self.session_duration <= 0:
                    return user_id
                # with expiration
                created_at = session_dict.get('created_at')
                expiration_date = created_at + timedelta(
                    seconds=self.session_duration) # enta tssali session
                if datetime.now() > expiration_date:
                    raise Exception("session expired")
                return user_id
            return None
        except Exception:
            return None
