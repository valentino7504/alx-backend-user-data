#!/usr/bin/env python3
'''

authentication module

'''
import uuid
from typing import Union

import bcrypt
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    '''hashes password'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    '''returns string of uuid'''
    return str(uuid.uuid4())


class Auth:
    '''Auth class to interact with the authentication database.
    '''

    def __init__(self) -> None:
        '''dunder init'''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''registers a user'''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            return self._db.add_user(email, hashed)
        else:
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        '''validates a login'''
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        '''creates a session'''
        new_session = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            return None
        self._db.update_user(user.id, session_id=new_session)
        return new_session

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        '''gets user using the session id'''
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except (NoResultFound, InvalidRequestError):
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        '''destroys a session from user instance'''
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        '''returns reset token'''
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        '''updates user password using the reset token'''
        if reset_token is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except (NoResultFound, InvalidRequestError):
            raise ValueError
        hashed_pwd = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_pwd,
            reset_token=None
        )
