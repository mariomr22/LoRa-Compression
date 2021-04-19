import os
import socket
import struct
import time
import random
from network import LoRa

# A basic package header
# B: 1 byte for the deviceId
# B: 1 bytes for the pkg size
# %ds: Formated string for string
_LORA_PKG_FORMAT = "BB%ds"

# A basic ack package
# B: 1 byte for the deviceId
# B: 1 bytes for the pkg size
# B: 1 bytes for the success or error message
_LORA_PKG_ACK_FORMAT = "BBB"

#The deviceID changes in each device
DEVICE_ID = 0x01

# Open a Lora Socket in Europe region. The value tx_iq avoid listening to our own messages
lora = LoRa(mode=LoRa.LORA, tx_iq=True, region=LoRa.EU868)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setblocking(False)

while(True):
    # Package send containing a simple string
    randomValue = random.randint(15,35)
    msg = str(round(randomValue),1)
    pkg = struct.pack(_LORA_PKG_FORMAT % len(msg), DEVICE_ID, len(msg), msg)
    print("The value is: " + msg)
    lora_sock.send(pkg)
        
    # Wait for the response from the gateway. NOTE: For this demo the device does an infinite loop for while waiting the response. Introduce a max_time_waiting for you application
    waiting_ack = True
    while(waiting_ack):
        recv_ack = lora_sock.recv(256)
        
        if (len(recv_ack) > 0):
            device_id, pkg_len, ack = struct.unpack(_LORA_PKG_ACK_FORMAT, recv_ack)
            if (device_id == DEVICE_ID):
                if (ack == 200):
                    waiting_ack = False
                    # If the uart = machine.UART(0, 115200) and os.dupterm(uart) are set in the boot.py this print should appear in the serial port
                    print("ACK")
                else:
                    waiting_ack = False
                    # If the uart = machine.UART(0, 115200) and os.dupterm(uart) are set in the boot.py this print should appear in the serial port
                    print("Message Failed")
    
    time.sleep(300)