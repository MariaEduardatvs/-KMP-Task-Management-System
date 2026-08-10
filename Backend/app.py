from flask import Flask, render_template, request, redirect
from auth import auth
from task import tasks
from data_conn import createConnection, getAllRecords, addRecords, deleteRecord

app = Flask(__name__,
            template_folder="../Frontend",
            static_folder="../Frontend")
app.secret_key = "kmp-task-management-secret"

app.register_blueprint(auth)
app.register_blueprint(tasks)

conn = createConnection()

if conn:
    print("Database connected successfully!")
else:
    print("Database connection failed!")

@app.route("/")
def home():
    tasks_list = getAllRecords(conn) if conn else []
    return render_template("index.html", tasks=tasks_list)

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/tasks")
def tasks_page():
    tasks_list = getAllRecords(conn) if conn else []
    return render_template("task.html", tasks=tasks_list)

@app.route("/add_task", methods=["POST"])
def add_task():
    if not conn:
        return redirect("/tasks")
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "due_date": request.form.get("due_date") or None,
        "created_by": 1
    }
    addRecords(conn, data)
    return redirect("/tasks")

@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if conn:
        deleteRecord(conn, task_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)