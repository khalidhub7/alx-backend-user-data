#!/usr/bin/env python3
""" wrapper functions to modify
route behavior """
from flask import request, jsonify


# register_route
def wrap_register(func):
    """ register_route behavior """
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
