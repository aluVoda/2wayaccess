from Functions import log_access_to_db, get_employee_logs
from Employees import FullTimeEmployee, PartTimeEmployee

class EmployeeMonitor:
    def __init__(self):
        # Dictionary to store employee objects by employee_id
        self.employees = {}

    def add_employee(self, employee):
        """Add a new employee (Full-time or Part-time)"""
        self.employees[employee.employee_id] = employee

    def log_access(self, employee_id, timestamp, action):
        """Log an access event for the specified employee"""
        if employee_id in self.employees:
            employee = self.employees[employee_id]
            employee.log_access(timestamp, action)
            log_access_to_db(employee_id, timestamp, action)
        else:
            print(f"Employee {employee_id} not found!")

    def get_employee_report(self, employee_id, date=None):
        """Generate a report for the specified employee"""
        if employee_id in self.employees:
            return self.employees[employee_id].get_report(date)
        else:
            print(f"Employee {employee_id} not found!")
