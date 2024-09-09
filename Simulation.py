import mysql.connector
from datetime import datetime, timedelta
import random

def simulate_access_logs():
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="2wayaccess"
    )
    cursor = conn.cursor()

    # Fetch all employees along with their employment status
    cursor.execute("SELECT employee_id, employment_status FROM employees")
    employees = cursor.fetchall()

    # Set the time window for simulation (60 days)
    today = datetime.now().date()
    start_date = today - timedelta(days=60)

    for emp in employees:
        emp_id = emp[0]
        employment_status = emp[1]  # 'full-time' or 'part-time'

        # Simulate for each day in the last 60 days
        for day in range(60):
            current_day = start_date + timedelta(days=day)

            # Determine the number of work days for part-time employees
            if employment_status == 'part-time':
                # Part-time employees work only 3-4 days a week
                if random.random() > 0.5:  # 50% chance they work on a given day
                    continue  # Skip this day if they don't work

            # Simulate random enter/exit actions
            num_entries = random.randint(1, 2)  # Employees enter/exit once or twice per day
            for _ in range(num_entries):
                # Randomize entry time depending on full-time or part-time status
                if employment_status == 'full-time':
                    entry_time = datetime.combine(current_day, datetime.min.time()) + timedelta(hours=random.randint(6, 10))
                    work_hours = random.uniform(7, 9)  # Full-time employees work 7-9 hours
                else:  # part-time
                    entry_time = datetime.combine(current_day, datetime.min.time()) + timedelta(hours=random.randint(8, 12))
                    work_hours = random.uniform(4, 6)  # Part-time employees work 4-6 hours

                cursor.execute("INSERT INTO access_logs (employee_id, timestamp, action) VALUES (%s, %s, %s)",
                               (emp_id, entry_time, 'enter'))

                # Exit time depends on how many hours they worked
                exit_time = entry_time + timedelta(hours=work_hours)
                cursor.execute("INSERT INTO access_logs (employee_id, timestamp, action) VALUES (%s, %s, %s)",
                               (emp_id, exit_time, 'exit'))

    # Commit the data to the database
    conn.commit()
    cursor.close()
    conn.close()
    print("Simulation data for 60 days has been added, with part-time and full-time employee logic.")

if __name__ == "__main__":
    simulate_access_logs()
