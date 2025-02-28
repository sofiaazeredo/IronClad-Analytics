import time
import json
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Create two ADS1115 instances with different addresses
ads2 = ADS.ADS1115(i2c, address=0x48)  # First ADC (ADDR → GND)
ads1 = ADS.ADS1115(i2c, address=0x49)  # Second ADC (ADDR → VCC)

# Define MQ sensors and their ADS channels
MQ_SENSORS = {
    "MQ-2":  {"adc": ads2, "channel": ADS.P0, "clean_air_ratio": 9.83, "r_load": 20, "A": 1000, "B": -2.2},
    "MQ-3":  {"adc": ads2, "channel": ADS.P2, "clean_air_ratio": 60, "r_load": 200, "A": 200, "B": -2.1},
    "MQ-4":  {"adc": ads1, "channel": ADS.P3, "clean_air_ratio": 4.4, "r_load": 20, "A": 400, "B": -1.9},
    "MQ-5":  {"adc": ads1, "channel": ADS.P2, "clean_air_ratio": 6.5, "r_load": 20, "A": 300, "B": -2.0},
    "MQ-6":  {"adc": ads1, "channel": ADS.P0, "clean_air_ratio": 10, "r_load": 60, "A": 500, "B": -2.3},
    "MQ-7":  {"adc": ads1, "channel": ADS.P1, "clean_air_ratio": 27, "r_load": 10, "A": 700, "B": -2.5},
    "MQ-8":  {"adc": ads2, "channel": ADS.P1, "clean_air_ratio": 70, "r_load": 10, "A": 150, "B": -1.8},
    "MQ-135": {"adc": ads2, "channel": ADS.P3, "clean_air_ratio": 3.6, "r_load": 20, "A": 220, "B": -2.1},
}

CALIBRATION_FILE = "calibration.json"
SAMPLES = 100  # Number of samples for calibration

def get_voltage(sensor_name):
    """Reads the voltage from the MQ sensor."""
    sensor = MQ_SENSORS[sensor_name]
    mq = AnalogIn(sensor["adc"], sensor["channel"])
    return mq.voltage

def calibrate_sensors():
    """Calibrates all MQ sensors by measuring Ro in clean air."""
    calibration_values = {}
    print("Starting calibration. Ensure sensors are in clean air.")
    time.sleep(2)
    
    for sensor_name, sensor in MQ_SENSORS.items():
        print(f"Calibrating {sensor_name}...")
        voltages = []
        
        for _ in range(SAMPLES):
            voltages.append(get_voltage(sensor_name))
            time.sleep(0.1)
        
        avg_voltage = sum(voltages) / len(voltages)
        Rs = (5.0 - avg_voltage) / avg_voltage * sensor["r_load"]
        Ro = Rs / sensor["clean_air_ratio"]
        
        calibration_values[sensor_name] = Ro
        print(f"{sensor_name} Ro: {Ro:.2f}")
        
    with open(CALIBRATION_FILE, "w") as file:
        json.dump(calibration_values, file, indent=4)
    print("Calibration completed and saved to calibration.json")

calibrate_sensors()
