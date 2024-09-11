import schedule
import time
from datetime import datetime, timedelta
from utils.db_utils import get_db_connection, close_db_connection

def calculate_working_hours(employee_id, start_date, end_date):
    conn = get_db_connection()
    if not conn:
        return 0

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT timestamp, action FROM access_logs
        WHERE employee_id = %s AND timestamp BETWEEN %s AND %s
        ORDER BY timestamp ASC
        """
        cursor.execute(query, (employee_id, start_date, end_date))
        logs = cursor.fetchall()

        total_hours = timedelta()
        last_entry = None

        for log in logs:
            if log['action'] == 'enter':
                last_entry = log['timestamp']
            elif log['action'] == 'exit' and last_entry:
                total_hours += (log['timestamp'] - last_entry)
                last_entry = None

        return total_hours.total_seconds() / 3600  # Convert to hours

    except Exception as e:
        print(f"Error calculating working hours for employee {employee_id}: {e}")
        return 0

    finally:
        close_db_connection(conn, cursor)

def generate_report(start_date, end_date, report_type):
    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT employee_id FROM employees")
        employees = cursor.fetchall()

        print(f"\n--- {report_type} Report ---")
        print(f"Report Period: {start_date} to {end_date}\n")

        for employee in employees:
            employee_id = employee['employee_id']
            total_hours = calculate_working_hours(employee_id, start_date, end_date)
            # Fetch gate usage for the employee
            cursor.execute("""
                SELECT gate_id, COUNT(*) as access_count
                FROM access_logs
                WHERE employee_id = %s AND timestamp BETWEEN %s AND %s
                GROUP BY gate_id
            """, (employee_id, start_date, end_date))
            gate_usage = cursor.fetchall()

            print(f"Employee {employee_id}: {total_hours:.2f} hours")
            for gate in gate_usage:
                print(f"  Gate {gate['gate_id']}: {gate['access_count']} accesses")

        print(f"\n--- End of {report_type} Report ---\n")

    except Exception as e:
        print(f"Error generating report: {e}")

    finally:
        close_db_connection(conn, cursor)

def generate_daily_report():
    today = datetime.now().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    generate_report(start_of_day, end_of_day, "Daily")

def generate_weekly_report():
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = datetime.combine(start_of_week, datetime.min.time())
    end_of_week = datetime.combine(today, datetime.max.time())
    generate_report(start_of_week, end_of_week, "Weekly")

def generate_monthly_report():
    today = datetime.now().date()
    first_day_of_month = today.replace(day=1)
    previous_month_last_day = first_day_of_month - timedelta(days=1)
    start_of_previous_month = datetime.combine(previous_month_last_day.replace(day=1), datetime.min.time())
    end_of_previous_month = datetime.combine(previous_month_last_day, datetime.max.time())
    generate_report(start_of_previous_month, end_of_previous_month, "Monthly")

def schedule_reports():
    # Schedule daily report at 23:00
    schedule.every().day.at("23:00").do(generate_daily_report)
    
    # Schedule weekly report every Sunday at 23:00
    schedule.every().sunday.at("23:00").do(generate_weekly_report)
    
    # Schedule monthly report by running a daily check at 23:00, and generate the report only on the 3rd of the month
    schedule.every().day.at("23:00").do(check_monthly_report)

    print("Report scheduling initiated...")

    while True:
        schedule.run_pending()
        time.sleep(60)

def check_monthly_report():
    today = datetime.now().date()
    if today.day == 3:  # Only generate the monthly report on the 3rd of the month
        generate_monthly_report()

if __name__ == "__main__":
    schedule_reports()
