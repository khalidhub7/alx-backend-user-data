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
    def _wrap_register():
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
    return _wrap_register


# login_route
def wrap_login(func):
    """ login_route behavior """
    @wraps(func)
    def _wrap_login():
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
    return _wrap_login


# logout_route
def wrap_logout(func):
    """ logout_route behavior """
    @wraps(func)
    def _wrap_logout():
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
    return _wrap_logout


# reset_token_get_route
def generate_pwd_token(func):
    """ reset_password 'post'_route behavior """
    @wraps(func)
    def _generate_pwd_token():
        try:
            email = request.form.get('email')
            reset_token = AUTH.get_reset_password_token(email)
            return jsonify({
                "email": f"{email}", "reset_token": f"{reset_token}"
            }), 200
        except Exception:
            abort(403)
    return _generate_pwd_token


# update_password
def update_pwd(func):
    """ reset_password 'put'_route behavior """
    @wraps(func)
    def wrap_update_pwd():
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        reset_token = request.form.get('reset_token')
        try:
            AUTH.update_password(reset_token, new_password)
            return jsonify({
                "email": email, "message": "Password updated"
            }), 200
        except ValueError:
            abort(403)
    return wrap_update_pwd


# user profile
def user_profile(func):
    """ user profile route behavior """
    @wraps(func)
    def wrap_userprofile():
        session_id = request.form.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user and session_id:
            return jsonify({
                "email": f"{user.email}"
            }), 200
        abort(403)
    return wrap_userprofile
