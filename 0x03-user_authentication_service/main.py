#!/usr/bin/env python3
""" test user_auth project """

import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email, pswd) -> None:
    req = requests.post(
        "http://localhost:5000/users",
        data={'email': email, 'password': pswd})
    assert req.json() == {
        "email": f"{email}", "message": "user created"}


def log_in_wrong_password(email, wrong_pswd):
    req = requests.post(
        'http://localhost:5000/sessions',
        data={'email': email, 'password': wrong_pswd})
    assert req.status_code == 401


def profile_unlogged():
    req = requests.get("http://localhost:5000/sessions")
    assert req.cookies.get("session_id") is None


def log_in(email, pswd):
    req = requests.post(
        "http://localhost:5000/sessions",
        data={'email': email, 'password': pswd})
    assert req.json() == {
        "email": f"{email}", "message": "logged in"}
    return req.cookies.get("session_id")


def profile_logged(session_id):
    assert session_id is not None


def log_out(session_id):
    req = requests.delete(
        'http://localhost:5000/sessions',
        cookies={"session_id": session_id})
    assert req.cookies.get("session_id") is None


def reset_password_token(email):
    req = requests.post(
        'http://localhost:5000/reset_password',
        data={'email': email})
    reset_token = req.json().get('reset_token')
    assert reset_token is not None
    return reset_token


def update_password(email, reset_token, new_pswd):
    req = requests.put(
        'http://localhost:5000/reset_password',
        data={'email': email, 'reset_token': reset_token,
              'new_password': new_pswd})


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    print(reset_token)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
