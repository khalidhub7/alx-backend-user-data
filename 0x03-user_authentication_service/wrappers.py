#!/usr/bin/env python3
""" wrapper functions to modify
route behavior """
from flask import request, jsonify, abort
from auth import Auth
AUTH = Auth()


# register_route
def wrap_register(func):
    """ register_route behavior """
    def wrapped_register():
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
    return wrapped_register


# login_route
def wrap_login(func):
    """ login_route behavior """
    def wrapped_login():
        email = request.form.get('email')
        password = request.form.get('password')
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
            raise Exception('invalid credentials')
        except Exception:
            abort(401)
    return wrapped_login
