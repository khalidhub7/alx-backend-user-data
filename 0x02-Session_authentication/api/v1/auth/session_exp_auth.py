#!/usr/bin/env python3
""" session auth class
with expiration handling """
import datetime
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Manages session expiration """

    def __init__(self):
        """ initializes SessionExpAuth """
        self.session_duration = int(
            getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """ Creates a session
and adds creation time for expiration tracking """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.datetime.now()
        }
        return session_id

    def user_id_for_session_id(
            self, session_id=None):
        """ Retrieves user ID if session is valid,
accounting for expiration """
        if session_id is None:
            return None
        user_id = self.user_id_by_session_id.get(
            session_id)
        if user_id is None:
            return None
        if self.session_duration <= 0:
            return user_id.get('user_id')
        if self.user_id_by_session_id.get(
                session_id).get('created_at') is None:
            return None

        session_expiry = self.user_id_by_session_id.get(
            session_id).get('created_at') + datetime.timedelta(
                seconds=self.session_duration)
        if session_expiry < datetime.datetime.now():
            return None
        return self.user_id_by_session_id.get(
            session_id).get('user_id')
