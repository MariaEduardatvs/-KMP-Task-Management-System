# Blueprint for task routes
from flask import Blueprint, request, jsonify, session

# Database connection
from data_conn import createConnection

# Create Blueprint
tasks = Blueprint("tasks", __name__)


# CREATE TASK
@tasks.route("/tasks", methods=["POST"])
def create_task():

    # Receive JSON data
    data = request.json

    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")
    assigned_to = data.get("assigned_to")

    # Check required fields
    if not title:
        return jsonify({
            "message": "Task title is required."
        }), 400

    if not due_date:
        return jsonify({
            "message": "Due date is required."
        }), 400


    #Get the logged-in user's ID
    created_by = session.get("user_id")
    if not created_by:
        return jsonify({
            "message": "User must be logged in."
            }), 401

    conn = createConnection()

    if not conn:
        return jsonify({
            "message": "Database connection error."
        }), 500

    cursor = conn.cursor()

    # Insert new task
    cursor.execute(
        """
        INSERT INTO tasks
        (title, description, due_date, created_by, assigned_to)

        VALUES(%s,%s,%s,%s,%s)
        """,

        (title, description, due_date, created_by, None)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({

        "message":"Task created successfully!"

    }), 201

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
        SET status = 'COMPLETED'
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


#Sub-Tasks

@tasks.route("/tasks/<int:task_id>/subtasks",methods=["POST"])
def create_subtask(task_id):
    data = request.json

    if not data:
        return jsonify({
            "message": "No data provided."
        }), 400

    title = data.get("title")

    if not title:
        return jsonify({
            "message": "Sub-task title is required."
        }), 400

    conn = createConnection()

    if not conn:
        return jsonify({
            "message": "Database connection error."
        }), 500

    cursor = conn.cursor(dictionary=True)

    #Check that parent task exists
    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    task = cursor.fetchone()

    if not task:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Parent task not found."
        }), 404

    #Create sub-task
    cursor.execute(
        """
        INSERT INTO subtasks
        (task_id, title)
        VALUES (%s, %s)
        """,
        (task_id, title)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Sub-task created successfully!"
    }), 201



#View Sub-tasks


@tasks.route("/tasks/<int:task_id>/subtasks", methods=["GET"])
def get_subtasks(task_id):

    conn = createConnection()

    if not conn:
        return jsonify({
            "message": "Database connection error."
        }), 500

    cursor = conn.cursor(dictionary=True)

    #Check parent task
    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    task = cursor.fetchone()

    if not task:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Parent task not found."
        }), 404

    #Get subtasks
    cursor.execute(
        """
        SELECT *
        FROM subtasks
        WHERE task_id = %s
        ORDER BY id
        """,
        (task_id,)
    )

    subtasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        "subtasks": subtasks
    }), 200


# Complete Sub-Tasks

@tasks.route("/subtasks/<int:subtask_id>/complete", methods=["PUT"])
def complete_subtask(subtask_id):

    conn = createConnection()

    if not conn:
        return jsonify({
            "message": "Database connection error."
        }), 500

    cursor = conn.cursor()

    #Mark sub-task as completed
    cursor.execute(
        """
        UPDATE subtasks
        SET completed = TRUE
        WHERE id = %s
        """,
        (subtask_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Sub-task not found."
        }), 404

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Sub-task completed successfully!"
    }), 200


# Delete Sub-tasks

@tasks.route("/subtasks/<int:subtask_id>", methods=["DELETE"])
def delete_subtask(subtask_id):
    conn = createConnection()

    if not conn:
        return jsonify({
            "message": "Database connection error."
        }), 500

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM subtasks
        WHERE id = %s
        """,
        (subtask_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Sub-task not found."
        }), 404

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Sub-task deleted successfully!"
    }), 200
