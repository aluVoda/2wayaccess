import datetime
from abc import ABC, abstractmethod


class Employee(ABC):
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self._logs = []

    @abstractmethod
    def log_access(self, timestamp, action):
        pass

    @abstractmethod
    def calculate_working_hours(self, date=None):
        pass

    @abstractmethod
    def get_report(self, date=None):
        pass

class FullTimeEmployee(Employee):
    def log_access(self, timestamp, action):
        """Log the access for a full-time employee"""
        self._logs.append((timestamp, action))
        print(f"Full-time Employee {self.employee_id} {action} at {timestamp}")

    def calculate_working_hours(self, date=None):
        """Calculate total working hours for the employee"""
        total_work_time = datetime.timedelta()
        entry_time = None

        for log_time, action in self._logs:
            if date and log_time.date() != date:
                continue
            if action == 'enter':
                entry_time = log_time
            elif action == 'exit' and entry_time:
                total_work_time += log_time - entry_time
                entry_time = None

        return total_work_time

    def get_report(self, date=None):
        total_work_time = self.calculate_working_hours(date)
        if date:
            print(f"Total working hours for Full-time Employee {self.employee_id} on {date}: {total_work_time}")
        else:
            print(f"Total working hours for Full-time Employee {self.employee_id}: {total_work_time}")
        return total_work_time

class PartTimeEmployee(Employee):
    def log_access(self, timestamp, action):
        """Log the access for a part-time employee"""
        self._logs.append((timestamp, action))
        print(f"Part-time Employee {self.employee_id} {action} at {timestamp}")

    def calculate_working_hours(self, date=None):
        total_work_time = datetime.timedelta()
        entry_time = None

        for log_time, action in self._logs:
            if date and log_time.date() != date:
                continue
            if action == 'enter':
                entry_time = log_time
            elif action == 'exit' and entry_time:
                total_work_time += log_time - entry_time
                entry_time = None

        return total_work_time

    def get_report(self, date=None):
        total_work_time = self.calculate_working_hours(date)
        if date:
            print(f"Total working hours for Part-time Employee {self.employee_id} on {date}: {total_work_time}")
        else:
            print(f"Total working hours for Part-time Employee {self.employee_id}: {total_work_time}")
        return total_work_time
