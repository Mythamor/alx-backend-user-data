#!/usr/bin/env python3

"""
Module: app.py
"""

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
