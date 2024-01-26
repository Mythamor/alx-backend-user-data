#!/usr/bin/env python3

"""
Module: app.py
"""

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def message():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():

    # Get form data
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        # Try register the user
        AUTH.register_user(email, password)

        # Return created user
        return jsonify({"email": email, "message": "user created"}), 200

    # Raise error if user already registered
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    Handles login requests
    """
    # Get form data
    email = request.form.get("email")
    password = request.form.get("password")

    # Authenticate user
    if AUTH.valid_login(email, password):
        # Create a new session id
        session_id = AUTH.create_session(email)

        # Set the sessio ID as a cookie in the response
        response = make_response(jsonify({f"email": "{email}",
                                         "message": "logged in"}))
        response.set_cookie('session_id', session_id)

        return response

    # If auth fails/ login info is incorrect, abort with 401
    abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    Deletes and logs out of the session
    """
    # Extract session ID from cookie
    session_id = request.cookies.get('session_id')

    # Find user with session ID
    user = auth.get_user_from_session_id(session_id)

    if user is not None:
        # Destroy session and redirect to /
        response = redirect('/')
        response.delete_cookie('session_id')
        return response
    else:
        # I f user does not exist abort 403
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
