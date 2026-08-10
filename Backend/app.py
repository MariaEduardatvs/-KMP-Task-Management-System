from flask import Flask, render_template, request, redirect
from auth import auth
from task import tasks
from data_conn import createConnection, getAllRecords, addRecords


app = Flask(__name__,
            template_folder="../Frontend",
            static_folder="../Frontend")
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

    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "due_date": request.form.get("due_date"),
        "created_by": 1, #temp user id
        "assigned_to": None
        }

    addRecords(conn, data)
    return redirect("/tasks")


if __name__ == "__main__":
    app.run(debug=True)