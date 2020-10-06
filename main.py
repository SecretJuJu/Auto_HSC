#!/usr/bin/python

# -*- coding: 949 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


from defs import getDriver
from defs import selectByText

import time

hcsurl = "https://hcs.eduro.go.kr/#/loginHome"

def err_check_your_network(e):
    print (e)
    print ("네트워크 연결을 확인하세요")
    exit(-1)
if __name__ == "__main__":
    driver = getDriver()
    driver.get(hcsurl)
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
        if (not selectByText(driver,city,"서울특별시")):
            print("city info is wrong")
            exit(-1)
        if (not selectByText(driver,school_level,"고등학교")):
            print("school level is wrong")
        
        schoolname = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector(".searchArea"))
        schoolname.click()
        schoolname.send_keys("선린인터넷고등학교")
        schoolname.send_keys(Keys.RETURN)
        try :
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector(".layerSchoolArea>li>p>a")).click()
            driver.find_element_by_css_selector(".layerFullBtn").click()
        except Exception as e:
            print(e)
            print ("Probably the schoolname is not clear.")
            exit(-1)
        
    except Exception as e:
        err_check_your_network(e)
    
    