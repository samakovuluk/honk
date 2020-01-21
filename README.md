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

## How it works

#### Problem
We need an automated script which will upload item independently.
#### Solution
Project working with library Selenium. As we know Selenium is s a free (open source) automated testing suite for web applications. And this tool I used for uploading items to hk.carousell.com. Selenium is perfect decision for our task. 
So script doing step by step tasks: 
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



   
    

