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
        if path is None or excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        if (path + '/') in excluded_paths:
            return False
        if path in excluded_paths:
            return False
        if (path + '/') not in excluded_paths:
            return True
        if path not in excluded_paths:
            return True

    def authorization_header(
            self, request=None) -> str:
        """Retrieve the value of the
Authorization header from a request"""
        if request is None:
            return None
        if not request.headers.get(
                'Authorization'):
            return None
        return request.headers.get(
            'Authorization')

    def current_user(self, request=None
                     ) -> TypeVar('User'):
        """Retrieve the current user
based on the request"""
        return None
