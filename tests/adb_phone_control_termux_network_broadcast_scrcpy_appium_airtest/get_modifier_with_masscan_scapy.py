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
myPort = 5555
myInterface = "wlan0"

# list avaliable devices.
from adb_wrapper import AdbWrapper
a = AdbWrapper()
devices = a.devices()
print(devices)
# exit()
connected_addresses = []
for key, value in devices.items():
    address = key
    connected_addresses.append(address)
    deviceType = value
# not working.

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
    mas.scan(scanAddress, ports=str(myPort), arguments='--max-rate 1000')
    result = mas.scan_result
    # usually it only show opens.
    import json
    scanResultDict = json.loads(result)['scan']
    for key, value in scanResultDict.items():
        address = key
        for port in value:
            if port['port'] == myPort and port['status'] =='open':
                # print(address, myPort)
                # we need to connect to it!
                connect_address = "{}:{}".format(address,myPort)
                print(connect_address)
                if not connect_address in connected_addresses:
                    print("connecting device:", connect_address)
                    # command1 = "adb tcpip 5555"
                    # no need to restart?
                    command2 = "adb connect {}".format(connect_address)
                    # os.system(command1)
                    os.system(command2)