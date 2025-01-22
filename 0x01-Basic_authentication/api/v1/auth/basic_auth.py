#!/usr/bin/env python3
""" basic auth module"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple
from models.user import User
from models.base import DATA


class BasicAuth(Auth):
    """ basic auth class"""

    def __init__(self):
        super().__init__()

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ extract Base64 part from 'Basic <Base64>' header
        returns:
        Base64 string (e.g., 'dXNlcjpwYXNz') or None if invalid.
        """
        if isinstance(authorization_header, str):
            if authorization_header.startswith('Basic '):
                return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ decode a Base64 string (e.g., 'dXNlcjpwYXNz') \
            into 'user:pass'.
            returns: The decoded string or None if it fails.
        """
        try:
            auth_h = base64.b64decode(
                base64_authorization_header)
            return auth_h.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """ return user credentials received from header """
        auth_h = decoded_base64_authorization_header
        if isinstance(auth_h, str):
            if ':' in auth_h:
                return tuple(auth_h.split(':'))
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> User:
        """ finds and returns the user object \
            based on the provided credentials """
        if isinstance(user_email, str) and \
                isinstance(user_pwd, str):
            if 'User' in DATA:
                users = User.search({'email': user_email})
                for user in users:
                    if user and user.is_valid_password(user_pwd):
                        return user
        return None

    def current_user(
            self, request=None) -> User:
        """ return the current user based \
            on the Authorization header """
        try:
            user_obj_from_credentials = \
                self.user_object_from_credentials(
                    *self.extract_user_credentials(
                        self.decode_base64_authorization_header(
                            self.extract_base64_authorization_header(
                                self.authorization_header(request)
                            ))))
            return user_obj_from_credentials
        except Exception:
            return None
