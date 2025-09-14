from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models import XBee64BitAddress
from pymavlink import mavutil
import time

# --- XBee Configuration ---
LOCAL_XBEE_PORT = "/dev/cu.USB#AQ015EBI"  # Replace with your local XBee's serial port
REMOTE_XBEE_ADDRESS = "0013A20041D365C4" # Replace with the 64-bit address of the remote XBee

# --- MAVLink Configuration ---
# Create a MAVLink connection (e.g., to a flight controller or simulator)
# This example uses a UDP connection to a local simulator on port 14550
# Adjust as needed for your setup (e.g., serial connection to a flight controller)
master = mavutil.mavlink_connection('udpout:localhost:14550', baud=115200)

try:
    # Initialize local XBee device
    local_xbee = XBeeDevice(LOCAL_XBEE_PORT, 9600)
    local_xbee.open()

    # Initialize remote XBee device
    remote_xbee = RemoteXBeeDevice(local_xbee, XBee64BitAddress.from_hex_string(REMOTE_XBEE_ADDRESS))

    print("XBee connected. Sending MAVLink heartbeats...")

    while True:
        # Create a MAVLink heartbeat message
        heartbeat_msg = master.mav.heartbeat_encode(
            mavutil.mavlink.MAV_TYPE_GENERIC,
            mavutil.mavlink.MAV_AUTOPILOT_GENERIC,
            0, 0, 0, 0
        )

        # Convert MAVLink message to bytes
        mavlink_data = heartbeat_msg.pack(master.mav)

        # Send MAVLink data via XBee
        local_xbee.send_data(remote_xbee, mavlink_data)
        print(f"Sent MAVLink heartbeat: {heartbeat_msg.get_type()}")

        time.sleep(1) # Send every second

except Exception as e:
    print(f"Error: {e}")

finally:
    if 'local_xbee' in locals() and local_xbee.is_open():
        local_xbee.close()
        print("XBee connection closed.")