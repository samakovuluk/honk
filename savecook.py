from selenium import webdriver
import csv
import time
import pickle
import random
import sys
from datetime import datetime


url = 'https://hk.carousell.com'

driver = webdriver.Chrome('D:/Chromedriver_win32/chromedriver.exe')

driver.get(url)

while True:
    time.sleep(2)
    try:
        driver.find_element_by_xpath("//button[@type = 'button'][contains(text(), 'New User? Register')]");
    except:
        time.sleep(3)
        pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
        break

driver.quit()
