import mysql.connector
from datetime import datetime

# MySQL connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',        # Hostname of the MySQL server (e.g., 'localhost')
        database='2wayaccess', # Name of the MySQL database
        user='root',     # MySQL username
        password='root'  # MySQL password
    )    
    return conn

def log_access_to_db(employee_id, timestamp, action):
    """Log access event into the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO access_logs (employee_id, timestamp, action) VALUES (%s, %s, %s)"
    cursor.execute(query, (employee_id, timestamp, action))
    conn.commit()
    
    cursor.close()
    conn.close()

def get_employee_logs(employee_id, date=None):
    """Retrieve employee logs from the database"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if date:
        query = "SELECT * FROM access_logs WHERE employee_id = %s AND DATE(timestamp) = %s ORDER BY timestamp"
        cursor.execute(query, (employee_id, date))
    else:
        query = "SELECT * FROM access_logs WHERE employee_id = %s ORDER BY timestamp"
        cursor.execute(query, (employee_id,))
    
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return rows

def get_employee_status(employee_id):
    """Fetch the employment status of an employee from the database"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT employment_status FROM employees WHERE employee_id = %s"
    cursor.execute(query, (employee_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result['employment_status']
    else:
        return None
