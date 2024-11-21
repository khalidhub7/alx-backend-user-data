#!/usr/bin/env python3
""" End-to-end integration test
"""
import requests


def register_user(email: str, password: str) -> None:
    url = "http://your-web-server/register"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    url = "http://your-web-server/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    url = "http://your-web-server/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    return session_id


def profile_unlogged() -> None:
    url = "http://your-web-server/profile"
    response = requests.get(url)
    assert response.status_code == 401


def profile_logged(session_id: str) -> None:
    url = "http://your-web-server/profile"
    headers = {
        "Authorization": f"Bearer {session_id}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    url = "http://your-web-server/logout"
    headers = {
        "Authorization": f"Bearer {session_id}"
    }
    response = requests.post(url, headers=headers)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    url = "http://your-web-server/reset_password"
    data = {
        "email": email
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    reset_token = response.json()["reset_token"]
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    url = "http://your-web-server/update_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200


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
