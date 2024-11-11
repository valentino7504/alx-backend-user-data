#!/usr/bin/env python3
'''

Basic Auth class

'''
import base64
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    '''Basic auth'''

    def __init__(self):
        '''init method'''
        super().__init__()

    def __is_base64(self, string: str) -> bool:
        '''checks if a string is valid base64'''
        try:
            base64.b64decode(string, validate=True)
            return True
        except Exception:
            return False

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        '''extracts base 64'''
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        '''decode base 64'''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        if not self.__is_base64(base64_authorization_header):
            return None
        return base64.b64decode(base64_authorization_header).decode('utf-8')

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        '''extracting user credentials'''
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        '''show user object from the credentials'''
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search(attributes={'email': user_email})
            if not users:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''overload Auth and retrieve User instance'''
        auth_header = self.authorization_header(request)
        base64_val = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(base64_val)
        user_creds = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(user_creds[0], user_creds[1])
