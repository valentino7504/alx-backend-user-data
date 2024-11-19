#!/usr/bin/env python3
'''

authentication module

'''
import bcrypt


def _hash_password(password: str) -> bytes:
    '''hashes password'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
