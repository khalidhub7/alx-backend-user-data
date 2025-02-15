#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth = None
auth_type = os.getenv('AUTH_TYPE')
if auth_type:
    if auth_type == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()
    if auth_type == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    if auth_type == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(err) -> str:
    """ unauthorized handler """
    return jsonify(
        {"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_page(err):
    """ forbidden handler """
    return jsonify(
        {"error": "Forbidden"}), 403


@app.before_request
def beforerequest():
    """ before request method """
    excluded_Paths = ['/api/v1/status/', '/api/v1\
/unauthorized/', '/api/v1/forbidden/']
    isAuthNeeded = auth.require_auth(request.path, excluded_Paths)

    if auth and isAuthNeeded:
        auth_header = auth.authorization_header(request)
        if not auth_header:
            abort(401)  # unauthorized

        user = auth.current_user(request)
        if not user:
            abort(403)  # forbidden
        request.current_user = user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
