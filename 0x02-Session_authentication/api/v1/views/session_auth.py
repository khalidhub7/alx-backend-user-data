#!/usr/bin/env python3
""" session authentication Module """
import os
from models.user import User
from uuid import uuid4
from api.v1.auth.auth import Auth
from api.v1.views import app_views
from flask import request, jsonify


class SessionAuth(Auth):
    """ Manages session ID """
    user_id_by_session_id = {}

    def create_session(
            self, user_id: str = None
    ) -> str:
        """ Generates a new session ID """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[
            session_id] = user_id
        return session_id

    def user_id_for_session_id(
            self, session_id: str = None) -> str:
        """
returns a User ID based on a Session ID """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        value = SessionAuth.user_id_by_session_id.get(
            session_id)
        return value

    def current_user(self, request=None):
        """ returns a User instance
based on a cookie value """
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)


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
