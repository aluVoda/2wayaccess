import mysql.connector

def connect_to_database():
    """Establishes connection to the 2wayaccess MySQL database."""
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': '2wayaccess',
        'raise_on_warnings': True
    }
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
