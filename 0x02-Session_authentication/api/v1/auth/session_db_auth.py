#!/usr/bin/env python3
""" session_db_auth module
"""
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


from os import getenv


class SessionDBAuth(SessionExpAuth):
    """ session db auth class
    """
    def create_session(self, user_id=None):
        """Create session method
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User id for session id method
        """
        if session_id is None:
            return None
        if super().user_id_for_session_id(session_id) is None:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            return user_session[0].user_id
        return None

    def destroy_session(self, request=None):
        """Destroy session method
        """
        if not super().destroy_session(request):
            return False
        session_id = self.session_cookie(request)
        if session_id:
            user_session = UserSession.search({'session_id': session_id})
            if user_session is None or user_session == []:
                return False
            user_session[0].remove()
            return True
