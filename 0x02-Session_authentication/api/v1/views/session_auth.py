#!/usr/bin/env python3
""" login / logout """

from flask import request, jsonify
from api.v1.views import app_views


@app_views.route('/auth_session/login',
                 strict_slashes=False, methods=['POST'])
def login():
    """ login route """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    from models.user import User
    found_users = User.search({'email': email})
    if len(found_users) != 0:
        for user in found_users:
            if user.is_valid_password(password):
                # create a session
                from api.v1.app import auth
                from os import getenv
                from flask import make_response
                session_id = auth.create_session(user.id)
                cookie_key = getenv('SESSION_NAME')
                response = make_response(jsonify(user.to_json()), 200)
                response.set_cookie(cookie_key, session_id)
                return response
            return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout',
                 strict_slashes=False, methods=['DELETE'])
def logout():
    """ logout route """
    from api.v1.app import auth
    from flask import abort
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
