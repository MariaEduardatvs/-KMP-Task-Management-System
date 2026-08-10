import os
from flask import Flask, render_template, request, redirect, session
from auth import auth
from task import tasks
from data_conn import createConnection, getAllRecords, addRecords

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "Frontend")

app = Flask(__name__,
            template_folder=FRONTEND_DIR,
            static_folder=FRONTEND_DIR)
app.secret_key = "kmp-task-management-secret"

#Register authentication routes
app.register_blueprint(auth)
app.register_blueprint(tasks)

#Connect to MySQL
conn = createConnection()

if conn:
    print("Database connected successfully!")
else:
    print("Database connection failed!")


@app.route("/")
def home():
    tasks = getAllRecords(conn)
    return render_template("index.html", tasks=tasks)


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/tasks")
def tasks_page():
    tasks = getAllRecords(conn)
    return render_template("task.html", tasks=tasks)

@app.route("/add_task", methods=["POST"])
def add_task():

    user_id =session.get("user_id")
    if not user_id:
        return redirect("/login")

    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "due_date": request.form.get("due_date"),
        "created_by": session["user_id"],
        "assigned_to": None
        }

    addRecords(conn, data)
    return redirect("/tasks")


if __name__ == "__main__":
    app.run(debug=True)