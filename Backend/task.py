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

#TASK COMPLETION

@tasks.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def complete_task(task_id):

    conn = createConnection()

    if not conn:
        return jsonify({
            "message": "Database connection error."
        }), 500

    cursor = conn.cursor(dictionary=True)

    # Check whether task exists
    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    task = cursor.fetchone()

    if not task:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Task not found."
        }), 404

    # Mark task as completed
    cursor.execute(
        """
        UPDATE tasks
        SET status = 'Completed'
        WHERE id = %s
        """,
        (task_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": f"Task '{task['title']}' has been completed."
    }), 200



# Task Deletion

@tasks.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    conn = createConnection()

    if not conn:
        return jsonify({
            "message": "Database connection error."
        }), 500

    cursor = conn.cursor(dictionary=True)

    # Check whether task exists
    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    task = cursor.fetchone()

    if not task:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Task not found."
        }), 404

    # Delete the task
    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": f"Task '{task['title']}' has been deleted."
    }), 200



# Edit task

@tasks.route("/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id):

    data = request.json

    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")
    assigned_to = data.get("assigned_to")

    if not title:
        return jsonify({
            "message": "Task title is required."
        }), 400

    if not due_date:
        return jsonify({
            "message": "Due date is required."
        }), 400

    conn = createConnection()

    if not conn:
        return jsonify({
            "message": "Database connection error."
        }), 500

    cursor = conn.cursor(dictionary=True)

    # Check whether task exists
    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    task = cursor.fetchone()

    if not task:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Task not found."
        }), 404

    # Update task
    cursor.execute(
        """
        UPDATE tasks
        SET title = %s,
            description = %s,
            due_date = %s,
            assigned_to = %s
        WHERE id = %s
        """,
        (
            title,
            description,
            due_date,
            assigned_to,
            task_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Task updated successfully!"
    }), 200
