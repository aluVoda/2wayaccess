import random
import mysql.connector
from utils.db_utils import connect_to_database

# Employee and Company settings
COMPANIES = [
    {"name": "JusIT", "domain": "IT", "size": 40},
    {"name": "ChiulSRL", "domain": "HR", "size": 30},
    {"name": "HO.ro", "domain": "IT", "size": 35},
    {"name": "Leugreu", "domain": "Finance", "size": 25}
]

PART_TIME_RATIO = 0.17  # 17% of employees should be part-time

DEPARTMENTS = {
    "IT": ["Software", "Infrastructure", "QA"],
    "HR": ["Recruitment", "Employee Relations"],
    "Finance": ["Accounting", "Audit", "Compliance"]
}

FIRST_NAMES = ["John", "Jane", "Alex", "Emily", "Michael", "Sarah", "David", "Sophia", "Daniel", "Olivia", 'Geo', 'Florin', 'Cristi', 'Ion', 'Firicel', 'Dani', 'Miha', 'Maria', 'Ana']
LAST_NAMES = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", 'Popescu', 'Ignat', 'Carutasu', 'Firea', 'Caras', 'Mihut', 'Silca']

def populate_companies(cursor):
    """Populates the Companies table."""
    for company in COMPANIES:
        cursor.execute("""
            INSERT INTO companies (name, domain, size)
            VALUES (%s, %s, %s) AS new_company
            ON DUPLICATE KEY UPDATE domain = new_company.domain, size = new_company.size
        """, (company['name'], company['domain'], company['size']))
    print("Companies table populated.")

def generate_managers(cursor, company_name, domain, employee_count):
    """Generates and populates managers for each company and department."""
    managers = []
    department_list = DEPARTMENTS[domain]
    
    # Distribute employees across departments and assign managers (max 10 employees per manager)
    employees_per_department = employee_count // len(department_list)
    
    for department in department_list:
        department_employees = employees_per_department
        remaining_employees = employee_count % len(department_list)
        if remaining_employees > 0:
            department_employees += 1

        num_managers = max(1, (department_employees // 10) + (department_employees % 10 > 0))
        
        for _ in range(num_managers):
            firstname = random.choice(FIRST_NAMES)
            lastname = random.choice(LAST_NAMES)
            cursor.execute("""
                INSERT INTO managers (firstname, lastname, department, company)
                VALUES (%s, %s, %s, %s) AS new_manager
            """, (firstname, lastname, department, company_name))
            managers.append(cursor.lastrowid)  
    return managers

def populate_employees(cursor):
    """Populates the Employees table with random full-time and part-time employees."""
    total_employees = 130
    part_time_count = int(total_employees * PART_TIME_RATIO)
    full_time_count = total_employees - part_time_count

    for company in COMPANIES:
        company_name = company["name"]
        domain = company["domain"]
        employee_count = company["size"]
        
        # Generate managers for the company
        managers = generate_managers(cursor, company_name, domain, employee_count)

        # Distribute employees across full-time and part-time
        for _ in range(employee_count):
            firstname = random.choice(FIRST_NAMES)
            lastname = random.choice(LAST_NAMES)
            employment_status = "parttime" if part_time_count > 0 else "fulltime"

            # Assign a random manager from the company's managers
            manager_id = random.choice(managers)

            cursor.execute("""
                INSERT INTO employees (firstname, lastname, employment_status, company, manager_id)
                VALUES (%s, %s, %s, %s, %s) AS new_employee
                ON DUPLICATE KEY UPDATE employment_status = new_employee.employment_status, company = new_employee.company, manager_id = new_employee.manager_id
            """, (firstname, lastname, employment_status, company_name, manager_id))

            if employment_status == "parttime":
                part_time_count -= 1
            else:
                full_time_count -= 1
    print("Employees table populated.")

def populate_data():
    """Populates all required tables with initial data."""
    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Populate Companies and Managers
        populate_companies(cursor)
        populate_employees(cursor)

        conn.commit()
        print("Database populated successfully.")
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
    populate_data()
