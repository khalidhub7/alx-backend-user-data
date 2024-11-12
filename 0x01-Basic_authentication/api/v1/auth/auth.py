#!/usr/bin/env python3
""" handling authentication """
from flask import request
from typing import List, TypeVar


class Auth:
    """
authentication for accessing resources """

    def require_auth(
            self, path: str, excluded_paths: List[str]
    ) -> bool:
        """ Determine if a given path
requires authentication """
        return False

    def authorization_header(
            self, request=None) -> str:
        """Retrieve the value of the
Authorization header from a request"""
        return request

    def current_user(self, request=None
                     ) -> TypeVar('User'):
        """Retrieve the current user
based on the request"""
        return request
