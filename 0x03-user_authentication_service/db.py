#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from user import Base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine(
            "sqlite:///a.db", echo=False)
        """ self._engine = create_engine(
            "mysql+pymysql://root:0000\
@localhost/user_auth_test", echo=True) """
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(
                bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(
            self, email: str, hashed_password: str) -> User:
        """ add a new user to the database """
        new_user = User(
            email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """ find a user by given attributes """
        columns = User.__table__.columns.keys()
        for attr, val in kwargs.items():
            if attr in columns:
                result = self._session.query(User).filter(
                    getattr(User, attr) == val).first()
                if result:
                    return result
                raise NoResultFound
            raise InvalidRequestError
