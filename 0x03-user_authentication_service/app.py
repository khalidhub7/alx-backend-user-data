#!/usr/bin/env python3
""" main app """
from wrappers import wrap_register
from flask import Flask, jsonify
from auth import Auth
AUTH = Auth()
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
