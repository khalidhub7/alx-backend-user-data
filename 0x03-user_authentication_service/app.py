#!/usr/bin/env python3
""" flask app """
from db import DB
from auth import Auth
from flask import (Flask, jsonify, request,
                   make_response, abort, redirect)
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'],
           strict_slashes=False)
def basic():
    """ basic route """
    return jsonify(
        {"message": "Bienvenue"})


@app.route('/users', methods=['POST'],
           strict_slashes=False)
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


@app.route('/sessions', methods=['POST'],
           strict_slashes=False)
def login():
    """ login page """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        new_session = AUTH.create_session(email)
        response = make_response(jsonify(
            {"email": email, "message": "logged in"}))
        response.set_cookie("session_id", new_session)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'],
           strict_slashes=False)
def logout():
    """ logout page """
    try:
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect('/')
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port="5000")
