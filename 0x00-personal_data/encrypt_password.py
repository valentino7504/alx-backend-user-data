#!/usr/bin/env python3
'''

password encryption module

'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''hashes a password with bcrypt'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''checks if password is valid'''
    return bcrypt.checkpw(password.encode(), hashed_password)
