import mysql.connector
import random

def populate_employees():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="2wayaccess"
    )
    cursor = conn.cursor()

    total_employees = 130
    part_time_percentage = 0.15
    part_time_count = int(total_employees * part_time_percentage)

    # Add employees
    for i in range(total_employees):
        name = f"Employee_{i + 1}"
        employment_status = 'part-time' if i < part_time_count else 'full-time'
        cursor.execute("INSERT INTO employees (name, employment_status) VALUES (%s, %s)", (name, employment_status))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    populate_employees()
