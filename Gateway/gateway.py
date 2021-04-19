import socket
import struct

from network import LoRa

# A basic package header, B: 1 byte for the deviceId, B: 1 byte for the pkg size, %ds: Formated string for string
_LORA_PKG_FORMAT = "!BB%ds"
# A basic ack package, B: 1 byte for the deviceId, B: 1 bytes for the pkg size, B: 1 byte for the Ok (200) or error messages
_LORA_PKG_ACK_FORMAT = "BBB"

# The region in Europe is LoRa.EU868
lora = LoRa(mode=LoRa.LORA, rx_iq=True, region=LoRa.EU868)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setblocking(False)

while (True):
   recv_pkg = lora_sock.recv(512)
   if (len(recv_pkg) > 2):
      recv_pkg_len = recv_pkg[1]

      device_id, pkg_len, msg = struct.unpack(_LORA_PKG_FORMAT % recv_pkg_len, recv_pkg)

      print('Device: %d - Pkg:  %s' % (device_id, msg))

      ack_pkg = struct.pack(_LORA_PKG_ACK_FORMAT, device_id, 1, 200)
      lora_sock.send(ack_pkg)