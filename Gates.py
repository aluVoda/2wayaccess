import mysql.connector
from datetime import datetime, timedelta
import random

# MySQL database configuration
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': '2wayaccess',
    'raise_on_warnings': True
}

# Simulated list of employees
employees = [i for i in range(1, 131)]  # Assuming 130 employees with IDs 1 to 130

# Simulated list of gate IDs (1 to 6)
gates = [1, 2, 3, 4, 5, 6]

# Function to log an entry/exit to the access_logs table
def log_access(employee_id, gate_id, action):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Get the current date and time separately
        current_datetime = datetime.now()
        current_date = current_datetime.date()  # Get current date
        current_time = current_datetime.time()  # Get current time

        # Insert the log into the access_logs table
        query = """
            INSERT INTO access_logs (employee_id, date, time, action, gate_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        data = (employee_id, current_date, current_time, action, gate_id)

        cursor.execute(query, data)
        conn.commit()

        print(f"Access log for Employee ID {employee_id} at Gate {gate_id} ({action}) logged successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to simulate gate activity
def simulate_gate_activity():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Simulate gate activity for 130 employees over 60 days
        for _ in range(60):
            for employee_id in range(1, 131):
                # Check if employee exists
                cursor.execute("SELECT employee_id FROM employees WHERE employee_id = %s", (employee_id,))
                if cursor.fetchone() is None:
                    print(f"Employee {employee_id} not found.")
                    continue  # Skip this employee if not found

                gate_id = random.randint(1, 6)
                action = random.choice(['enter', 'exit'])
                date = (datetime.now() - timedelta(days=random.randint(0, 60))).date()
                time = (datetime.now() - timedelta(hours=random.randint(0, 10))).time()

                query = """
                    INSERT INTO access_logs (employee_id, date, time, action, gate_id)
                    VALUES (%s, %s, %s, %s, %s)
                """
                data = (employee_id, date, time, action, gate_id)
                cursor.execute(query, data)

        conn.commit()
        print("Gate activity simulation complete.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    simulate_gate_activity(gates, employees)
