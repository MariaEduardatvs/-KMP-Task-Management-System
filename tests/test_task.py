# This file contains unit tests for the task routes.

import json


# This test verifies that the home page can be loaded successfully.
def test_home_page(client):

    # Send a GET request to the home page.
    response = client.get("/")

    # Verify that the request was successful.
    assert response.status_code == 200


# This test verifies that a new task can be created successfully.
def test_create_task(client):

    # Register a user because the tasks table
    # requires a valid user ID (created_by = 1).
    client.post(
        "/register",
        json={
            "username": "task_user",
            "password": "123456"
        }
    )

    # Send a POST request to create a new task.
    response = client.post(
        "/tasks",
        json={
            "title": "PyTest Task",
            "description": "Task created during automated testing.",
            "due_date": "2026-08-05 18:00:00"
        }
    )

    # Verify that the request was successful.
    assert response.status_code == 200

    # Convert the JSON response into a Python dictionary.
    data = response.get_json()

    # Verify that the correct success message is returned.
    assert data["message"] == "Task created successfully!"