from EmployeeMonitor import EmployeeMonitor
from Employees import FullTimeEmployee, PartTimeEmployee
import datetime

def run_simulation():
    # Create employee monitor
    monitor = EmployeeMonitor()

    # Add employees (Full-time and Part-time)
    emp1 = FullTimeEmployee(101)
    emp2 = PartTimeEmployee(102)

    monitor.add_employee(emp1)
    monitor.add_employee(emp2)

    # Simulate access logs
    monitor.log_access(101, datetime.datetime(2024, 9, 5, 9, 0, 0), 'enter')
    monitor.log_access(101, datetime.datetime(2024, 9, 5, 12, 0, 0), 'exit')
    monitor.log_access(101, datetime.datetime(2024, 9, 5, 13, 0, 0), 'enter')
    monitor.log_access(101, datetime.datetime(2024, 9, 5, 17, 0, 0), 'exit')

    monitor.log_access(102, datetime.datetime(2024, 9, 5, 10, 0, 0), 'enter')
    monitor.log_access(102, datetime.datetime(2024, 9, 5, 14, 0, 0), 'exit')

    # Generate reports
    monitor.get_employee_report(101, datetime.date(2024, 9, 5))
    monitor.get_employee_report(102, datetime.date(2024, 9, 5))
