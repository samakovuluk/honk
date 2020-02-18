from selenium import webdriver
import csv
import time
import pickle
import random
import sys
from datetime import datetime


url = 'https://hk.carousell.com'

driver = webdriver.Chrome('chromedriver.exe')

driver.get(url)

counterRef = 0
counterSub = 0
counterFill = 0

driver.get('https://hk.carousell.com/sell')
driver.execute_script('window.localStorage.clear();')
time.sleep(1)


#Writing result in LogFile, getting two parameters list and boolean.
#list which is containg values of item, and boolean result of uploaded item
def submitLog(row, b):
    logs = open('log.txt','a+')
    for i in row:
        logs.write(i)
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
    counterFill = 0
    driver.execute_script('window.localStorage.clear();')
    driver.refresh();
    try:
        driver.switch_to_alert().accept()
    except:
        print('Hard Refresh')
    driver.get(url)

#Selecting all selectable fields randomly
def selectFill():
    elm = driver.find_elements_by_xpath("//div[@role='dropdown']")
    for i in range(1,len(elm)):
        #Hear we checking is the field is optional or not, if not so we selecting
        if '(Optional)' not in elm[i].text:
            elm[i].click()
            time.sleep(2)
            p = elm[i].find_element_by_xpath('parent::*')
            elem = p.find_elements_by_class_name('_1H4f-PmiEr')
            if len(elem)>0:
                elem[random.randint(0,len(elem)-1)].click()
                print('Dropdown selected')
                time.sleep(1)

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
            elm[i].send_keys('sample')
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
    elm = driver.find_element_by_xpath("//button[@type='submit'][@role='submitButton'][contains(text(), 'List now')]")
    elm.submit()
    print('Submitting')
    time.sleep(5)
    try:
        res = driver.find_element_by_class_name('_2_WIPmzf97')
    except:
        counter+=1
        if(counter>3):
            submitLog(row,False)
            return
        else:
            submitAndGetResult(row)
    counterSub=0
    res = res.text

    if 'Successfully listed' in res:
        submitLog(row,True)
    else:
        submitLog(row,False)

    return res

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
        pr = driver.find_elements_by_xpath("//input[@type='number']");
        for i in range(len(pr)):
            if 'Price' in pr[i].find_element_by_xpath('..').text:
                    print(pr[i].find_element_by_xpath('..').text)
                    pr[i].send_keys(price)
    except:
        print('Price not filled')

    time.sleep(2)

    try:
        desc = driver.find_element_by_xpath("//*[contains(text(), 'description')]").find_element_by_xpath('..')
        desc = desc.find_element_by_tag_name('textarea')
        desc.send_keys(descp)
    except:
        print('description not filled')

    print('Data from csv filled')


#Main function of proccess uploading item
def upload(category, category_child, categorychild, title, condition, price, descp, photo, row):
    global counterRef
    elm = driver.find_element_by_xpath("//input[@type='file']")
    elm.send_keys(photo)
    print("photo sended")
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
        em = driver.find_elements_by_xpath("//*[contains(text(), \""+category+"\")]")
        em[0].click()
        print("selected category")
    except:
        driver.get('https://hk.carousell.com/sell')
        upload(category, category_child, categorychild, title, condition, price, descp, photo,row)
        counterRef+=1

    counterRef = 0

    try:
        if category_child!='':
            time.sleep(3)
            em = driver.find_elements_by_xpath("//*[contains(text(), \""+category_child+"\")]")
            em[0].click()
            print("selected category child")
    except:
        print('no category child')

    time.sleep(3)
    try:
        if categorychild!='':
            em = driver.find_elements_by_xpath("//*[contains(text(), \""+categorychild+"\")]")
            em[0].click()
            print("selected c category child ",categorychild)
    except:
        print('not third category')

    time.sleep(3)


    selectFill()
    radioFill()
    textFill()
    numberFill()
    checkboxMailingFill()
    fillFromCsv(title, condition, price, descp)
    return submitAndGetResult(row)

#Uploading cookie to authorize
def init(cook):
    cookies = pickle.load(open(cook, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(url)
    try:
        em = driver.find_element_by_xpath("//button[contains(text(), 'New User? Register')]")
        if(len(em)>=1):
            print('Needs to update cookie')
            return;
    except:
        print('Started')
    time.sleep(1)
    em = driver.find_element_by_class_name('_3j4GRV18q8')
    ep = em.find_element_by_xpath("//option[contains(text(), 'English')]")
    em.click()
    time.sleep(1)
    ep.click()
    driver.get(url+'/sell')



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
    init(str(args[1]))

    with open(str(args[0]), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if("price" not in row):
               try:
                   upload(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row)
               except:
                   submitLog(row,False)

               super_get('https://hk.carousell.com/sell')

    driver.quit()




if __name__ == "__main__":
    main(sys.argv[1:])
