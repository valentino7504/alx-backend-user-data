#!/usr/bin/env python3
'''

The flask app

'''
from flask import Flask, abort, jsonify, request

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
