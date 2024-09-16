import os
import csv
import json
from datetime import datetime
import mysql.connector
from utils.db_utils import connect_to_database

ACCESS_FOLDER = 'accessed'


if not os.path.exists(ACCESS_FOLDER):
    os.makedirs(ACCESS_FOLDER)

def process_csv_file(gate_id):
    """Process the CSV file for type 1 gates."""
    filename = os.path.join(ACCESS_FOLDER, f'Gate_{gate_id}.csv')
    if not os.path.isfile(filename):
        return

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        logs = list(reader)

    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        for log in logs:
            cursor.execute("""
                INSERT INTO access_logs (employee_id, date, time, gate_id, direction)
                VALUES (%s, %s, %s, %s, %s)
                """, (log['employee_id'], log['date'], log['time'], gate_id, log['direction']))
        
        conn.commit()
        print(f"Processed {filename} successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def process_json_file(filename):
    """Process JSON files for type 2 gates."""
    with open(filename, 'r') as file:
        data = json.load(file)

    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO access_logs (employee_id, date, time, gate_id, direction)
            VALUES (%s, %s, %s, %s, %s)
            """, (data['employee_id'], data['date'], data['time'], data['gate_id'], data['direction']))
        
        conn.commit()
        print(f"Processed {filename} successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def generate_json(employee_id, gate_id, direction):
    """Generate a JSON file for type 2 gate access."""
    data = {
        'date': datetime.utcnow().isoformat(),
        'direction': direction,
        'employee_id': employee_id,
        'gate_id': gate_id
    }
    filename = os.path.join(ACCESS_FOLDER, f'Gate_{gate_id}.json')
    with open(filename, 'w') as file:
        json.dump(data, file)

def handle_gate_access():
    """Process all gate access files."""
    for gate_id in range(1, 7):
        if gate_id <= 4:
            process_csv_file(gate_id)
        else:
            filename = os.path.join(ACCESS_FOLDER, f'Gate_{gate_id}.json')
            if os.path.isfile(filename):
                process_json_file(filename)

if __name__ == "__main__":
    handle_gate_access()
