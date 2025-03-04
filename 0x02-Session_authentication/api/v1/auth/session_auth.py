#!/usr/bin/env python3
""" session authentication module """
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session Auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create session for a given user_id """
        if user_id and isinstance(user_id, str):
            from uuid import uuid4
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(
            self, session_id: str = None) -> str:
        """ return a user_id for given session_id """
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        """ return user obj based on session_id """
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                # here it use appropriate (user_id_for_session_id) func
                # (user_id_for_session_id) that control expiration
                # so (session_auth) or (session_exp_auth)'s
                # (user_id_for_session_id)
                user_id = self.user_id_for_session_id(session_id)
                if user_id:
                    from models.user import User
                    user = User.get(user_id)
                    if user:
                        return user
        return None

    def destroy_session(self, request=None):
        """ deletes the user session / logout """
        if request:
            session_id = self.session_cookie(request)
            if session_id and session_id \
                    in self.user_id_by_session_id:
                del self.user_id_by_session_id[session_id]
                return True
        return False
