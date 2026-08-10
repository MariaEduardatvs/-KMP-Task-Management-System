# This file creates a Flask test client that will be used by all unit tests.

import os
import sys
import pytest

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

BACKEND_PATH = os.path.join(PROJECT_ROOT, "Backend")

sys.path.insert(0, BACKEND_PATH)

# Import the Flask application.
from app import app


# Create a Flask test client.
@pytest.fixture
def client():

    # Enable testing mode.
    app.config["TESTING"] = True

    # Create the test client.
    with app.test_client() as client:

        # Make the client available to every test.
        yield client