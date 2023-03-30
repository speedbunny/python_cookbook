# -*- coding: utf-8 -*-
"""
Generate OTP on screen instead of phone
Created on Mon Jun 21 08:28:15 2021
@author: SEaglesfield
"""
import pyotp
import selenium
from selenium import webdriver


print("your really long password you don't want to type in is: 50l;--#055nUh]zORR0")

print("Azure \n")
totp = pyotp.TOTP("[QR Code Here]")
print("Current OTP:", totp.now())
token = totp.now()

print("AWS \n")
totp = pyotp.TOTP("[QR Code 2 Here]")
print("Current OTP:", totp.now())
token = totp.now()

#driver = webdriver.chrome.webdriver.WebDriver(executable_path='C:/Downloads/geckodriver.exe')

#driver.get("http://www.python.org")

# find OTP element on page and send token
#e = driver.find_elements_by_ID(selenium.By.ID, "auth-mfa-otpcode")
#e.selenium.send_keys(totp.now())

