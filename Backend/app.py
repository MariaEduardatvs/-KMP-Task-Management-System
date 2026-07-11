from flask import Flask, render_template, request, redirect
from auth import auth
from data_conn import createConnection, getAllRecords, addRecords

app = Flask(__name__)

#Register authentication routes
app.register_blueprint(auth)

#Connect to MySQL
conn = createConnection()


@app.route("/")
def home():
    tasks = getAllRecords(conn)
    return render_template("index.html", tasks=tasks)


@app.route("/add_task", methods=["POST"])
def add_task():

    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "created_by": 1 #temp user id
        }

    addRecords(conn, data)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)