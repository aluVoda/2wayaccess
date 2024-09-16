import mysql.connector
from mysql.connector import errorcode
from utils.db_utils import connect_to_database

def database_exists(cursor, db_name):
    """Check if the database exists."""
    cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
    return cursor.fetchone() is not None

def create_database(cursor, db_name):
    """Create the database if it does not exist."""
    if not database_exists(cursor, db_name):
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created.")
    else:
        print(f"Database '{db_name}' already exists.")

def check_and_update_table(cursor, table_name, create_sql, expected_columns):
    """Check if table exists and either create or update it."""
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()

    if result:
        print(f"Table '{table_name}' exists. Checking for differences...")

        # Get the current table structure
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        current_columns = {column[0]: column[1] for column in cursor.fetchall()}

        # Compare the expected columns with the current ones
        for column_name, column_type in expected_columns.items():
            if column_name not in current_columns:
                print(f"Adding missing column '{column_name}' to '{table_name}'")
                cursor.execute(f"ALTER TABLE {table_name} ADD {column_name} {column_type}")
            elif current_columns[column_name] != column_type:
                print(f"Updating column '{column_name}' in '{table_name}'")
                cursor.execute(f"ALTER TABLE {table_name} MODIFY {column_name} {column_type}")
    else:
        print(f"Table '{table_name}' does not exist. Creating the table.")
        cursor.execute(create_sql)

def create_or_update_tables(cursor):
    """Create or update tables."""
    # Companies table
    companies_table = """
        CREATE TABLE IF NOT EXISTS companies (
            name VARCHAR(255) PRIMARY KEY,
            domain VARCHAR(255),
            size INT
        )
    """
    companies_columns = {
        'name': 'VARCHAR(255)',
        'domain': 'VARCHAR(255)',
        'size': 'INT'
    }
    check_and_update_table(cursor, 'companies', companies_table, companies_columns)

    # Managers table
    managers_table = """
        CREATE TABLE IF NOT EXISTS managers (
            manager_id INT AUTO_INCREMENT PRIMARY KEY,
            firstname VARCHAR(255),
            lastname VARCHAR(255),
            department VARCHAR(255),
            company VARCHAR(255),
            email VARCHAR(255),
            FOREIGN KEY (company) REFERENCES companies(name) ON DELETE CASCADE
        )
    """
    managers_columns = {
        'manager_id': 'INT AUTO_INCREMENT PRIMARY KEY',
        'firstname': 'VARCHAR(255)',
        'lastname': 'VARCHAR(255)',
        'department': 'VARCHAR(255)',
        'company': 'VARCHAR(255)',
        'email': 'VARCHAR(255)'
    }
    check_and_update_table(cursor, 'managers', managers_table, managers_columns)

    # Employees table
    employees_table = """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INT AUTO_INCREMENT PRIMARY KEY,
            firstname VARCHAR(255),
            lastname VARCHAR(255),
            employment_status ENUM('fulltime', 'parttime'),
            company VARCHAR(255),
            manager_id INT,
            FOREIGN KEY (company) REFERENCES companies(name) ON DELETE CASCADE,
            FOREIGN KEY (manager_id) REFERENCES managers(manager_id) ON DELETE SET NULL
        )
    """
    employees_columns = {
        'employee_id': 'INT AUTO_INCREMENT PRIMARY KEY',
        'firstname': 'VARCHAR(255)',
        'lastname': 'VARCHAR(255)',
        'employment_status': "ENUM('fulltime', 'parttime')",
        'company': 'VARCHAR(255)',
        'manager_id': 'INT'
    }
    check_and_update_table(cursor, 'employees', employees_table, employees_columns)

    # Access Logs table
    access_logs_table = """
        CREATE TABLE IF NOT EXISTS access_logs (
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id INT,
            date DATE,
            time TIME,
            gate_id INT,
            direction ENUM('in', 'out'),
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
        )
    """
    access_logs_columns = {
        'log_id': 'INT AUTO_INCREMENT PRIMARY KEY',
        'employee_id': 'INT',
        'date': 'DATE',
        'time': 'TIME',
        'gate_id': 'INT',
        'direction': "ENUM('in', 'out')"
    }
    check_and_update_table(cursor, 'access_logs', access_logs_table, access_logs_columns)

def setup_database():
    """Main function to setup the database and tables."""
    conn = None
    cursor = None
    try:
        # Connect to MySQL server without specifying the database
        conn = mysql.connector.connect(
            host='localhost',       
            user='root',   
            password='root' 
        )
        if conn is None:
            raise ValueError("Failed to connect to the database server.")

        cursor = conn.cursor()

        # Create the database if it doesn't exist
        create_database(cursor, '2wayaccess')
        
        # Switch to the new database
        cursor.execute("USE 2wayaccess")

        # Create or update the necessary tables
        create_or_update_tables(cursor)

        conn.commit()
        print("Database setup completed.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if conn:
            conn.rollback()
    except ValueError as ve:
        print(ve)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()
