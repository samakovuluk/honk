from selenium import webdriver
import csv
import time
import pickle
import random
import sys
from datetime import datetime


url = 'https://hk.carousell.com'

driver = webdriver.Chrome('C:\\Users\\Ulukbek\\Downloads\\chromedriver_win32 (1)\\chromedriver.exe')

driver.get(url)

while True:
    time.sleep(2)

    if driver.find_elements_by_xpath("//p[contains(text(), 'Register')]")==[]:
        if driver.find_elements_by_xpath("//p[contains(text(), '註冊')]")==[]:
           if driver.find_elements_by_xpath("//p[contains(text(), '立即注册')]")==[]:
                time.sleep(2)
                pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
                print('success saved in cokokies.')
                break


driver.quit()
