import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
import mysql.connector
from utils.db_utils import connect_to_database

# Constants
BACKUP_FOLDER = 'Backup'
EMAIL_SENDER = 'florentin.voda@gmail.com'  # Replace with your email
EMAIL_PASSWORD = 'wckwwmxkilldxjls'  # Replace with your email password
SMTP_SERVER = 'smtp.gmail.com'  # Replace with your SMTP server
SMTP_PORT = 587  # Replace with your SMTP port

def ensure_backup_folder():
    """Ensure the backup folder exists."""
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

def fetch_working_hours(start_date, end_date):
    """Fetch working hours between start_date and end_date."""
    query = """
        SELECT e.firstname, e.lastname, DATE(a.date) AS date, 
               SUM(TIME_TO_SEC(TIMEDIFF(a.exit_time, a.entry_time)) / 3600) AS working_hours
        FROM (
            SELECT employee_id, date, 
                   MIN(CASE WHEN direction = 'in' THEN time END) AS entry_time,
                   MAX(CASE WHEN direction = 'out' THEN time END) AS exit_time
            FROM access_logs
            WHERE date BETWEEN %s AND %s
            GROUP BY employee_id, date
        ) AS a
        JOIN employees AS e ON a.employee_id = e.employee_id
        GROUP BY e.firstname, e.lastname, DATE(a.date)
    """
    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (start_date, end_date))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_managers_emails():
    """Fetch email addresses of all managers."""
    query = """
        SELECT DISTINCT m.email
        FROM managers AS m
        JOIN employees AS e ON m.manager_id = e.manager_id
    """
    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        return [row['email'] for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def generate_report_filename(report_type):
    """Generate a report filename based on the current date."""
    current_date = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(BACKUP_FOLDER, f"{current_date}_{report_type}")

def save_report(data, filename):
    """Save the report data to both CSV and TXT formats."""
    csv_filename = f"{filename}.csv"
    txt_filename = f"{filename}.txt"
    
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Firstname', 'Lastname', 'Date', 'WorkingHours'])
        for row in data:
            writer.writerow([row['firstname'], row['lastname'], row['date'], row['working_hours']])
    
    with open(txt_filename, 'w') as txtfile:
        txtfile.write("Firstname, Lastname, Date, WorkingHours\n")
        for row in data:
            txtfile.write(f"{row['firstname']}, {row['lastname']}, {row['date']}, {row['working_hours']}\n")

def send_email_with_attachment(recipient_email, subject, body, attachment_path):
    """Send an email with an attachment."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(attachment_path)}',
        )
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

def send_reports():
    """Generate and send daily, weekly, and monthly reports."""
    # Dates for the reports
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    last_week_start = today - timedelta(days=today.weekday() + 7)
    last_week_end = last_week_start + timedelta(days=6)
    last_month_start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_month_end = today.replace(day=1) - timedelta(days=1)

    # Generate and save daily report
    daily_data = fetch_working_hours(yesterday, yesterday)
    daily_filename = generate_report_filename('daily_report')
    save_report(daily_data, daily_filename)
    
    # Generate and save weekly report
    weekly_data = fetch_working_hours(last_week_start, last_week_end)
    weekly_filename = generate_report_filename('weekly_report')
    save_report(weekly_data, weekly_filename)
    
    # Generate and save monthly report
    monthly_data = fetch_working_hours(last_month_start, last_month_end)
    monthly_filename = generate_report_filename('monthly_report')
    save_report(monthly_data, monthly_filename)
    
    # Fetch manager emails
    manager_emails = fetch_managers_emails()
    
    # Send reports via email
    for email in manager_emails:
        send_email_with_attachment(email, 'Daily Report', 'Please find the daily report attached.', daily_filename + '.csv')
        send_email_with_attachment(email, 'Weekly Report', 'Please find the weekly report attached.', weekly_filename + '.csv')
        send_email_with_attachment(email, 'Monthly Report', 'Please find the monthly report attached.', monthly_filename + '.csv')

if __name__ == "__main__":
    ensure_backup_folder()
    send_reports()
