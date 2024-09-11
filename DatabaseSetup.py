import mysql.connector

# Database configuration
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'raise_on_warnings': True
}

database_name = '2wayaccess'


def create_or_update_database():
    conn = None
    cursor = None
    try:
        # Connect to MySQL without specifying the database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
        database_exists = cursor.fetchone()

        if not database_exists:
            # If the database doesn't exist, create it
            cursor.execute(f"CREATE DATABASE {database_name}")
            conn.commit()
            print(f"Database '{database_name}' created.")
        else:
            print(f"Database '{database_name}' already exists.")

        # Switch to the '2wayaccess' database
        conn.database = database_name

        # Ensure tables exist with correct schema
        check_and_update_schema(cursor)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def check_and_update_schema(cursor):
    # Check if employees table exists
    cursor.execute("""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = %s 
        AND TABLE_NAME = 'employees';
    """, (database_name,))
    
    table_exists = cursor.fetchone()[0]

    if table_exists == 0:
        # Create employees table
        create_employees_table(cursor)
    else:
        # Check if employees table matches the expected schema
        check_and_update_employees_table(cursor)

    # Check if access_logs table exists
    cursor.execute("""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = %s 
        AND TABLE_NAME = 'access_logs';
    """, (database_name,))
    
    table_exists = cursor.fetchone()[0]

    if table_exists == 0:
        # Create access_logs table
        create_access_logs_table(cursor)
    else:
        # Check if access_logs table matches the expected schema
        check_and_update_access_logs_table(cursor)


def create_employees_table(cursor):
    cursor.execute("""
        CREATE TABLE employees (
            employee_id INT AUTO_INCREMENT PRIMARY KEY,
            firstname VARCHAR(255),
            lastname VARCHAR(255),
            employment_status ENUM('fulltime', 'parttime'),
            company VARCHAR(255),
            manager_id INT
        );
    """)
    print("Created 'employees' table.")


def check_and_update_employees_table(cursor):
    # Check if columns match the expected schema for 'employees'
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'employees';
    """, (database_name,))
    
    columns = {row[0] for row in cursor.fetchall()}
    expected_columns = {'employee_id', 'firstname', 'lastname', 'employment_status', 'company', 'manager_id'}
    
    missing_columns = expected_columns - columns
    extra_columns = columns - expected_columns

    if missing_columns:
        for column in missing_columns:
            # Add missing columns based on their type
            if column == 'firstname':
                cursor.execute("ALTER TABLE employees ADD COLUMN firstname VARCHAR(255);")
            elif column == 'lastname':
                cursor.execute("ALTER TABLE employees ADD COLUMN lastname VARCHAR(255);")
            elif column == 'employment_status':
                cursor.execute("ALTER TABLE employees ADD COLUMN employment_status ENUM('fulltime', 'parttime');")
            elif column == 'company':
                cursor.execute("ALTER TABLE employees ADD COLUMN company VARCHAR(255);")
            elif column == 'manager_id':
                cursor.execute("ALTER TABLE employees ADD COLUMN manager_id INT;")
            print(f"Added missing column: {column}.")

    if extra_columns:
        print(f"Extra columns found in 'employees' table: {extra_columns}. Please review manually.")


def create_access_logs_table(cursor):
    cursor.execute("""
        CREATE TABLE access_logs (
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id INT,
            date DATE,
            time TIME,
            action ENUM('enter', 'exit'),
            gate_id INT,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        );
    """)
    print("Created 'access_logs' table.")


def check_and_update_access_logs_table(cursor):
    # Check if columns match the expected schema for 'access_logs'
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'access_logs';
    """, (database_name,))
    
    columns = {row[0] for row in cursor.fetchall()}
    expected_columns = {'log_id', 'employee_id', 'date', 'time', 'action', 'gate_id'}
    
    missing_columns = expected_columns - columns
    extra_columns = columns - expected_columns

    if missing_columns:
        for column in missing_columns:
            # Add missing columns based on their type
            if column == 'date':
                cursor.execute("ALTER TABLE access_logs ADD COLUMN date DATE;")
            elif column == 'time':
                cursor.execute("ALTER TABLE access_logs ADD COLUMN time TIME;")
            elif column == 'action':
                cursor.execute("ALTER TABLE access_logs ADD COLUMN action ENUM('enter', 'exit');")
            elif column == 'gate_id':
                cursor.execute("ALTER TABLE access_logs ADD COLUMN gate_id INT;")
            print(f"Added missing column: {column}.")

    if extra_columns:
        print(f"Extra columns found in 'access_logs' table: {extra_columns}. Please review manually.")


if __name__ == "__main__":
    create_or_update_database()
