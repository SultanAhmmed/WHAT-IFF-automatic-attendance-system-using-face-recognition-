import pymysql
from pymysql import MySQLError

# Function to establish the connection to MySQL
def connect():
    return pymysql.connect(
        host='localhost',      # or your MySQL host
        user='root',           # replace with your MySQL username
        password='',           # replace with your MySQL password
        database='section_6'  # specify the database name
    )

# Initialize connection variable
connection = None

# Establishing the connection to MySQL and creating database and table
try:
    connection = pymysql.connect(
        host='localhost',      # or your MySQL host
        user='root',           # replace with your MySQL username
        password=''            # replace with your MySQL password
    )
    cursor = connection.cursor()
    
    # Creating the database and table
    cursor.execute("CREATE DATABASE IF NOT EXISTS section_6;")
    cursor.execute("USE section_6;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students_database (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            dept ENUM('CSE', 'EEE', 'BBA', 'English', 'MAS') NOT NULL,
            gender ENUM('Male', 'Female') NOT NULL,
            photo LONGBLOB,
            attendance_count INT NOT NULL DEFAULT 0
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_history (
            attendance_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            date DATE NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students_database(id) ON DELETE CASCADE
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teacher_login (
            teacher_id INT PRIMARY KEY NOT NULL,
            name VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL
        );

    """)

    print("Database and table created successfully!")

except MySQLError as e:
    print(f"Error: {e}")

finally:
    if connection is not None:
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")

# Functions for CRUD operations
def insert(student_id, name, phone, dept, gender, photo):
    conn = connect()
    cursor = conn.cursor()
    sql = "INSERT INTO students_database (id, name, phone, dept, gender, photo) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (student_id, name, phone, dept, gender, photo))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_student():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, dept, gender ,attendance_count FROM students_database")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetch_student_photo():
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT id,name,photo FROM students_database"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if results:
        return results
    return None


def search(column, value):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT id, name, phone, dept, gender FROM students_database WHERE {column} = %s"
    cursor.execute(query, (value,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def id_exists(student_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students_database WHERE id = %s", (student_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def update(student_id, name, phone, dept, gender, photo):
    conn = connect()  
    cursor = conn.cursor()
    
    sql = """UPDATE students_database 
             SET name = %s, phone = %s, dept = %s, gender = %s"""
    
    params = [name, phone, dept, gender]
    
    if photo is not None:
        sql += ", photo = %s" 
        params.append(photo_data)  
    else:
        photo_data = None  
    
    sql += " WHERE id = %s"
    params.append(student_id) 
    
    try:
        cursor.execute(sql, tuple(params))  
        conn.commit() 
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback() 
    finally:
        cursor.close()
        conn.close()


# def update(student_id, name, phone, dept, gender,photo):
#     conn = connect()
#     cursor = conn.cursor()
#     sql = "UPDATE students_database SET name = %s, phone = %s, dept = %s, gender = %s, photo = %s WHERE id = %s"
#     cursor.execute(sql, (name, phone, dept, gender, student_id,photo))
#     conn.commit()
#     cursor.close()
#     conn.close()

def delete(student_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students_database WHERE id = %s", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_all_records():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students_database")
    conn.commit()
    cursor.close()
    conn.close()


def mark_attendance(student_id,name,date):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance_history (student_id,name,date) VALUES (%s, %s, %s)", (student_id,name,date))
    cursor.execute("UPDATE students_database SET attendance_count = attendance_count + 1 WHERE id = %s", (student_id))
    conn.commit()
    cursor.close()
    conn.close()

def attendance_data():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, attendance_count FROM students_database")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
    
def filter_attendance(student_id,month):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""SELECT s.name, a.date 
                    FROM students_database s 
                   JOIN attendance_history a ON s.id = a.student_id
                   WHERE 1=1 AND s.id = %s AND MONTH(a.date) = %s""",(student_id,month))
    query = cursor.fetchall()
    cursor.close()
    conn.close()
    return query

def get_attendance_by_student(student_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name, date FROM attendance_history WHERE student_id = %s",(student_id))
    query = cursor.fetchall()
    cursor.close()
    conn.close()
    return query

def teacher_login_database(user):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name, password FROM teacher_login WHERE teacher_id = %s",(user))
    query = cursor.fetchall()
    cursor.close()
    conn.close()
    return query