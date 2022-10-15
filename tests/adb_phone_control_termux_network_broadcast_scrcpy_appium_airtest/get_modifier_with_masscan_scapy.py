# strange.
from __future__ import absolute_import, division, print_function
import logging
import scapy.config
import scapy.layers.l2
import scapy.route
import socket
import math
import errno
import os
import getopt
import sys
myInterface = "wlan0"
if os.geteuid() != 0:
        print('You need to be root to run this script', file=sys.stderr)
        sys.exit(1)
scanAddress = None
for network, netmask, _, interface, address, _ in scapy.config.conf.route.routes:
    # print(interface, address)
    if interface == myInterface:
        myAddress = address.split(".")
        myAddress[3] = "0/24"
        scanAddress = ".".join(myAddress)
        print(scanAddress, interface)
        break
if scanAddress is not None:
    # now scan this interface with masscan.
    import masscan
    mas = masscan.PortScanner()
    mas.scan(scanAddress, ports='5555', arguments='--max-rate 1000')
    print(mas.scan_result)