
#!/usr/bin/python
# -*- coding: 949 -*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


import time
import json
import argparse
import os
from datetime import date




hcsurl = "https://hcs.eduro.go.kr/#/loginHome"

def err_check_your_network(e):
    print (e)
    print ("네트워크 연결을 확인하세요")
    exit(-1)

def loadJson(filename):
    print(filename)
    with open("./user_datas/"+filename,"r",encoding="UTF8") as json_file:
        json_data = json.load(json_file)
        return json_data
    return False

def getDriver(options):
    try:
        if (os.path.isfile("./driverpath.txt")):
            f = open("./driverpath.txt","r")
            driverpath = f.readline()
            print(f"dirver path : {driverpath}")
            f.close()
            driver = webdriver.Chrome(driverpath,options=options)
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


if __name__ == "__main__":
    if not os.path.isdir("./user_datas"):
        print("can't find ./user_datas directory.")
        exit(-1)
    today = date.today()

    user_datas = loadJson("datas.json")
    
    for user_data in user_datas["user_datas"]:
        is_success = False
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = getDriver(options=op)
        driver.get(hcsurl) # hcsurl : link
        ## click the btnConfirm2 btn ##
        try :
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("btnConfirm2")).click()
        except Exception as e:
            err_check_your_network(e)

        ## click find school btn ##
        try :
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector(".searchBtn")).click()
        except Exception as e:
            err_check_your_network(e)
        
        ## select your school ##
        try :
            selects = WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_css_selector("select"))
            city = selects[0]
            school_level = selects[1]
            if (not selectByText(driver,city,user_data["city"])):
                print("city info is wrong")
                exit(-1)
            if (not selectByText(driver,school_level,user_data["school_level"])):
                print("school level is wrong")
            
            schoolname = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector(".searchArea"))
            schoolname.click()
            schoolname.send_keys(user_data["school_name"])
            schoolname.send_keys(Keys.RETURN)
            try :
                WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector(".layerSchoolArea>li>p>a")).click()
                driver.find_element_by_css_selector(".layerFullBtn").click()
            except Exception as e:
                print(e)
                print ("Probably the schoolname is not clear.")
                exit(-1)
            ## input name
            # .input_text_common
            toInput = WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_css_selector(".input_text_common"))
            name = toInput[1]
            birth = toInput[2]
            name.click()
            name.send_keys(user_data["user_name"])
            birth.click()
            birth.send_keys(user_data["user_birth"])
            birth.send_keys(Keys.RETURN)
            time.sleep(3)
            password = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector(".input_text_common"))
            password.click()
            password.send_keys(user_data["user_pass"])
            password.send_keys(Keys.RETURN)
            time.sleep(2)
            user = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector(".name")) 
            user.click()

            # self check start
            time.sleep(2)
            have_to_sels = WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_css_selector(".survey_question dl li:nth-child(1)>label")) # List the questions to be selected
            print(have_to_sels)
            for s in have_to_sels: # health check self
                print(s.text)
                s.click()
                time.sleep(0.2)
            # click btnConfirm
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector("#btnConfirm")).click() # click the submit btn 
            time.sleep(3)
            
            print("take screenshot")
            screenshot_path = "./screenshots/"+str(today)
            os.makedirs(screenshot_path,exist_ok=True)
            screenshot_path +="/"+str(today)+"_"+str(user_data["facebook_uid"])+".png"
            driver.save_screenshot(screenshot_path)
            is_success = True

        except Exception as e:
            err_check_your_network(e)
            pass
        finally :
            driver.close()
