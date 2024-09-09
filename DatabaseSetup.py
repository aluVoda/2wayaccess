import mysql.connector

def create_db_and_tables():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Adjust as per your MySQL credentials
            password="root"  # Adjust as per your MySQL password
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS 2wayaccess")
        cursor.execute("USE 2wayaccess")

        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                employment_status ENUM('full-time', 'part-time') NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS access_logs (
                log_id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id INT,
                timestamp DATETIME,
                action ENUM('enter', 'exit'),
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
            )
        """)
        print("Database and tables created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_db_and_tables()
