# This file creates a Flask test client that will be used by all unit tests.

import os
import sys
import pytest

# Add the Backend folder to Python's search path.
# This allows the tests to import the Flask application.
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "Backend"
        )
    )
)

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