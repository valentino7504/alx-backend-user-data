#!/usr/bin/env python3
'''

A module to implement session auth for ALX tasks

'''
import uuid

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    '''The session authentication class'''

    user_id_by_session_id = {}

    def __init__(self):
        '''dunder init method'''
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        '''create a session ID for user_id'''
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id
        return session_id
