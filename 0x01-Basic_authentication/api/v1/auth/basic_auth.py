#!/usr/bin/env python3
""" basic auth module"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ basic auth class"""

    def __init__(self):
        super().__init__()

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
returns the Base64 part of the Authorization header """
        if isinstance(authorization_header, str):
            if authorization_header.startswith('Basic '):
                return authorization_header[6:]
        return None
