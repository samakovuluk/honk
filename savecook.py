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

#pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
