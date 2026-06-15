import serial
import database
from datetime import datetime

# Serial port configuration
PORT = '/dev/tty.usbmodem14101'
BAUD_RATE = 9600

# valid events and their severity levels
SEVERITY_MAP = {
    "TEMP_HIGH": "MEDIUM",
    "HUMIDITY_HIGH": "MEDIUM",
    "AIR_QUALITY_ALERT": "HIGH",
    "SYSTEM_FAULT": "HIGH",
    "SYSTEM_FAILURE_CHECK_ALL": "CRITICAL"
}

# Initialize the serial connection
ser = serial.Serial(PORT, BAUD_RATE)

# Main loop to read serial data
try:
    while True:
        data = ser.readline().decode('utf-8').strip()
        if data in SEVERITY_MAP:
            time = datetime.now()
            severity = SEVERITY_MAP.get(data, "INFO")
            database.insert_event(data, time, severity, None)    

# end on keyboard interrupt
except KeyboardInterrupt:
    print("Serial listener stopped.")
    ser.close()