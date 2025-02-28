import subprocess
import time
from datetime import datetime

# Run the calibration script (optional, can be skipped if already calibrated)
print("Running calibration...")
subprocess.run(["python3", "calibration.py"]) 

time.sleep(2)  # Small delay to ensure the system is ready

# Run the gas reading script
print("Running gas reading...")
subprocess.run(["python3", "reading.py"]) 

time.sleep(2)

# Generate a unique report filename based on timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
report_filename = f"gas_report_{timestamp}.txt"

# Run the report script with the generated filename
print(f"Generating report: {report_filename}")
subprocess.run(["python3", "report.py", report_filename])

print("Process completed.")
