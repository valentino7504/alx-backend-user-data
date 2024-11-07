#!/usr/bin/env python3
'''

password encryption module

'''
from bcrypt import gensalt, hashpw


def hash_password(password: str) -> bytes:
    '''hashes a password with bcrypt'''
    return hashpw(password.encode(), gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''checks if password is valid'''
    return hashpw(password.encode(), hashed_password) == hashed_password
