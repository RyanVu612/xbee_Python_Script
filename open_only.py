from digi.xbee.devices import DigiMeshDevice
import os
PORT = os.environ.get("XBEE_PORT", "/dev/cu.usbserial-AQ015EBI")
BAUD = int(os.environ.get("XBEE_BAUD", "9600"))
print("Trying to open", PORT, "@", BAUD, flush=True)
xb = DigiMeshDevice(PORT, BAUD)
xb.open()
print("OPENED. Protocol:", xb.get_protocol().name, flush=True)
xb.close()
print("CLOSED.", flush=True)
