#!/usr/bin/env python3
""" main app """
from wrappers import wrap_register, wrap_login, AUTH
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
