#!/usr/bin/env python3
""" test user_auth project """
import requests
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email, pswd) -> None:
    req = requests.post(
        "http://localhost:5000/users",
        data={'email': email, 'password': pswd}
    )
    assert req.status_code == 200
    assert req.json() == {
        "email": f"{email}", "message": "user created"
    }


def log_in_wrong_password(email, wrong_pswd):
    req = requests.post(
        'http://localhost:5000/sessions',
        data={'email': email, 'password': wrong_pswd}
    )
    assert req.status_code == 401


def profile_unlogged():
    req = requests.get("http://localhost:5000/profile")
    assert req.status_code == 403


def log_in(email, pswd):
    req = requests.post(
        "http://localhost:5000/sessions",
        data={'email': email, 'password': pswd}
    )
    assert req.status_code == 200
    assert req.json() == {
        "email": f"{email}", "message": "logged in"
    }
    return req.cookies.get("session_id")


def profile_logged(session_id):
    req = requests.get(
        "http://localhost:5000/profile",
        cookies={"session_id": session_id}
    )
    assert req.status_code == 200


def reset_password_token(email):
    req = requests.post(
        'http://localhost:5000/reset_password',
        data={'email': email}
    )
    assert req.status_code == 200
    reset_token = req.json().get('reset_token')
    assert reset_token is not None
    return reset_token


def update_password(email, reset_token, new_pswd):
    req = requests.put(
        'http://localhost:5000/reset_password',
        data={'email': email, 'reset_token': reset_token,
              'new_password': new_pswd}
    )
    assert req.status_code == 200
    assert req.json() == {
        "email": email, "message": "Password updated"
    }


def log_out(session_id):

    req = requests.delete(
        'http://localhost:5000/sessions',
        cookies={'session_id': session_id}
    )
    # not 302 because it redirect to homepage /
    assert req.status_code == 200
    assert req.cookies.get("session_id") != session_id
    assert req.cookies.get("session_id") is None


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_out(session_id)
