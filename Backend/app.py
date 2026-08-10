import os
from flask import Flask, render_template, request, redirect, session
from auth import auth
from task import tasks
from data_conn import createConnection, getAllRecords, addRecords, deleteRecord
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "Frontend")

load_dotenv()

app = Flask(__name__,
            template_folder=FRONTEND_DIR,
            static_folder=FRONTEND_DIR)
app.secret_key = os.getenv("SECRET_KEY", "kmp-task-management-secret")

app.register_blueprint(auth)
app.register_blueprint(tasks)

conn = createConnection()

if conn:
    print("Database connected successfully!")
else:
    print("Database connection failed!")

def get_conn():
    #Return a live db conn. reconnnect if old closed
    global conn
    if conn is None:
        conn = createConnection()
        return conn
    try:
        conn.ping(reconnect=True, attempts=3, delay=1)
    except Exception:
        conn = createConnection()
    return conn

@app.route("/")
def home():
    c = get_conn()
    tasks_list = getAllRecords(c) if c else []
    return render_template("index.html", tasks=tasks_list)

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/tasks")
def tasks_page():
    c = get_conn()
    tasks_list = getAllRecords(c) if c else []
    return render_template("task.html", tasks=tasks_list)

@app.route("/add_task", methods=["POST"])
def add_task():
    c = get_conn()
    if not c:
        return redirect("/tasks")
    
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "due_date": request.form.get("due_date") or None,
        "created_by": user_id,
        "assigned_to": None
    }
    
    addRecords(c, data)
    return redirect("/tasks")

@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    c = get_conn()
    if c:
        deleteRecord(c, task_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)