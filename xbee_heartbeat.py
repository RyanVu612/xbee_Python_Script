import argparse, time, sys
import serial
from pymavlink.dialects.v20 import common as mavlink2   # MAVLink 2

def main():
    ap = argparse.ArgumentParser(description="Send MAVLink HEARTBEAT over Xbee serial")
    ap.add_argument("--port", required=True, help="Serial port for Xbee (e.g., /dev/ttyUSB0 or COM3)")
    ap.add_argument("--baud", type=int, default=9600, help="Baud rate for serial communication (default: 9600)")
    ap.add_argument("--sysid", type=int, default=255, help="Our MAVLink system id (255 = GCS/ground)")
    ap.add_argument("--compid", type=int, default=190, help="Our MAVLink component id (190 = logger/UI; use 190-199)")
    ap.add_argument("--rate", type=float, default=1.0, help="Heartbeat rate Hz (default: 1.0)")
    ap.add_argument("--type", type=int, default=mavlink2.MAV_TYPE_GCS, help="MAV_TYPE_* (default GCS)")
    ap.add_argument("--autopilot", type=int, default=mavlink2.MAV_AUTOPILOT_INVALID, help="MAV_AUTOPILOT_*")
    ap.add_argument("--status", type=int, default=mavlink2.MAV_STATE_ACTIVE, help="MAV_STATE_*")
    args = ap.parse_args()

    #Open serial to Xbee
    ser = serial.Serial(args.port, args.baud, timeout=0)

    #Create a MAVLink connection object that writes to the same serial port file descriptor
    # (pymavlink will frame/CRC the bytes for us)
    mav = mavlink2.MAVLink(ser)
    #Tell pymavlink we want MAVLink 2 framing
    mav.WIRE_PROTOCOL_VERSION = "2.0"

    # set source IDs
    mav.srcSystem = args.sysid
    mav.srcComponent = args.compid

    interval = 1.0 / max(args.rate, 0.001)
    print(f"Sending HEARTBEAT on {args.port} at {args.baud} ({args.rate} Hz). Press Ctrl+C to stop.")
    try:
        while True:
            #Create and send a HEARTBEAT message
            #Fields: type, autopilot, base_mode, custom_mode, system_status
            msg = mav.heartbeat_encode(
                args.type,
                args.autopilot,
                0,  # base_mode (bitmask);
                0,   # custom_mode (vehicle-specific)
                args.status
            )
            #send with our sysid/compid
            msg.pack(mav)
            mav.send(msg)

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        ser.close()

if __name__ == "__main__":
    main()