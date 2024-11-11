#!/usr/bin/env python3
'''

This is the auth file

'''
from typing import Any, List, TypeVar

from flask import request


class Auth():
    '''authentication class'''
    def __init__(self) -> None:
        '''init method'''
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''checks if a path requires authentication'''
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        return not path.rstrip('/') in [p.rstrip('/') for p in excluded_paths]

    def authorization_header(self, request=None) -> Any:
        '''auth header'''
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        '''current user'''
        return None
