#!/usr/bin/env python3
'''
Main file
'''
import requests

BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    '''registers a user'''
    form_data = {'email': email, 'password': password}
    res = requests.post(f'{BASE_URL}/users', data=form_data)
    assert res.status_code == 200
    assert res.json() == {'email': email, 'message': 'user created'}
    res = requests.post(f'{BASE_URL}/users', data=form_data)
    assert res.status_code == 400
    return


def log_in_wrong_password(email: str, password: str) -> None:
    '''log in with wrong password'''
    form_data = {'email': email, 'password': password}
    res = requests.post(f'{BASE_URL}/sessions', data=form_data)
    assert res.status_code == 401
    return


def profile_unlogged() -> None:
    '''access profile without logging in'''
    res = requests.get(f'{BASE_URL}/profile', cookies={'session_id': None})
    assert res.status_code == 403
    return


def log_in(email: str, password: str) -> str:
    '''tests login'''
    form_data = {'email': email, 'password': password}
    res = requests.post(f'{BASE_URL}/sessions', data=form_data)
    assert res.status_code == 200
    session_id = res.cookies.get_dict().get('session_id')
    assert session_id
    assert res.json() == {'email': email, 'message': 'logged in'}
    return session_id


def profile_logged(session_id: str) -> str:
    '''tests get profile when logged in'''
    cookies = {'session_id': session_id}
    res = requests.get(f'{BASE_URL}/profile', cookies=cookies)
    assert res.status_code == 200
    assert res.json() == {'email': EMAIL}
    return


def log_out(session_id: str) -> None:
    '''attempts to logout'''
    cookies = {'session_id': session_id}
    res = requests.delete(f'{BASE_URL}/sessions', cookies=cookies)
    assert res.status_code == 200
    assert res.json() == {'message': 'Bienvenue'}
    res2 = requests.delete(f'{BASE_URL}/sessions', cookies=cookies)
    assert res2.status_code == 403
    return


def reset_password_token(email: str) -> str:
    '''resets password token'''
    form_data = {'email': email}
    res = requests.post(f'{BASE_URL}/reset_password', data=form_data)
    assert res.status_code == 200
    reset_token = res.json()['reset_token']
    assert res.json() == {'email': email, 'reset_token': reset_token}
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''update password'''
    form_data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    res = requests.put(f'{BASE_URL}/reset_password', data=form_data)
    assert res.status_code == 200
    assert res.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
