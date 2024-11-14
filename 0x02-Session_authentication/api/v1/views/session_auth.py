#!/usr/bin/env python3
""" session authentication Module """
import os
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def all_routes_auth():
    """ handle session login and auth """
    email = request.form.get('email')
    passwd = request.form.get('password')

    if email is None or \
            len(email) == 0:
        return jsonify(
            {"error": "email missing"}), 400
    if passwd is None or \
            len(passwd) == 0:
        return jsonify(
            {"error": "password missing"}), 400
    users = User.search({'email': email})

    if not users:
        return jsonify({"error": "no user fou\
nd for this email"}), 404
    for i in users:
        if i.email == email:
            user = i
    if not user.is_valid_password(passwd):
        return jsonify({"error": "wrong \
password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    responce = jsonify(user.to_json())
    responce.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return responce
