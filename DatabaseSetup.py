import mysql.connector
from mysql.connector import errorcode

# Database connection configuration
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'raise_on_warnings': True
}

# Function to create database
def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS 2wayaccess DEFAULT CHARACTER SET 'UTF8MB4'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

# Function to create tables
def create_tables(cursor):
    # Switch to the 2wayaccess database
    cursor.execute("USE 2wayaccess")

    # Create employees table
    create_employees_table = """
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        employment_status ENUM('fulltime', 'parttime') NOT NULL
    )
    """
    
    # Create access_logs table with gate_id
    create_access_logs_table = """
    CREATE TABLE IF NOT EXISTS access_logs (
        log_id INT AUTO_INCREMENT PRIMARY KEY,
        employee_id INT NOT NULL,
        timestamp DATETIME NOT NULL,
        action ENUM('enter', 'exit') NOT NULL,
        gate_id INT NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    )
    """
    
    try:
        cursor.execute(create_employees_table)
        cursor.execute(create_access_logs_table)
        print("Tables created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed creating tables: {err}")

# Main function to set up the database
def main():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Create database if not exists
        create_database(cursor)
        
        # Create necessary tables
        create_tables(cursor)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)
    else:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
