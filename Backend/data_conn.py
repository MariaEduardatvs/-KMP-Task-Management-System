import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# database conn setup
def createConnection():
        try:
                conn = mysql.connector.connect(
                        host=os.getenv("DB_HOST"),
                        user=os.getenv("DB_USER"),
                        password=os.getenv("DB_PASSWORD"),
                        database=os.getenv("DB_NAME")
                )
                return conn
        except mysql.connector.Error as err:
                print(f"error:{err}")
                return None
#grab data
def getAllRecords(conn):
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM tasks")
        return mycursor.fetchall()

#give data
def addRecords(conn,data):
        mycursor = conn.cursor()
        sql = "INSERT INTO tasks(title, description, created_by) VALUES (%s, %s, %s)"
        val = (data['title'], data['description'],  data['created_by'])
        mycursor.execute(sql, val)
        conn.commit()