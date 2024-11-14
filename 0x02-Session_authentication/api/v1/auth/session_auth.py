#!/usr/bin/env python3
'''

A module to implement session auth for ALX tasks

'''
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    '''The session authentication class'''

    def __init__(self):
        '''dunder init method'''
        super().__init__()
