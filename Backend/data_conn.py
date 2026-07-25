import mysql.connector

# database conn setup
def createConnection():
        try:
                conn = mysql.connector.connect(
                        host='127.0.0.1',
                        user='root',
                        password='',
                        database='kmp_task_management'
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