# Blueprint for task routes
from flask import Blueprint, request, jsonify

# Database connection
from data_conn import createConnection

# Create Blueprint
tasks = Blueprint("tasks", __name__)


# CREATE TASK
@tasks.route("/tasks", methods=["POST"])
def create_task():

    # Receive JSON data
    data = request.json

    title = data["title"]
    description = data["description"]
    due_date = data["due_date"]

    # Temporary user
    created_by = 1

    conn = createConnection()

    cursor = conn.cursor()

    # Insert new task
    cursor.execute(
        """
        INSERT INTO tasks
        (title, description, due_date, created_by)

        VALUES(%s,%s,%s,%s)
        """,

        (title, description, due_date, created_by)
    )

    conn.commit()

    return jsonify({

        "message":"Task created successfully!"

    })