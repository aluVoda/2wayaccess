import mysql.connector
import random

# Sample data for the employees
first_names = ['John', 'Jane', 'Alice', 'Bob', 'Charlie', 'Geo', 'Florin', 'Cristi', 'Ion', 'Firicel', 'Dani', 'Miha', 'Maria', 'Ana']
last_names = ['Doe', 'Smith', 'Johnson', 'Brown', 'Taylor', 'Popescu', 'Ignat', 'Carutasu', 'Firea', 'Caras', 'Mihut', 'Silca']
companies = ['JusIT', 'ChiulSRL', 'HO.co']

# MySQL database configuration
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': '2wayaccess',
    'raise_on_warnings': True
}

def populate_employees():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Simulate 130 employees
        for i in range(1, 131):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            employment_status = 'fulltime' if i > 19 else 'parttime'  # 15% part-time, 85% full-time
            company = random.choice(companies)
            manager_id = None if employment_status == 'parttime' else random.randint(1, 130)  # Managers only for full-time employees

            # Insert the employee record into the database
            query = """
                INSERT INTO employees (firstname, lastname, employment_status, company, manager_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            data = (last_name, first_name, employment_status, company, manager_id)
            cursor.execute(query, data)

        conn.commit()
        print("Employees populated successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    populate_employees()
