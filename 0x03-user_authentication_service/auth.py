#!/usr/bin/env python3
'''

authentication module

'''
import bcrypt
from sqlalchemy.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    '''hashes password'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth():
    '''Auth class to interact with the authentication database.
    '''

    def __init__(self) -> None:
        '''dunder init'''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''registers a user'''
        try:
            user_check = self._db.find_user_by(email=email)
            raise ValueError(f'User {user_check.email} already exists.')
        except NoResultFound:
            pass
        hashed_pwd = _hash_password(password)
        return self._db.add_user(email, hashed_pwd)
