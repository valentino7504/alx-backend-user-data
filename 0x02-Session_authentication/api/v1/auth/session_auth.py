#!/usr/bin/env python3
'''

A module to implement session auth for ALX tasks

'''
import uuid

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    '''The session authentication class'''

    user_id_by_session_id: dict = {}

    def __init__(self):
        '''dunder init method'''
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        '''create a session ID for user_id'''
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''get user id based on session id'''
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''returns current user'''
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        '''destroys a session'''
        if request is None:
            return False
        if self.session_cookie(request) is None:
            return False
        session_id = self.session_cookie(request)
        if self.user_id_for_session_id(session_id) is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
