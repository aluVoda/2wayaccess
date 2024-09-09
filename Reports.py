import mysql.connector
from datetime import datetime, timedelta
import schedule
import time
from datetime import datetime

# Function to calculate total working hours between 'enter' and 'exit' actions
def calculate_working_hours(employee_id, start_date, end_date):
    conn = None
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  
            database="2wayaccess"
        )
        cursor = conn.cursor(dictionary=True)

        # Query to fetch all logs for the employee within the specified date range
        query = """
        SELECT timestamp, action FROM access_logs
        WHERE employee_id = %s AND timestamp BETWEEN %s AND %s
        ORDER BY timestamp ASC
        """
        cursor.execute(query, (employee_id, start_date, end_date))
        logs = cursor.fetchall()

        # Calculate total working hours
        total_hours = timedelta()  # total_hours as a timedelta object
        last_entry = None

        for log in logs:
            if log['action'] == 'enter':
                last_entry = log['timestamp']
            elif log['action'] == 'exit' and last_entry:
                # Calculate difference between exit and entry
                total_hours += (log['timestamp'] - last_entry)
                last_entry = None

        return total_hours.total_seconds() / 3600  # Convert seconds to hours

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return 0

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# Generate report for today's working hours
def generate_daily_report():
    today = datetime.now().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    return generate_report(start_of_day, end_of_day, "Daily")


# Generate weekly report (previous 7 days including today)
def generate_weekly_report():
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    start_of_week = datetime.combine(start_of_week, datetime.min.time())
    end_of_week = datetime.combine(today, datetime.max.time())  # Today

    return generate_report(start_of_week, end_of_week, "Weekly")


# Generate monthly report (previous calendar month)
def generate_monthly_report():
    today = datetime.now().date()
    first_day_of_month = today.replace(day=1)
    previous_month_last_day = first_day_of_month - timedelta(days=1)
    start_of_previous_month = datetime.combine(previous_month_last_day.replace(day=1), datetime.min.time())
    end_of_previous_month = datetime.combine(previous_month_last_day, datetime.max.time())

    return generate_report(start_of_previous_month, end_of_previous_month, "Monthly")


# Main report generation function
def generate_report(start_date, end_date, report_type):
    conn = None
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  
            database="2wayaccess"
        )
        cursor = conn.cursor(dictionary=True)

        # Get all employee IDs
        cursor.execute("SELECT employee_id FROM employees")
        employees = cursor.fetchall()

        print(f"\n--- {report_type} Report ---\n")
        print(f"Report Period: {start_date} to {end_date}\n")

        # Generate working hours for each employee
        for employee in employees:
            employee_id = employee['employee_id']
            total_hours = calculate_working_hours(employee_id, start_date, end_date)
            print(f"Employee {employee_id}: {total_hours:.2f} hours")

        print(f"\n--- End of {report_type} Report ---\n")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Example usage to test functions
if __name__ == "__main__":
    generate_daily_report()
    generate_weekly_report()
    generate_monthly_report()

def run_daily():
    generate_daily_report()

def run_weekly():
    # Only run if today is Sunday
    if datetime.now().weekday() == 6:
        generate_weekly_report()

def run_monthly():
    # Only run if today is the 3rd
    if datetime.now().day == 3:
        generate_monthly_report()

# Scheduling daily, weekly, and monthly reports
schedule.every().day.at("23:00").do(run_daily)
schedule.every().sunday.at("23:00").do(run_weekly)
schedule.every().month.at("23:00").do(run_monthly)

while True:
    schedule.run_pending()
    time.sleep(60)  # Wait one minute before checking again