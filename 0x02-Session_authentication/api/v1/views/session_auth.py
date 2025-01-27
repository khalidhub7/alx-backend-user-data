#!/usr/bin/env python3
""" module of session_auth views """

from flask import request, jsonify, abort
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login():
    """ login page """
    # fetch user credentials
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # find appropriate user
    user = None
    found_users = User.search({'email': email})
    if len(found_users) != 0:
        for i in found_users:
            if i.is_valid_password(password):
                user = i
                break
        if not user:
            return jsonify({"error": "wrong password"}), 401
    else:
        return jsonify(
            {"error": "no user found for this email"}), 404

    # if user find
        # create session
    from api.v1.app import auth
    from os import getenv
    from flask import make_response
    session_id = auth.create_session(user.id)
    # set cookie
    res = make_response(jsonify(user.to_json()))
    cookie_key = getenv("SESSION_NAME")
    if cookie_key:
        res.set_cookie(cookie_key, session_id)
    return res


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ logout page """
    from api.v1.app import auth
    status = auth.destroy_session(request)
    if status is False:
        abort(404)
    return jsonify({}), 200
