import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Encapsulate MySQL connection creation."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="root",  
            database="2wayaccess"
        )
        return conn
    except Error as err:
        print(f"Error connecting to database: {err}")
        return None

def close_db_connection(conn, cursor):
    """Encapsulate closing the database connection."""
    if conn and conn.is_connected():
        cursor.close()
        conn.close()
