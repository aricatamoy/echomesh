# from __future__ import absolute_import, division, print_function, unicode_literals

import os
import socket

from util import Platform


def ip_address():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('8.8.8.8', 80))
  name = s.getsockname()[0]
  s.close()
  return name


if Platform.IS_LINUX:
  import fcntl, socket, struct

  # From here: http://stackoverflow.com/questions/159137/getting-mac-address
  def get_hw_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # b = b'256s'
    b = '256s'
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack(b, ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

  def mac_address():
    return get_hw_addr('eth0')

else:
  import uuid
  def mac_address():
    myMAC = uuid.getnode()
    return ':'.join('%02X' % ((myMAC >> 8*i) & 0xff) for i in reversed(xrange(6)))

MAC_ADDRESS = mac_address()
IP_ADDRESS = ip_address()
NODENAME = os.uname()[1]

if __name__ == '__main__':
  print(mac_address())
  print(ip_address())