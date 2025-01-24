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

auth_method = (os.getenv('AUTH_TYPE'), None)
if auth_method:
    if auth_method == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()
    if auth_method == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    if auth_method == 'session_auth':
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
def befoore_request():
    """ before request method """
    exclude_auth = ['/api/v1/status/',
                    '/api/v1/unauthorized/',
                    '/api/v1/forbidden/']
    req_auth = auth.require_auth(
        request.path, exclude_auth)
    auth_header = auth.authorization_header(request)

    if auth and req_auth:
        if not auth_header:
            abort(401)
        current_user = auth.current_user(request)
        if not current_user:
            abort(403)
        request.current_user = current_user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
