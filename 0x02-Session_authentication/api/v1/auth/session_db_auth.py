#!/usr/bin/env python3
""" SessionDBAuth for storing session data in the database """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Handles session storage in the database """

    def create_session(self, user_id=None):
        """ Create and store a new UserSession, returning session_id """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Assuming `save()` writes to file
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve user_id from the session database """
        if not session_id:
            return None
        # Assuming `load()` retrieves from file
        user_session = UserSession.load(session_id=session_id)
        if not user_session:
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """ Remove UserSession from database based on session_id """
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.load(session_id=session_id)
        if not user_session:
            return False
        user_session.remove()  # Assuming `remove()` deletes from file
        return True
