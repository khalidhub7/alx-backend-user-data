#!/usr/bin/env python3
""" basic auth module """
import base64
from models.user import User
from models.base import DATA
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ basic auth """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Base64 part from header """
        if authorization_header is None:
            return None
        if not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith(
                'Basic '):
            return None
        return authorization_header.split('Basic ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Basic - Base64 decode """
        if base64_authorization_header is None:
            return None
        if not isinstance(
                base64_authorization_header, str):
            return None
        try:
            value = base64.b64decode(
                base64_authorization_header)
        except Exception:
            return None
        return value.decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> Tuple[str]:
        """ User credentials """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(
                decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(
            decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar(User):
        """ retrieve a User instance
based on email and password """
        if user_email is None:
            return None
        if user_pwd is None:
            return None
        if not isinstance(user_email, str):
            return None
        if not isinstance(user_pwd, str):
            return None

        user_objs = User.search(
            {'email': user_email})
        if len(user_objs) == 0:
            return None
        for user_obj in user_objs:
            if user_obj.is_valid_password(user_pwd):
                return user_obj
