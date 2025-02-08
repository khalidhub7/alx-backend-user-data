#!/usr/bin/env python3
""" session database auth module """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ database: file """

    def create_session(self, user_id=None):
        """ create session but now stored in db not memory """
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id, session_id)
            user_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """ user_id for given session_id """
        if session_id:
            user_session = UserSession.search({'session_id': session_id})
            if len(user_session) != 0:
                return user_session[0].user_id
        return None

    def destroy_session(self, request=None):
        """ delete user session (in database) / logout """
        try:
            session_id = self.session_cookie(request)
            user_session = UserSession.search({'session_id': session_id})
            if len(user_session) != 0:
                del user_session[0]
                return True
            return False
        except Exception:
            return False
