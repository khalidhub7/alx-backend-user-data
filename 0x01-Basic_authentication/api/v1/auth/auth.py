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
        """ require auth """
        if path and excluded_paths:
            if len(path) != 0 and len(excluded_paths) != 0:
                if path in excluded_paths \
                        or path + '/' in excluded_paths:
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
