#!/usr/bin/env python3
""" session database auth module """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ database: file """

    def create_session(self, user_id=None):
        """ create session but now stored in db not memory """
        session_id = super().create_session(user_id)
        if session_id and user_id:
            user_session = UserSession(
                user_id=user_id, session_id=session_id)
            user_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """ user_id for given session_id """
        if session_id:
            # check is the session not yet expired
            check_session = super().user_id_for_session_id(session_id)
            if check_session:
                user_session = UserSession.search(
                    {'session_id': session_id})
                if len(user_session) != 0:
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
