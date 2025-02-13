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

    '''def user_id_for_session_id(self, session_id=None):
        """ user_id for given session_id """
        if session_id:
            # check is the session not yet expired
            user_id = super().user_id_for_session_id(session_id)
            if user_id:
                user_session = UserSession.search(
                    {'session_id': session_id})
                if len(user_session) != 0:
                    return user_session[0].user_id
        return None'''

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user ID associated with a session ID from the database, considering expiration."""
        if session_id is None:
            return None
    # Query the database for the UserSession
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None
        user_session = user_sessions[0]
    # Check session expiration
        if self.session_duration <= 0:
            return user_session.user_id
    # Ensure created_at exists
        created_at = getattr(user_session, 'created_at', None)
        if created_at is None:
            return None
    # Calculate expiration time
        from datetime import datetime, timedelta
        expire_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expire_time:
            self.destroy_session_by_session_id(session_id)
            return None
        return user_session.user_id

    '''def destroy_session(self, request=None):
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
            return False'''

    def destroy_session_by_session_id(self, session_id):
        """Deletes the UserSession instance for the given session_id."""
        user_sessions = UserSession.search({'session_id': session_id})
        if user_sessions:
            user_session = user_sessions[0]
            user_session.remove()
            user_session.save()
            return True
        return False
