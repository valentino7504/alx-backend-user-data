#!/usr/bin/env python3
'''

The flask app

'''
from flask import Flask, abort, jsonify, redirect, request

from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome_route():
    '''welcome to the app'''
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    '''registers users'''
    email = request.form.get('email')
    pwd = request.form.get('password')
    try:
        AUTH.register_user(email, pwd)
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400
    return jsonify({'email': email, 'message': 'user created'})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    '''logs in a user'''
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not AUTH.valid_login(email, pwd):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    '''logs out of a user'''
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    '''returns a user profile'''
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({'email': user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    '''POST for reset password token'''
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        return abort(403)
    return jsonify({'email': email, 'reset_token': reset_token}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
