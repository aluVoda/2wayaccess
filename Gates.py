import mysql.connector
from datetime import datetime
import random

class Gate:
    def __init__(self, gate_id):
        self.gate_id = gate_id  # Unique ID for each gate (1 to 6)

    def log_access(self, employee_id, action):
        """
        Logs the access event to the database with employee_id, timestamp, gate_id, and action (enter/exit).
        """
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="2wayaccess"
        )
        cursor = conn.cursor()

        try:
            # Get the current timestamp
            timestamp = datetime.now()

            # Insert the access log into the database, including the gate_id used for access
            query = """
            INSERT INTO access_logs (employee_id, timestamp, action, gate_id)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (employee_id, timestamp, action, self.gate_id))
            conn.commit()

            print(f"Employee {employee_id} {action}ed at Gate {self.gate_id} at {timestamp}.")

        except mysql.connector.Error as err:
            print(f"Error logging access: {err}")
        finally:
            cursor.close()
            conn.close()

    def validate_card(self, employee_id, action):
        """
        Simulate card validation and log access if the employee has a valid card.
        """
        # Here we assume the card is always valid for the sake of simulation
        self.log_access(employee_id, action)

def simulate_gate_activity(gates, employees):
    """
    Simulates activity at the gates. Randomly picks employees and actions for the simulation.
    """
    for _ in range(100):  # Simulate 100 random accesses
        # Randomly pick an employee, a gate, and whether they are entering or exiting
        employee_id = random.choice(employees)
        gate = random.choice(gates)
        action = random.choice(['enter', 'exit'])

        gate.validate_card(employee_id, action)

if __name__ == "__main__":
    # Create 6 gate objects
    gates = [Gate(gate_id) for gate_id in range(1, 7)]

    # Fetch all employee IDs from the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="2wayaccess"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT employee_id FROM employees")
    employees = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    # Simulate random gate activity
    simulate_gate_activity(gates, employees)
