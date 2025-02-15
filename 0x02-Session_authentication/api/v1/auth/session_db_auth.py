#!/usr/bin/env python3
""" store Session IDs in db (file) """
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """

    def create_session(self, user_id=None):
        """ overload, to store instance of UserSession """
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(
                user_id=user_id, session_id=session_id)
            user_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """ overload user_id_for_session_id """
        if session_id:
            UserSession.load_from_file()

            sessions = UserSession.search(
                {'session_id': session_id})
            if len(sessions) != 0:
                from datetime import timedelta, datetime
                created_at = sessions[0].created_at
                expiration_date = created_at + timedelta(
                    seconds=self.session_duration)
                if self.session_duration <= 0:
                    return sessions[0].user_id
                if expiration_date > datetime.now():
                    return sessions[0].user_id
        return None

    def destroy_session(self, request=None):
        """ overload to destroy the UserSession """
        session_id = self.session_cookie(request)
        if session_id:
            UserSession.load_from_file()
            sessions = UserSession.search(
                {'session_id': session_id})
            if len(sessions) != 0:
                user_session = sessions[0]
                user_session.remove()
                return True
        return False
