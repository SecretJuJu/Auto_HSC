#!/usr/bin/python

# -*- coding: 949 -*-

from selenium import webdriver
import os
import time
def getDriver():
    try:
        if (os.path.isfile("./driverpath.txt")):
            f = open("./driverpath.txt","r")
            driverpath = f.readline()
            print(f"dirver path : {driverpath}")
            f.close()
            driver = webdriver.Chrome(driverpath)
            return driver
        else :
            print("please write driverpath.txt")
            f=open("./driverpath.txt","w")
            f.close()
            exit(-1)
    except Exception as e:
        print("----------------- error -----------------")
        print (e)
        print("Probably the error is in the chromedriver\nThe path is must be english")
        exit(-1)

def selectByText(driver,ss,sel):
    ss.click()
    time.sleep(0.5)
    for s in  ss.find_elements_by_css_selector("option"):
        print(s.text)
        if (s.text == sel):
            s.click()
            ss.click()
            return True
    return False
