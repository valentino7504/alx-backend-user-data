#!/usr/bin/env python3
'''

authentication module

'''

import bcrypt
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    '''hashes password'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    '''Auth class to interact with the authentication database.
    '''

    def __init__(self) -> None:
        '''dunder init'''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''registers a user'''
        try:
            find_user = self._db.find_user_by(email=email)
            if find_user:
                raise ValueError("User {} already exists".format(email))
        except (NoResultFound, InvalidRequestError):
            hashed = _hash_password(password).decode('utf-8')
            user = self._db.add_user(email, hashed)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        '''validates a login'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password, user.hashed_password)
