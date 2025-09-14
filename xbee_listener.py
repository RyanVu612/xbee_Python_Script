from digi.xbee.devices import XBeeDevice
from pymavlink import mavutil
import time

# --- XBee Configuration ---
LOCAL_XBEE_PORT = "COM4" # Replace with your local XBee's serial port

try:
    # Initialize local XBee device
    local_xbee = XBeeDevice(LOCAL_XBEE_PORT, 9600)
    local_xbee.open()

    print("XBee connected. Waiting for MAVLink messages...")

    while True:
        # Read data from XBee
        xbee_message = local_xbee.read_data()

        if xbee_message is not None:
            mavlink_data = xbee_message.data
            # Process MAVLink data (e.g., print message type)
            try:
                msg = mavutil.mavlink.MAVLink_message.decode(mavlink_data)
                print(f"Received MAVLink message: {msg.get_type()}")
            except mavutil.mavlink.MAVLink_error as e:
                print(f"Error decoding MAVLink message: {e}")

        time.sleep(0.1) # Check for new data frequently

except Exception as e:
    print(f"Error: {e}")

finally:
    if 'local_xbee' in locals() and local_xbee.is_open():
        local_xbee.close()
        print("XBee connection closed.")