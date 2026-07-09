import serial
import time
import database
from datetime import datetime

# Serial port configuration
PORT = "/dev/cu.usbmodem14101"
BAUD_RATE = 9600
ser = None

# valid events and their severity levels
SEVERITY_MAP = {
    "TEMP_HIGH": "MEDIUM",
    "HUMIDITY_HIGH": "MEDIUM",
    "AIR_QUALITY_ALERT": "HIGH",
    "SYSTEM_FAULT": "HIGH",
    "SYSTEM_FAILURE_CHECK_ALL": "CRITICAL",
}


# Initialize the serial connection
def init_serial():
    global ser
    ser = serial.Serial(PORT, BAUD_RATE)


# Reconnect to the serial port
def reconnect():
    global ser
    print("Arduino disconnected. Attempting to reconnect...")
    while True:
        try:
            ser = serial.Serial(PORT, BAUD_RATE)
            print("Reconnected successfully.")
            break
        except serial.SerialException:
            print("Retrying in 5 seconds...")
            time.sleep(5)


# Read data from the serial port
def read_serial_data():
    data = ser.readline()
    if data is None:
        return ""
    return data.decode("utf-8").strip()


# Process the serial data
def process_serial_data(data):
    return data in SEVERITY_MAP


# Write data to the database
def write_to_database(data, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()
    severity = SEVERITY_MAP.get(data, "INFO")
    database.insert_event(data, timestamp, severity, None)


# Main loop to read serial datawrite to the database
if __name__ == "__main__":
    database.init_database()
    init_serial()
    reading = True
    while reading:
        print("Reading serial data...")
        try:
            data = read_serial_data()
            if process_serial_data(data):
                write_to_database(data)
                print(f"Event logged: {data}")
        except serial.SerialException:
            reconnect()

        # end on keyboard interrupt
        except KeyboardInterrupt:
            print("Serial listener stopped.")
            ser.close()
            reading = False
