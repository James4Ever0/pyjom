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

for network, netmask, a, interface, address, b in scapy.config.conf.route.routes:
    print(network, netmask, a, interface, address, b )