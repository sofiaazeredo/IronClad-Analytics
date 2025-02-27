import json
import csv
import time
from datetime import datetime

# File where gas readings are logged
LOG_FILE = "gas_readings.json"
REPORT_CSV = "gas_report.csv"
REPORT_JSON = "gas_report.json"

# Load logged readings
def load_readings():
    try:
        with open(LOG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("No gas readings found. Please run the gas reading script first.")
        return []

def generate_report():
    data = load_readings()
    if not data:
        return

    summary = {}
    
    for entry in data:
        timestamp = entry["timestamp"]
        for sensor, value in entry["readings"].items():
            if sensor not in summary:
                summary[sensor] = {"values": [], "min": None, "max": None, "avg": None}
            summary[sensor]["values"].append(value)
    
    for sensor, stats in summary.items():
        stats["min"] = min(stats["values"])
        stats["max"] = max(stats["values"])
        stats["avg"] = sum(stats["values"]) / len(stats["values"])
        del stats["values"]  # Remove raw values to keep the report clean
    
    # Save report as JSON
    with open(REPORT_JSON, "w") as file:
        json.dump(summary, file, indent=4)
    print(f"Report saved as {REPORT_JSON}")
    
    # Save report as CSV
    with open(REPORT_CSV, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Sensor", "Min (ppm)", "Max (ppm)", "Avg (ppm)"])
        for sensor, stats in summary.items():
            writer.writerow([sensor, stats["min"], stats["max"], stats["avg"]])
    print(f"Report saved as {REPORT_CSV}")

if __name__ == "__main__":
    generate_report()
