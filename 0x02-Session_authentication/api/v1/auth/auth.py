#!/usr/bin/env python3
""" auth module """
from typing import List
from models.user import User
from os import getenv


class Auth:
    """ auth class """

    def __init__(self):
        pass

    def require_auth(self, path: str, excluded_paths:
                     List[str]) -> bool:
        """ check if path in excluded_paths
        excluded_paths: paths that not require auth """
        if len(path) != 0 and len(excluded_paths) != 0:
            for expath in excluded_paths:
                if '*' in expath:
                    p = expath.split('/')[-1].rstrip('*')  # like 'stat'
                    last_part = [i for i in path.split(
                        '/') if i][-1]  # like 'status'
                    if last_part.startswith(p):
                        return False
                else:
                    if path == expath or \
                            path + '/' == expath:
                        return False
        return True

    def authorization_header(self, request=None
                             ) -> str:
        """ authorization header """
        if request:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None
                     ) -> User:
        """ return current user """

    def session_cookie(self, request=None):
        """ return cookie value from a request """
        try:
            return request.cookies.get(
                getenv('SESSION_NAME'))
        except Exception:
            return None
