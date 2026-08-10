# This file contains unit tests for the authentication routes.

import json


# This test verifies that a new user can successfully register
# when a unique username is provided.
def test_register_success(client):

    # Send a POST request to the registration endpoint
    # with a valid username and password.
    response = client.post(
        "/register",
        json={
            "username": "pytest_user_01",
            "password": "123456"
        }
    )

    # Verify that the request was successful.
    assert response.status_code == 200

    # Convert the JSON response into a Python dictionary.
    data = response.get_json()

    # Verify that the correct success message is returned.
    assert data["message"] == "User registered successfully!"


# This test verifies that the system does not allow
# two users with the same username.
def test_register_duplicate_username(client):

    # Register the user for the first time.
    client.post(
        "/register",
        json={
            "username": "duplicate_user",
            "password": "123456"
        }
    )

    # Try to register the same username again.
    response = client.post(
        "/register",
        json={
            "username": "duplicate_user",
            "password": "123456"
        }
    )

    # Verify that the request returns HTTP 400 (Bad Request).
    assert response.status_code == 400

    # Convert the JSON response into a Python dictionary.
    data = response.get_json()

    # Verify that the expected error message is returned.
    assert data["message"] == "Username already exists."


# This test verifies that an existing user
# can successfully log into the system.
def test_login_success(client):

    # Register a new user before attempting login.
    client.post(
        "/register",
        json={
            "username": "login_user",
            "password": "123456"
        }
    )

    # Send a login request using the same credentials.
    response = client.post(
        "/login",
        json={
            "username": "login_user",
            "password": "123456"
        }
    )

    # Verify that the login request was successful.
    assert response.status_code == 200

    # Convert the JSON response into a Python dictionary.
    data = response.get_json()

    # Verify that the success message is returned.
    assert data["message"] == "Login successful!"


# This test verifies that login fails
# when invalid credentials are provided.
def test_login_invalid_credentials(client):

    # Send a login request using incorrect credentials.
    response = client.post(
        "/login",
        json={
            "username": "wrong_user",
            "password": "wrong_password"
        }
    )

    # Verify that HTTP status code 401 is returned.
    assert response.status_code == 401

    # Convert the JSON response into a Python dictionary.
    data = response.get_json()

    # Verify that the correct error message is returned.
    assert data["message"] == "Invalid username or password."


# This test verifies that the logout endpoint
# clears the current user session.
def test_logout(client):

    # Send a POST request to the logout endpoint.
    response = client.post("/logout")

    # Verify that the logout request was successful.
    assert response.status_code == 200

    # Convert the JSON response into a Python dictionary.
    data = response.get_json()

    # Verify that the correct success message is returned.
    assert data["message"] == "Logout successful!"