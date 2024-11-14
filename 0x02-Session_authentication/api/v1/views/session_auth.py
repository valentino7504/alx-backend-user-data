#!/usr/bin/env python3
'''

files for session auth views

'''
from os import getenv

from flask import jsonify, request

from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    '''login method for handling auth'''
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not pwd:
        return jsonify({'error': 'password missing'}), 400
    user_search = User.search({'email': email})
    if not user_search:
        return jsonify({'error': 'no user found for this email'}), 404
    user: User = user_search[0]
    if not user.is_valid_password(pwd=pwd):
        return jsonify({'error': 'wrong password'}), 401
    from api.v1.app import auth
    session = auth.create_session(user.id)
    cookie_name = getenv('SESSION_NAME')
    response = jsonify(user.to_json())
    response.set_cookie(cookie_name, session)
    return response
