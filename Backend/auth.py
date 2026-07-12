#REGISTRAR USUÁRIO: 
# Receive username and password
# Checks if the user already exists
#If it exists, it returns error 400

# blueprint for organize the routes in different files 
#request to get the data from the user
#jsonify to convert python to json 
#session to store user information during login 
from flask import Blueprint, request, jsonify, session

#connection to the database 
from data_conn import createConnection 

#Blueprint called auth
auth = Blueprint("auth", __name__)

# REGISTER
@auth.route("/register", methods=["POST"])
def register():

#get data sent in JSON format
    data = request.json
#get username and password from json
    username = data["username"]
    password = data["password"]

    conn = createConnection() #connection 

cursor = conn.cursor(dictionary=True) #cursor to execute sql and  dictionary=True to change from tupla to dictionary 

#check if the user name already exists in the database
cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (username,)
    )

#get the first name
user = cursor.fetchone()

#return an error if the user already exists
if user:
        return jsonify({
            "message": "Username already exists."
        }), 400

#if dont exists it will insert the new user name
cursor.execute(
        """
        INSERT INTO users(username,password)
        VALUES(%s,%s)
        """,
        (username, password)
    )

#save it in the database
conn.commit()

#success message
return jsonify({
        "message": "User registered successfully!"
    })
