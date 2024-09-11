import mysql.connector
from datetime import datetime
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
def simulate_gate_activity(gates, employees):
    actions = ['enter', 'exit']  # Possible actions
    for i in range(200):  # Simulate 200 random entries/exits
        employee_id = random.choice(employees)
        gate_id = random.choice(gates)
        action = random.choice(actions)

        # Log the simulated access
        log_access(employee_id, gate_id, action)

if __name__ == "__main__":
    simulate_gate_activity(gates, employees)
