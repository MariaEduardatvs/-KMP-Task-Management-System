import mysql.connector

def createConnection():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='password',
            database='kmp_task_management'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"error:{err}")
        return None

def getAllRecords(conn):
    mycursor = conn.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    return mycursor.fetchall()

def addRecords(conn, data):
    mycursor = conn.cursor()
    sql = "INSERT INTO tasks(title, description, due_date, created_by) VALUES (%s, %s, %s, %s)"
    val = (data['title'], data['description'], data.get('due_date'), data['created_by'])
    mycursor.execute(sql, val)
    conn.commit()

def deleteRecord(conn, task_id):
    mycursor = conn.cursor()
    sql = "DELETE FROM tasks WHERE id = %s"
    mycursor.execute(sql, (task_id,))
    conn.commit()