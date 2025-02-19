#!/usr/bin/env python3
""" DB module """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """ DB class """

    def __init__(self) -> None:
        """ initialize a new DB instance """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        # self._engine = create_engine(
        #    "mysql://khalid77:0000@localhost/user_auth", echo=False)

        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ memoized session object """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(
            self, email: str, hashed_password: str) -> User:
        """ add_user to the users table """
        user = User(email=email,
                    hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ find appropriate row or user """
        try:
            user = self._session.query(
                User).filter_by(**kwargs).first()
        except Exception:
            raise InvalidRequestError
        if user:
            return user
        raise NoResultFound

    def update_user(self, user_id: int,
                    **kwargs) -> None:
        """ update _row_ user in db """
        user = self.find_user_by(id=user_id)
        if user:
            for k, v in kwargs.items():
                if not hasattr(user, k):
                    raise ValueError
                setattr(user, k, v)
            self._session.commit()
