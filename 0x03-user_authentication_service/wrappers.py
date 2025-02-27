#!/usr/bin/env python3
""" wrapper functions to modify
route behavior """
from flask import request, jsonify, abort
from auth import Auth
AUTH = Auth()

# request credentials
email = request.form.get('email')
password = request.form.get('password')


# register_route
def wrap_register(func):
    """ register_route behavior """
    def wrapped_register():
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
    return wrapped_register


# login_route
def wrap_login(func):
    """ login_route behavior """
    def wrapped_login():
        try:
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
    return wrapped_login


def wrap_logout(func):
    """ logout_route behavior """
    def wrapped_logout():
        try:
            sess_cookie = request.cookies.get('session_id')
            user = AUTH.get_user_from_session_id(sess_cookie)
            AUTH.destroy_session(user.id)
            from flask import redirect
            redirect('app.sessions')
        except Exception:
            abort(403)
    return wrapped_logout
