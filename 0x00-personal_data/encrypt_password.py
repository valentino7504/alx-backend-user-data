#!/usr/bin/env python3
'''

password encryption module

'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''hashes a password with bcrypt'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
