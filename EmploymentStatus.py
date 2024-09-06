import mysql.connector
import random

def assign_employment_status():
    try:
    # Connect to MySQL server
        conn = mysql.connector.connect(
            host="localhost",  
            user="root",       
            password="root",
            database="2wayaccess" 
        )
        cursor = conn.cursor()

        # Number of employees
        total_employees = 130
        part_time_count = int(total_employees * 0.15)  # 15% part-time
        full_time_count = total_employees - part_time_count

        # Create a list of employee statuses
        employee_statuses = ['part_time'] * part_time_count + ['full_time'] * full_time_count

        # Shuffle the list to randomize the assignment of statuses
        random.shuffle(employee_statuses)

        # Insert employees and their statuses into the employees table
        for employee_id in range(1, total_employees + 1):
            employment_status = employee_statuses[employee_id - 1]
            cursor.execute(
                "INSERT INTO employees (employee_id, employment_status) VALUES (%s, %s)",
                (employee_id, employment_status)
            )

        # Commit the changes
        conn.commit()

        print(f"Employment statuses for {total_employees} employees inserted successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the connection
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed.")

# Run the employment status assignment
if __name__ == "__main__":
    assign_employment_status()
