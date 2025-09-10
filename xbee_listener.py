import serial
from pymavlink.dialects.v20 import common as mavlink2  # MAVLink 2

# -----------------------------
# SETTINGS
# -----------------------------
PORT = "/dev/tty.usbserial-AR0JQZGS"   # receiving XBee port (try /dev/cu.usbserial-AR0JQZGS if tty fails)
BAUD = 9600                            # must match XCTU config
TIMEOUT = 1                            # seconds

def main():
    # Open the serial port
    ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
    print(f"[INFO] Listening for HEARTBEATs on {PORT} @ {BAUD} baud... Ctrl+C to stop.")

    # Create MAVLink parser
    mav = mavlink2.MAVLink(ser)
    mav.WIRE_PROTOCOL_VERSION = "2.0"

    try:
        while True:
            byte = ser.read(1)  # read one byte at a time
            if not byte:
                continue

            msg = mav.parse_char(byte)
            if msg and msg.get_type() == "HEARTBEAT":
                print(f"❤️  HEARTBEAT from sys={msg.get_srcSystem()}, comp={msg.get_srcComponent()} "
                      f"type={msg.type}, autopilot={msg.autopilot}, "
                      f"base_mode={msg.base_mode}, custom_mode={msg.custom_mode}, "
                      f"system_status={msg.system_status}")

    except KeyboardInterrupt:
        print("\n[INFO] Listener stopped.")
    finally:
        ser.close()
        print("[INFO] Port closed.")

if __name__ == "__main__":
    main()
