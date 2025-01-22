#!/usr/bin/env python3
""" auth module """
from typing import List, TypeVar
from flask import (request)
from models.user import User


class Auth:
    """ auth class """

    def __init__(self):
        """ no any obj """
        pass

    def require_auth(self, path: str, excluded_paths:
                     List[str]) -> bool:
        """ check if path in excluded_paths
        excluded_paths: paths that not require auth """
        if len(path) != 0 and len(excluded_paths) != 0:
            for expath in excluded_paths:
                p = expath.split('/')[-1].rstrip('*')  # like 'stat'
                last_part = [i for i in path.split(
                    '/') if i][-1]  # like 'status'
                if last_part.startswith(p):
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
        """ current user """

