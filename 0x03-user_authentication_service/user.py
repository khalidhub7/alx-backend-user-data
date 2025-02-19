#!/usr/bin/env python3
""" 'User' model """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()


class User(Base):
    """ users table """
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True, autoincrement=True)  # auto
    email = Column(String(250), nullable=False)  # required
    hashed_password = Column(String(250), nullable=False)  # required
    session_id = Column(String(250), nullable=True)  # optional
    reset_token = Column(String(250), nullable=True)  # optional
