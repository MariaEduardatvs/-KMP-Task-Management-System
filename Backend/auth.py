#register user
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

# LOGIN: 
#Receive username and password
#check for a user with this information
#If found, save the user ID in the session
#If it cannot be found, it returns error 401


@auth.route("/login", methods=["POST"])
def login():

    # Receives the data sent by the user
    data = request.json

    # Get username and password
    username = data["username"]
    password = data["password"]

    # Connect to the bank
    conn = createConnection()

    # Create cursor
    cursor = conn.cursor(dictionary=True)

    # Search for a user with this username and password
    cursor.execute(
        """
        SELECT * FROM users
        WHERE username=%s
        AND password=%s
        """,
        (username, password)
    )

    # Get the user found
    user = cursor.fetchone()

    # If not found, invalid login
    if not user:
        return jsonify({
            "message": "Invalid username or password."
        }), 401
    
    # Stores the user ID in the session
    # This indicates that the user is logged in
    session["user_id"] = user["id"]

    # Returns success
    return jsonify({
        "message": "Login successful!"
    })





