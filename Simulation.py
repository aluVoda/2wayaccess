from EmployeeMonitor import EmployeeMonitor
from Employees import FullTimeEmployee, PartTimeEmployee
from Functions import log_access_to_db, get_employee_status
import random
import datetime

def generate_random_time(base_time):
    """Generates a random datetime for entering or exiting"""
    random_minutes = random.randint(0, 60 * 9)  # Workday can start anytime between 9 hours span
    return base_time + datetime.timedelta(minutes=random_minutes)

def generate_random_access_logs(monitor, num_employees=130):
    """Generates random access logs for employees based on their employment status"""
    # Current day and base entry time for random time generation
    base_date = datetime.datetime(2024, 9, 5, 8, 0, 0)  # Base date (e.g. 8:00 AM)

    for employee_id in range(1, num_employees + 1):
        # Fetch employment status from the database
        employment_status = get_employee_status(employee_id)

        # Create the appropriate employee object based on status
        if employment_status == 'full_time':
            employee = FullTimeEmployee(employee_id)
        elif employment_status == 'part_time':
            employee = PartTimeEmployee(employee_id)
        else:
            print(f"Error: Employee {employee_id} does not have a valid employment status.")
            continue

        monitor.add_employee(employee)

        # Generate random entry time
        entry_time = generate_random_time(base_date)
        
        # Log the entry time
        monitor.log_access(employee_id, entry_time, 'enter')

        # Generate random exit time after entry (ensuring the employee leaves after entering)
        exit_time = entry_time + datetime.timedelta(hours=random.randint(4, 9))  # Work between 4 to 9 hours
        
        # Log the exit time
        monitor.log_access(employee_id, exit_time, 'exit')

    print(f"Random access logs generated for {num_employees} employees.")

def run_simulation():
    # Create the employee monitor
    monitor = EmployeeMonitor()

    # Generate random access logs for 130 employees
    generate_random_access_logs(monitor, 130)


  
  
  

  
  

  
  
  
  
  

  
  

  
  
  
