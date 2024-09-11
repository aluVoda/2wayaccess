import os
import time
import threading

# Importing modules from various parts of the app
from DatabaseSetup import create_or_update_database
from EmploymentStatus import populate_employees
from Gates import simulate_gate_activity
from Reports import schedule_reports

def run_database_setup():
    print("Setting up the database...")
    create_or_update_database()

def run_employee_setup():
    print("Setting up employee data (full-time and part-time)...")
    populate_employees()

def run_gate_simulation():
    print("Starting gate activity simulation...")
    from Gates import gates, employees
    simulate_gate_activity(gates, employees)

def run_reports_scheduler():
    print("Scheduling report generation...")
    schedule_reports()

def main():
    print("Starting the 2Way Access Control System...")

    # Step 1: Set up the database
    run_database_setup()

    # Step 2: Set up employees in the database
    run_employee_setup()

    # Step 3: Run gate simulation (simulates last 60 days)
    gate_simulation_thread = threading.Thread(target=run_gate_simulation)
    gate_simulation_thread.start()

    # Step 4: Schedule report generation (runs daily, weekly, and monthly reports)
    report_scheduler_thread = threading.Thread(target=run_reports_scheduler)
    report_scheduler_thread.start()

    # Step 5: Keep the main process running indefinitely to manage background tasks
    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\nShutting down the system...")
        gate_simulation_thread.join()
        report_scheduler_thread.join()

if __name__ == "__main__":
    main()
