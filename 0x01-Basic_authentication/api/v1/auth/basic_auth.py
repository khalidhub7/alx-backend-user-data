#!/usr/bin/env python3
""" basic auth module """
import base64
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
