#!/usr/bin/env python3
""" flask app """
from auth import Auth
from flask import Flask, jsonify, request
from db import DB
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'],
           strict_slashes=True)
def basic():
    """ basic route """
    return jsonify(
        {"message": "Bienvenue"})


@app.route('/users', methods=['POST'],
           strict_slashes=True)
def register():
    """ register page """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify(
            {"email": "{}".format(email),
             "message": "user created"})
    except Exception:
        return jsonify(
            {"message": "\
email already registered"}), 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port="5000")
