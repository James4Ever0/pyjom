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
    noSign=True
)

appium_server_url = 'http://localhost:4723'

driver = webdriver.Remote(appium_server_url, capabilities)

el = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Battery"]')
el.click()


if driver:
    driver.quit()
