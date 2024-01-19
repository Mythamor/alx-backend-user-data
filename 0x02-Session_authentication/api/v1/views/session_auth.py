#!/usr/bin/env python3

"""
Module: session_auth.py
    View that handles all routes for session auth
"""

from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_auth_session():
    """
    POST:
        /api/v1/auth_session/login
    Handles session auth for user login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email is None:
        return jsonify({"error": "email missing"}), 400

    if not password or password is None:
        return jsonify({"error": "password missing"}), 400

    # Return list of filtered emails using search
    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    # Check for password in each of the users
    for user in users:
        user_pass = User.search({"email": users})

        if user_pass:
            upass = user_pass.pop()

            if u_pass.is_valid_password(password):

                # Create session ID for User ID
                from api.v1.app import auth
                session_id = auth.SessionAuth.create_session(upass.id)

                # Return the dict repr of the user
                user_data = upass.to_json()

                # Set the cookie to the response
                response = jsonify(user_data)
                response.set_cookie(app.config['SESSION_NAME'], session_id)

                return response

    # If no valid response is found
    return jsonify({"error": "wrong password"}), 401
