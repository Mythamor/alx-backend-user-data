#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from typing import Any, Dict, Union

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds and saves a user to the db
        """
        # Set up session
        session = self._session

        # Create instance of new user
        user = User(email=email, hashed_password=hashed_password)

        # Add user to session
        session.add(user)

        # Commit session to save user to db
        session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Takes in arbitrary keyword arguments
        Returns the first row found in the users table as filtered by
        the method’s input arguments.
        """
        # Set up session
        session = self._session

        # Filter
        try:
            result = session.query(User).filter_by(**kwargs).first()
            if result is None:
                raise NoResultFound
            return result
        except (NoResultFound, InvalidRequestError) as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Use find_user_by to locate the user to update,
        update the user’s attributes as passed in the method’s args
        commit changes to the database.
        """

        # Set up session
        session = self._session

        user_to_update = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(User, key):
                setattr(user_to_update, key, value)
            else:
                raise ValueError

        session.commit()
        return None

    def commit(self) -> None:
        """
        Commits changes to the database
        """
        session = self._session
        session.commit()
