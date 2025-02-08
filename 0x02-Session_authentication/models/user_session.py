#!/usr/bin/env python3
""" usersessiondb module  """

from models.base import Base


class UserSession(Base):
    """ usersession class """

    def __init__(self, *args: list, **kwargs: dict):
        """ constructor """
        super().__init__(*args, **kwargs)
        self.user_id = str(kwargs.get('user_id'))
        self.session_id = str(kwargs.get('session_id'))
