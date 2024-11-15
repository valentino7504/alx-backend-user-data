#!/usr/bin/env python3
'''

session auth with expiry

'''
from datetime import datetime, timedelta
from os import getenv

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    '''session auth with expiry class'''

    def __init__(self) -> None:
        '''dunder init method'''
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', "0"))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        '''create a session id'''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''get user id for session id'''
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_details: dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_details.get('user_id')
        if 'created_at' not in session_details:
            return None
        created = session_details['created_at']
        time_change = timedelta(seconds=self.session_duration)
        expired = created + time_change < datetime.now()
        if expired:
            return None
        return session_details.get('user_id')
