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
        return False

    def authorization_header(self, request=None
                             ) -> str:
        """ authorization header """
        return None

    def current_user(self, request=None
                     ) -> User:
        """ current user """
