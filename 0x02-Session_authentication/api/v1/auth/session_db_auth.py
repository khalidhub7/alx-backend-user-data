#!/usr/bin/env python3
""" session database auth module """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ database: file (.db_{class name}.json) """

    def create_session(self, user_id=None):
        """ create session but now stored in db not memory """
        if user_id:
            session_id = super().create_session(user_id)
            if session_id:
                user_session = UserSession(
                    user_id=user_id, session_id=session_id)
                user_session.save()
                print(user_session)
                return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """ user_id for given session_id """
        if session_id:
            found_sessions = UserSession.search({'session_id': session_id})
            if len(found_sessions) != 0:
                # check if session not_yet expired
                '''if super().user_id_for_session_id(session_id):'''
                check = super().user_id_for_session_id(session_id)
                if check:
                    return found_sessions[0].user_id
        return None

    def destroy_session(self, request=None):
        """ delete user session (in database) / logout """
        try:
            # it means 'not implemented'—neither true nor false
            if not super().destroy_session(request):
                return None
            session_id = self.session_cookie(request)
            user_session = UserSession.search({'session_id': session_id})
            if len(user_session) != 0:
                del user_session[0]
                return True
            raise Exception('session not found')
        except Exception:
            return False
