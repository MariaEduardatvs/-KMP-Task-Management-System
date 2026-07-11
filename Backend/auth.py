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


