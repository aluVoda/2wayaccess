import mysql.connector

def create_database_and_table():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host="localhost",  
            user="root",       
            password="root",
            database="2wayaccess" 
        )
        cursor = conn.cursor()

        # Create the database
        cursor.execute("CREATE DATABASE IF NOT EXISTS 2wayaccess")
        print("Database '2wayaccess' created or already exists.")
        

        # Create the access_logs table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS access_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id INT NOT NULL,
            timestamp DATETIME NOT NULL,
            action ENUM('enter', 'exit') NOT NULL
        );
        """
        cursor.execute(create_table_query)

        # Create the employees table for employment status
        create_employees_table = """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INT PRIMARY KEY,
            employment_status ENUM('full_time', 'part_time') NOT NULL
        );
        """
        cursor.execute(create_employees_table)

        print("Tables 'access_logs' and 'employees'created or already exists.")
        
        # Commit changes
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        # Close the connection
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed.")

# Run the setup
if __name__ == "__main__":
    create_database_and_table()
