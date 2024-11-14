#!/usr/bin/env python3
""" UserSession model """
from models.base import Base


class UserSession(Base):
    """ Model to represent a user session stored in the database """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize UserSession instance """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', "")
        self.session_id = kwargs.get('session_id', "")
