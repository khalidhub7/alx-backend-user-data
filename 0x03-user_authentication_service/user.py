#!/usr/bin/env python3
""" (User)> SQLAlchemy model """
from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import declarative_base
""" from sqlalchemy import create_engine """
Base = declarative_base()


class User(Base):
    """ users table """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)


""" db_url = "mysql+pymysql://root:0000\
@localhost/user_auth_test"
engine = create_engine(db_url, echo=True)
Base.metadata.create_all(engine) """
