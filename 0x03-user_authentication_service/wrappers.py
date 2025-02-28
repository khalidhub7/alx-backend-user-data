#!/usr/bin/env python3
""" wrapper functions to modify
route behavior """
from flask import request, jsonify, abort
from functools import wraps
from auth import Auth
AUTH = Auth()


# register_route
def wrap_register(func):
    """ register_route behavior """
    @wraps(func)
    def wrapper():
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            return jsonify({
                "message": "missing email or password"
            }), 400
        try:
            func(email, password)
            return jsonify({
                "email": f"{email}", "message": "user created"
            }), 200
        except ValueError:
            return jsonify({
                "message": "email already registered"
            }), 400
    return wrapper


# login_route
def wrap_login(func):
    """ login_route behavior """
    @wraps(func)
    def wrapper():
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            # validate credentials
            isvalid = AUTH.valid_login(email, password)
            if isvalid:
                sess_id = AUTH.create_session(email)
                response = jsonify({
                    "email": f"{email}", "message": "logged in"
                })
                response.set_cookie('session_id', sess_id)
                return response, 200
            # else
            raise Exception('invalid credentials')
        except Exception:
            abort(401)
    return wrapper


# logout_route
def wrap_logout(func):
    """ logout_route behavior """
    @wraps(func)
    def wrapper():
        try:
            sess_cookie = request.cookies.get('session_id')
            if sess_cookie:
                user = AUTH.get_user_from_session_id(sess_cookie)
                if user:
                    AUTH.destroy_session(user.id)
                    from flask import redirect
                    return redirect('/')
            raise Exception
        except Exception:
            abort(403)
    return wrapper


# reset_token_get_route
def generate_pwdtoken(func):
    @wraps(func)
    def wrapper():
        try:
            email = request.form.get('email')
            reset_token = AUTH.get_reset_password_token(email)
            return jsonify({
                "email": f"{email}", "reset_token": f"{reset_token}"
            }), 200
        except Exception:
            abort(403)
    return wrapper


# update_password
def updatepwd(func):
    @wraps(func)
    def wrapper():
        email = request.form.get('email')
        password = request.form.get('password')
        reset_token = request.form.get('reset_token')
        try:
            AUTH.update_password(reset_token, password)
            return jsonify({
                "email": f"{email}", "message": "Password updated"
            }), 200
        except Exception:
            abort(403)
    return wrapper
