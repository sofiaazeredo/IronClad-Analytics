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

# Define MQ sensors and their ADS channels with calibration data
MQ_SENSORS = {
    "MQ-2":  {"adc": ads1, "channel": ADS.P1, "clean_air_ratio": 9.83, "r_load": 20, "A": 1000, "B": -2.2},
    "MQ-3":  {"adc": ads2, "channel": ADS.P2, "clean_air_ratio": 60, "r_load": 200, "A": 200, "B": -2.1},
    "MQ-4":  {"adc": ads1, "channel": ADS.P3, "clean_air_ratio": 4.4, "r_load": 20, "A": 400, "B": -1.9},
    "MQ-5":  {"adc": ads2, "channel": ADS.P1, "clean_air_ratio": 6.5, "r_load": 20, "A": 300, "B": -2.0},
    "MQ-6":  {"adc": ads1, "channel": ADS.P2, "clean_air_ratio": 10, "r_load": 60, "A": 500, "B": -2.3},
    "MQ-7":  {"adc": ads2, "channel": ADS.P3, "clean_air_ratio": 27, "r_load": 10, "A": 700, "B": -2.5},
    "MQ-8":  {"adc": ads1, "channel": ADS.P0, "clean_air_ratio": 70, "r_load": 10, "A": 150, "B": -1.8},
    "MQ-135": {"adc": ads2, "channel": ADS.P0, "clean_air_ratio": 3.6, "r_load": 20, "A": 220, "B": -2.1},
}

# Load calibration values from JSON
CALIBRATION_FILE = "calibration.json"
try:
    with open(CALIBRATION_FILE, "r") as file:
        calibration_values = json.load(file)
except FileNotFoundError:
    print("Calibration file not found. Please calibrate sensors first.")
    exit()

def get_voltage(sensor_name):
    """Reads the voltage from the MQ sensor."""
    sensor = MQ_SENSORS[sensor_name]
    mq = AnalogIn(sensor["adc"], sensor["channel"])
    return mq.voltage

def get_gas_concentration(sensor_name):
    """Calculates the gas concentration in ppm based on sensor readings."""
    sensor = MQ_SENSORS[sensor_name]
    R_LOAD = sensor["r_load"]
    A = sensor["A"]
    B = sensor["B"]
    Ro = calibration_values.get(sensor_name, None)
    
    if Ro is None:
        print(f"No calibration data for {sensor_name}. Run calibration first.")
        return None
    
    V_sensor = get_voltage(sensor_name)
    Rs = (5.0 - V_sensor) / V_sensor * R_LOAD
    ratio = Rs / Ro
    
    # Convert Rs/Ro ratio to ppm using the empirical formula
    ppm = A * (ratio ** B)
    return ppm

# Read gas concentration values from all sensors
print("\nGas Concentration Readings (ppm):")
for sensor in MQ_SENSORS:
    concentration = get_gas_concentration(sensor)
    if concentration is not None:
        print(f"{sensor}: {concentration:.2f} ppm")
    time.sleep(1)
