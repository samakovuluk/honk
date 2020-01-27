# Honk

Here the project for uploading items to platform hk.carousell.com

#### Requirements for script
* Install python, which version greater 3, with adding Windows path https://datatofish.com/add-python-to-windows-path/
* Library Selenium, to install just open cmd and type `pip install selenium`

#### Instruction to start script
* You need authorize
  * Run the script `savecook.py` and authorize.
  * script will open website hk.carousell.com, you need log in and pass verification test of human, after successfully authorization it will automatically close.
* Fill your items in csv file, for sample you can see file `sample.csv`
  * there fieds: category_parent, category, category_child, title, condition(Used,New), Price, Description, Photo
* Open `honk.py` via notepad or IDLE, in line 12 `driver = webdriver.Chrome('path')` instead of `path`, put location of `chromedriver.exe` [screen](Screenshot_3.png)
  * Example my is `driver = webdriver.Chrome('D:/Chromedriver_win32/chromedriver.exe')`
* And Finally, run main script `honk.py` by giving path of csv file. 
  * Open your cmd in location of script, and type `python honk.py sample.csv` [screen](Screenshot_2.png)
  
#### Login with other account

* Run script `savecook.py`. It will open website hk.carousell.com
   * Type your login and password
   * Pass verification test of human
And it will automatically closed when you sucessfully authorized

# How it works

#### Problem
We need an automated script which will upload item independently.
#### Solution
Project working with library Selenium. As we know Selenium is s a free (open source) automated testing suite for web applications. And this tool I used for uploading items to hk.carousell.com. Selenium is perfect decision for our task. 
So script doing step by step tasks. 
#### What you need to know about Selenium
Selenium able to do what the user can does on the site. Only needs to be configured correctly. 
How is everything going. So for example we have task, that script need open website facebook.com click to button `sign up` with name `websubmit`.
```
   import selenium
   driver = webdriver.Chrome('chromedriver.exe')
   driver.get('https://www.facebook.com/')
   el = driver.find_element_by_name('websubmit')
   el.click()
```
###### Attention do not forget to put full path of chromedriver.exe in `driver = webdriver.Chrome('{path}')`
As you see we found element by name and click, so you wanna ask how to get name of button. It is easy just open the website facebook.com,
and in the button `sign up` click right mouse, and there will be option `Inspect code` and select this. After you will able to see source  (html), in the right side. There will shaded [code](https://github.com/samakovuluk/honk/blob/master/Screenshot_8.png) wchich is source of button. In the shaded source will be parameter `name=websubmit`, so we now know that name of the button is `websubmit`.

So in selenium there a lot of options to find elements, you can find elements by functions :
`find_element_by_css' 
'find_element_by_class_name'
'find_element_by_xpath'.

You can learn more about selenium [here](https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test)

### Actions in the script
Here main actions of the script, in source you can see code implemetation of action.
* Init actions
    * Open url hk.carousell.com [source](https://github.com/samakovuluk/honk/blob/d6d942f5d803d3d897fdcefec7bc08bdd9e0b302/honk.py#L20)
    * Uploading cookie [source](https://github.com/samakovuluk/honk/blob/d6d942f5d803d3d897fdcefec7bc08bdd9e0b302/honk.py#L254)
    * Select language English [source](https://github.com/samakovuluk/honk/blob/d6d942f5d803d3d897fdcefec7bc08bdd9e0b302/honk.py#L265)
    * Open url hk.carousell.com/sell
* Uploading items one by one
    * Open csv file where items [source](https://github.com/samakovuluk/honk/blob/d6d942f5d803d3d897fdcefec7bc08bdd9e0b302/honk.py#L195)
    * Get photo value from csv and upload photo [source](https://github.com/samakovuluk/honk/blob/d6d942f5d803d3d897fdcefec7bc08bdd9e0b302/honk.py#L197)
    * Choose category and category child [source](https://github.com/samakovuluk/honk/blob/d6d942f5d803d3d897fdcefec7bc08bdd9e0b302/honk.py#L211)
    * Choose randomly and Put text in fields where is required [source](https://github.com/samakovuluk/honk/blob/d6d942f5d803d3d897fdcefec7bc08bdd9e0b302/honk.py#L55)
    * Fill items fields (title, price, condition, description) [source](https://github.com/samakovuluk/honk/blob/d6d942f5d803d3d897fdcefec7bc08bdd9e0b302/honk.py#L155)
    * Submit [source](https://github.com/samakovuluk/honk/blob/d6d942f5d803d3d897fdcefec7bc08bdd9e0b302/honk.py#L129)
    * Wait 5 seconds
    * Write result in log file [source](https://github.com/samakovuluk/honk/blob/d6d942f5d803d3d897fdcefec7bc08bdd9e0b302/honk.py#L27)
    * Upload next item

The project works very simply, there we getting elements by function `find_element_by_xpath` in xpath function we can indicate conditions for finding elements. Example we want get input checkbox with value mailing so we writing `elm = driver.find_element_by_xpath("//input[@type='checkbox'][@value='mailing']")`.  Now variable `elm` equal to checkbox element, so for click it just write `elm.click()`. Here is how our project works on most parts. 

So let's see one of action in project. We will take action which selecting randomly in dropdown fileds.

```
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
```

Here we finding dropdown fields by xpath function `find_elements_by_xpath("//div[@role='dropdown']")` we go through elements. And each element we checking for required or not, `if '(Optional)' not in elm[i].text:` if text of element not contains text `(optional)` so we click `elm[i].click()` .

 




   
    

