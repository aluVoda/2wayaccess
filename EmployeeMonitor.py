import threading
import Simulation
import Reports

def start_monitoring():
    # You can simulate or set up a real-time monitoring system here
    print("Starting employee monitoring system...")
    Simulation.simulate_access_logs()

def start_report_scheduling():
    print("Starting report scheduling...")
    Reports.schedule_reports()

if __name__ == "__main__":
    # Run monitoring and report scheduling in parallel threads
    monitoring_thread = threading.Thread(target=start_monitoring)
    scheduling_thread = threading.Thread(target=start_report_scheduling)

    monitoring_thread.start()
    scheduling_thread.start()

    monitoring_thread.join()
    scheduling_thread.join()
