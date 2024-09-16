import random
from datetime import datetime, timedelta
import mysql.connector
from utils.db_utils import connect_to_database

# Constants
NUM_GATES = 6  # Total number of gates

def generate_random_time(start_time, work_duration):
    """Generate a random time of day within the work duration."""
    start_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = start_datetime + timedelta(hours=work_duration)
    random_time = start_datetime + timedelta(seconds=random.randint(0, int((end_datetime - start_datetime).total_seconds())))
    return random_time.time()

def generate_access_logs_for_employee(employee_id, employment_status, num_days=30):
    """Generate access logs for a single employee for the last num_days days."""
    logs = []
    today = datetime.today()
    
    # Set work hours based on employment status
    if employment_status == "fulltime":
        work_hours = (7, 9)  # Full-time work hours range (in hours)
    else:
        work_hours = (4, 6)  # Part-time work hours range (in hours)
    
    for i in range(num_days):
        day = today - timedelta(days=i)
        date_str = day.strftime('%Y-%m-%d')
        
        work_duration = random.randint(*work_hours)
        
        # Generate entry and exit times
        entry_time = generate_random_time(datetime.min.time(), work_duration)
        exit_time = generate_random_time(entry_time, work_duration)
        
        # Generate random gate ID
        gate_id = random.randint(1, NUM_GATES)
        
        # Entry log
        logs.append((employee_id, date_str, entry_time, gate_id, 'in'))
        
        # Exit log
        logs.append((employee_id, date_str, exit_time, gate_id, 'out'))
    
    return logs

def populate_access_logs():
    """Populates the access_logs table with random access data for each employee."""
    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        
        # Fetch all employee data (ID and employment status)
        cursor.execute("SELECT employee_id, employment_status FROM employees")
        employees = cursor.fetchall()
        
        # Generate and insert access logs for each employee
        for employee_id, employment_status in employees:
            logs = generate_access_logs_for_employee(employee_id, employment_status)
            cursor.executemany("""
                INSERT INTO access_logs (employee_id, date, time, gate_id, direction)
                VALUES (%s, %s, %s, %s, %s)
            """, logs)
        
        conn.commit()
        print("Access logs table populated successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    populate_access_logs()
