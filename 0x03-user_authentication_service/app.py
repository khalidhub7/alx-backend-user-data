#!/usr/bin/env python3
""" main app """
from wrappers import (
    AUTH, wrap_register, password_token,
    wrap_login, wrap_logout)
from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/', strict_slashes=False,
           methods=['GET'])
def index():
    """ basic route """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', strict_slashes=False,
           methods=['POST'])
@wrap_register
def register(email, password):
    """ register route 'page' """
    return AUTH.register_user(email, password)


@app.route('/sessions', strict_slashes=False,
           methods=['POST'])
@wrap_login
def login():
    """ login route 'page' """
    pass


@app.route('/sessions', strict_slashes=False,
           methods=['DELETE'])
@wrap_logout
def logout():
    """ logout route 'page' """
    pass


@app.route('/reset_password', strict_slashes=False,
           methods=['POST'])
@password_token
def get_reset_password_token():
    """ get 'reset password token' """
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
