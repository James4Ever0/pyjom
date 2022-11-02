#!/usr/bin/env python
# -*- coding: utf-8 -*-

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='com.android.settings',
    appActivity='.Settings',
    language='en',
    locale='US',
    noSign=True,
    skipUnlock=True
    # it tries to clear my password.
)

appium_server_url = 'http://localhost:4723'

driver = webdriver.Remote(appium_server_url, capabilities)
print('is screen ready?')
while True:
    try:
        locked = driver.is_locked()
        print('locked?', locked)
        if not locked:
            break
        import os
        if locked:
            os.system("bash adb_unlock.sh")
            print("UNLOCKED")
    except:
        pass

# unlocking the phone will disconnect adb sessions



if driver:
    driver.quit()
