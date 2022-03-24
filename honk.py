from selenium import webdriver
import csv
import time
import pickle
import random
import sys
from datetime import datetime
import requests
import string
from bs4 import BeautifulSoup
import traceback
import sys
import random
import openpyxl
from datetime import datetime
import os
from selenium.webdriver.common.keys import Keys
now = datetime.now() # current date and time
import fileinput
url = 'https://www.carousell.sg'
options = webdriver.ChromeOptions()
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)

driver.get(url)

indexG = 0
counterRef = 0
counterSub = 0
counter = 0
counterFill = 0

driver.get('https://www.carousell.sg/sell')
driver.execute_script('window.localStorage.clear();')
driver.execute_script("window.onbeforeunload = function() {};")
time.sleep(1)


#Writing result in LogFile, getting two parameters list and boolean.
#list which is containg values of item, and boolean result of uploaded item
def submitLog(row, b):
    logs = open('log.txt','a+')
    for i in row:
        logs.write(str(i.encode("utf-8")))
        logs.write(',')
    logs.write(str(datetime.now()))
    logs.write(',')
    if b == True:
        logs.write('Success')
    else:
        logs.write('Fail')
    logs.write('\n')
    logs.close()

#is hard refreshing by cleaning caches and opening given url
def super_get(url):
    counterRef = 0
    counterSub = 0
    counter = 0
    counterFill = 0
    driver.execute_script("window.alert = null;")
    driver.execute_script("Window.prototype.alert = null;")
    driver.refresh()
    time.sleep(3)
    try:
        alert_obj = driver.switch_to.alert
        time.sleep(1)
        alert_obj.accept()
        alert_obj.dismiss()
        time.sleep(1)
        driver.execute_script("window.alert = null;")
        driver.execute_script("Window.prototype.alert = null;")
        webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()
    except:
        print('s')
    time.sleep(1)
    driver.get(url)
    time.sleep(2)
    webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()
    
    

#Selecting all selectable fields randomly
def selectFill():
    elm = driver.find_elements_by_xpath("//div[@role='dropdown']")
    for i in range(1,len(elm)):
        #Hear we checking is the field is optional or not, if not so we selecting
        if '(Optional)' not in elm[i].text and 'Add location' not in elm[i].text:
            elm[i].click()
            time.sleep(2)
            p = elm[i].find_element_by_xpath('parent::*')
            elem = p.find_elements_by_class_name('_1H4f-PmiEr')
            if len(elem)>0:
                elem[random.randint(0,len(elem)-1)].click()
                print('Dropdown selected')
                time.sleep(1)
def selectBrand():
    try: 
        em = driver.find_elements_by_xpath("//span[contains(text(), 'Brand')]")
        em[0].click()
        time.sleep(2)
        em = driver.find_elements_by_xpath("//div[@data-testid]")
        em[-1].click()
    except:
        try:
            em = driver.find_elements_by_xpath("//input[@aria-label='Brand'][@name='field_brand']")
            em[0].send_keys('As listed')
        except:
            em = driver.find_elements_by_xpath("//span[contains(text(), 'Brand')]")
            em = em.parent.find_elements_by_xpath("//p[contains(text(), 'Others')]")
            em[0].click()



def dealMethod():
    em = driver.find_elements_by_xpath("//p[contains(text(), 'Delivery')]")
    em[0].click()
    time.sleep(1)
    em = driver.find_elements_by_xpath("//p[contains(text(), 'Custom courier')]")
    em[0].click()
    time.sleep(1)
    em = driver.find_elements_by_xpath("//div[@data-testid='delivery_period_dropdown'][@role='dropdown']")
    em[0].click()
    time.sleep(1)
    em = driver.find_elements_by_xpath("//div[@data-testid='5']")
    em[0].click()
    time.sleep(1)
    em = driver.find_elements_by_xpath("//input[@name='shipping_custom_delivery']")
    em[0].send_keys(5)
    time.sleep(1)

def typeD():
    try:
        typ = driver.find_elements_by_xpath("//span[contains(text(), 'Type')]")[0]
        typ.click()
        time.sleep(2)
        em = typ.find_elements_by_xpath("//div[@data-testid]")
        em[-1].click()
        driver.find_elements_by_xpath("//h2[contains(text(), 'payment methods')]")[0].click()
    except:
        typ = driver.find_elements_by_xpath("//p[contains(text(), 'Type')]")[0]
        em = typ.parent.find_elements_by_xpath("//p[contains(text(), 'Others')]")
        em[0].click()
        typ.click()

def ageRange():
    typ = driver.find_elements_by_xpath("//span[contains(text(), 'Age Range')]")[0]
    typ.click()
    em = typ.find_elements_by_xpath("//div[@data-testid]")
    em[-1].click()
    typ.click()
    




    

#Choose all radio buttons randomly
def radioFill():
    elm = driver.find_elements_by_xpath("//input[@type='radio']")
    d = dict()
    for i in range(len(elm)):
        if elm[i].get_attribute('name') not in d:
            d[elm[i].get_attribute('name')] = []
            d[elm[i].get_attribute('name')].append(elm[i])
        else:
            d[elm[i].get_attribute('name')].append(elm[i])
    for i in d:
        print(len(d[i]))
        t = random.randint(0,len(d[i])-1)
        elm = d[i][t]
        el = elm.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
        el = el.find_element_by_class_name('_1gJzwc_bJS')
        #Here we checking is Optional or not, if not so we choose
        if '(Optional)' not in el.text:
            d[i][t].click()
            print('Radio button selected')
        time.sleep(1)

#Chek mailing chechbox
def checkboxMailingFill():
    elm = driver.find_element_by_xpath("//input[@type='checkbox'][@value='mailing']")
    elm.click()
    print('Checkbox cheked')


#Fill all text field with text 'sample' where is required
def textFill():
    elm = driver.find_elements_by_xpath("//input[@type='text']")
    for i in range(len(elm)):
        el = elm[i].find_element_by_xpath('..')
        if '(Optional)' not in el.text and 'Listing Title' not in el.text:
            try:
                elm[i].send_keys('sample')
            except:
                print('ch')
            print('Text filled')
            time.sleep(1)


#Fill all number fields where is required
def numberFill():
    elm = driver.find_elements_by_xpath("//input[@type='number']")
    for i in range(len(elm)):
        el = elm[i].find_element_by_xpath('..')
        if '(Optional)' not in el.text and 'Price' not in el.text:
            elm[i].send_keys('2020')
            print('Number filled')
            time.sleep(1)


#Fill all textarea fields with text 'sample' where is required
def textAreaFill():
    elm = driver.find_elements_by_tag_name('textarea')
    for i in range(len(elm)):
        if '(Optional)' not in elm[i].get_property('placeholder'):
            elm[i].send_keys('sample')
            print('Textare filled')

#Clicking the button List Now and getting result
def submitAndGetResult(row):
    global counterSub
    global counter
    elm = driver.find_element_by_xpath("//button[@type='submit'][@role='submitButton'][contains(text(), 'List now')]")
    elm.submit()
    print('Submitting')
    time.sleep(10)
    try:
        em = driver.find_element_by_xpath("//p[contains(text(), 'Similar to your existing listing')]")
        sheet[f"AB{indexG}"] = 'Duplicate'
        return 'Similar'
    except:
        em = driver.find_element_by_xpath("//p[contains(text(), 'Successfully listed')]")
        listing_url = ''
        tmp = BeautifulSoup(driver.page_source, "lxml").find_all('a', href=True)
        for t in tmp:
            if t.span and 'View listing' in t.span.text:
                sheet[f"AB{indexG}"] = 'Listed'
                listing_url = 'https://www.carousell.sg' + t['href']
                sheet[f"AC{indexG}"] = listing_url
                break

        return 'Success'
    counterSub=0

    return 'Error'

#Filling title, condition, price, descp fields
def fillFromCsv(title, condition, price, descp):
    try:
        em = driver.find_element_by_xpath("//*[contains(text(), 'Listing Title')]")
        title_f = em.find_element_by_xpath("//input[@type='text']")
        title_f.send_keys(title)
    except:
        print('Title not filled')

    time.sleep(2)
    try:
        cond = driver.find_element_by_xpath("//*[contains(text(), '"+condition+"')]")
        cond.click()
    except:
        print('Condition not flled')

    time.sleep(2)
    try:
        pr = driver.find_elements_by_xpath("//input[@type='number'][@name='field_price']");
        pr[0].send_keys(price)
    except:
        print('Price not filled')
    time.sleep(2)
    try:
        desc = driver.find_element_by_xpath("//textarea[@placeholder='Describe what you are selling and include any details a buyer might be interested in. People love items with stories!']")
        desc.send_keys(descp)
    except:
        print('description not filled')
    print('Data from csv filled')

def downloadFile(photo):
    st = ''.join(random.choices(string.ascii_lowercase, k=5))
    URL = photo
    picture_req = requests.get(URL)
    if picture_req.status_code == 200:
        with open('data/'+st+".jpg", 'wb') as f:
            f.write(picture_req.content)
            return 'data/'+st+".jpg"
    return ''

def uploadPhoto(urls):
    photos = urls.split(";;;")
    for photo in photos:
        if(photo != ''):
            print(photo)
            elm = driver.find_element_by_xpath("//input[@type='file']")
            st = os.getcwd() + '/'+ downloadFile(photo)
            print(st)
            elm.send_keys(st)
            print("photo sended")
            time.sleep(1)


#Main function of proccess uploading item
def upload(category, title, condition, price, descp, photo, row):
    global counterRef
    uploadPhoto(photo)
    #Selecting category

    em = driver.find_elements_by_xpath("//*[contains(text(), 'Select a category')]")
    em[0].click()
    time.sleep(3)

    if(counterRef>3):
        submitLog(row,False)
        return 'Failed to upload ' + title;
    #Why I put (try,except)? because website have a bug, sometimes website is swithching to Chinesee language.
    #And if we refresh it, will gives back in English. So hear I put counter, to refresh three times.
    try:
        print(category.strip())
        em = driver.find_elements_by_xpath("//input")
        em[1].send_keys(category)
        time.sleep(5)
        em = driver.find_elements_by_xpath("//div[.//div[.//div[.//input]]]")
        em = em[6].find_elements_by_xpath(".//div[.//div[.//span]]")
        time.sleep(1)
        em[0].click()
        time.sleep(2)
        print("selected category")
        
    except: 
        traceback.print_exception(*sys.exc_info())
        print("error selected category")
        driver.get('https://www.carousell.sg/sell')
        upload(category, category_child, categorychild, title, condition, price, descp, photo,row)
        counterRef+=1

    counterRef = 0

    time.sleep(3)

    print("---select-fill")
    selectFill()
    print("---radio-fill")
    radioFill()
    print("--text-fill")
    #textFill()
    print("--number-fill")
    #numberFill()
    print("--number-fill")
    #numberFill()


    print("--checkbox-fill")
    #checkboxMailingFill()

    print("--selectBrand-fill")
    try:
        selectBrand()
    except:
        print('error brand')

    print("--typeD-fill")
    try:
        typeD()
    except:
        print('error typeD')

    print("--typeD-fill")
    try:
        ageRange()
    except:
        print('error ageRange')

    print("--dealMethod-fill")
    dealMethod()

    print("--csv-fill")


    fillFromCsv(title, condition, price, descp)
    return submitAndGetResult(row)

#Uploading cookie to authorize
def init(cook):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(url)
    try:
        em = driver.find_element_by_xpath("//button[contains(text(), 'Register')]")
        if(len(em)>=1):
            print('Needs to update cookie')
            return;
    except:
        print('Started')
    time.sleep(1)
    driver.get(url+'/sell')

def convertToStr(val):
    try:
        if(val!=None):
            return str(val)
    except:
        return ""
    return ""


#login = driver.find_elements_by_xpath("//*[contains(text(), 'Login')]")
#login[0].click()
#time.sleep(3)
#driver.find_element_by_name('username').send_keys("szetohonam2018")
#driver.find_element_by_name('password').send_keys("Fchi11747")
#el = driver.find_element_by_xpath("//button[@role = 'submitButton'][contains(text(), 'Log in')]");
#el.submit()
#time.sleep(50)
#driver.get("https://hk.carousell.com/sell")
#pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

#Here we sendig item values to function Upload, one by one
def main(args):
    global book
    global sheet
    global indexG
    print(args)
    print(args[0])
    init(str(args[0]))
    book = openpyxl.load_workbook(str(args[0]))
    sheet = book.active
    counter = 0
    for index in range(2, 100000000):
        indexG = index
        print(counter," next item ")
        if(sheet[f"D{index}"].value == None):
            break

        sheet[f"AD{index}"].value = now.strftime("%m/%d/%Y, %H:%M:%S")
        try:
            images = convertToStr(sheet[f"I{index}"].value) + ';;;' + convertToStr(sheet[f"J{index}"].value) + ';;;' + convertToStr(sheet[f"K{index}"].value) + ';;;'
            images += convertToStr(sheet[f"L{index}"].value) + ';;;' + convertToStr(sheet[f"M{index}"].value) + ';;;' + convertToStr(sheet[f"N{index}"].value)
            images += ';;;' + convertToStr(sheet[f"O{index}"].value)  + ';;;'+ convertToStr(sheet[f"P{index}"].value)

            category = sheet[f"AA{index}"].value
            title = convertToStr(sheet[f"D{index}"].value) + ' ' + convertToStr(sheet[f"E{index}"].value)
            condition = 'Brand new'
            price = sheet[f"F{index}"].value
            descp = convertToStr(sheet[f"G{index}"].value) + '\n' + convertToStr(sheet[f"H{index}"].value)
            roww = [category, title, condition, price, descp, images]
            print(roww)
            res = upload(category, title, condition, price, descp, images, roww)       
        except:
            sheet[f"AB{index}"] = 'Error'
            traceback.print_exception(*sys.exc_info())
           
        book.save(str(args[0]))
        super_get('https://www.carousell.sg/sell')

        counter+=1
     
    driver.close()




if __name__ == "__main__":
    main(sys.argv[1:])

