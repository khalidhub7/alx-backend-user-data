#!/usr/bin/env python3
""" basic auth module"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple


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
