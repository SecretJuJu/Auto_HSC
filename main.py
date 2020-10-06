from selenium import webdriver

import os

try:
    if (os.path.isfile("./driverpath.txt")):
        f = open("./driverpath.txt","r")
        driverpath = f.readline()
        print(f"dirver path : {driverpath}")
        f.close()
        driver = webdriver.Chrome(driverpath)
    else :
        print("please write driverpath.txt")
        f=open("./driverpath.txt","w")
        f.close()
        exit(-1)
except Exception as e:
    print("error")
# https://hcs.eduro.go.kr/