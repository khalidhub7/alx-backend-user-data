#!/usr/bin/env python3
""" handling authentication """
from os import getenv
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

        for i in excluded_paths:
            # if *
            if '*' in i:
                # it give something like ['api', 'v1', 'status']
                p = list(filter(None, path.split('/')))
                for ex_p in excluded_paths:
                    find = list(filter(None, ex_p.split('/')))
                    if p[:-1] == find[:-1]:
                        find = find[-1].split('*')[0]
                        if p[-1].startswith(find):
                            return False
                return True
        # if not *
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

    def session_cookie(self, request=None):
        """ Retrieve the session cookie
value from the request """
        if request is None:
            return None
        name = getenv('SESSION_NAME')
        cookie = request.cookies.get(name)
        return cookie
