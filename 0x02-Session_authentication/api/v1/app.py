#!/usr/bin/env python3
'''
Route module for the API
'''
from os import getenv

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r'/api/v1/*': {'origins': '*'}})
auth_type = getenv('AUTH_TYPE', None)
auth = BasicAuth() if auth_type == 'basic_auth' else Auth()


@app.before_request
def validate_request():
    '''validates each request'''
    if auth is None:
        return None
    exempt_list = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if not auth.require_auth(request.path, exempt_list):
        return None
    if auth.authorization_header(request) is None:
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
