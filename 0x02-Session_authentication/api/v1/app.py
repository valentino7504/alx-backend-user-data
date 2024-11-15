#!/usr/bin/env python3
'''
Route module for the API
'''
from os import getenv

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r'/api/v1/*': {'origins': '*'}})
auth_type = getenv('AUTH_TYPE', None)
if auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'session_auth':
    auth = SessionAuth()
elif auth_type == 'session_exp_auth':
    auth = SessionExpAuth()
else:
    auth = Auth()


@app.before_request
def validate_request():
    '''validates each request'''
    if auth is None:
        return None
    exempt_list = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login'
    ]
    if not auth.require_auth(request.path, exempt_list):
        return None
    auth_head = auth.authorization_header(request)
    if auth_head is None and auth.session_cookie(request) is None:
        return abort(401)
    request.current_user = auth.current_user(request)
    if request.current_user is None:
        return abort(403)
    return None


@app.errorhandler(404)
def not_found(error) -> tuple:
    ''' Not found handler
    '''
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(401)
def unauthorised(e):
    '''unauthorised error handler'''
    return jsonify({'error': 'Unauthorized'}), 401


@app.errorhandler(403)
def forbidden(e):
    '''forbidden error handler'''
    return jsonify({'error': 'Forbidden'}), 403


if __name__ == '__main__':
    host = getenv('API_HOST', '0.0.0.0')
    port = getenv('API_PORT', '5000')
    app.run(host=host, port=port)
