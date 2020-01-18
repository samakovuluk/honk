# Honk

Here the project for uploading items to platform hk.carousell.com

### Requirements for script
* Install python, which version greater 3, with adding Windows path https://datatofish.com/add-python-to-windows-path/
* Library Selenium, to install just open cmd and type `pip install selenium`

### Instruction to start script
* You need authorize
  * Run the script `savecook.py` and authorize.
  * script will open website hk.carousell.com, you need log in and pass verification of human, after successfully authorization it automatically close.
* Fill your items in csv file, for sample you can see file `sample.csv`
  * there fieds: category_parent, category, category_child, title, condition(Used,New), Price, Description, Photo
* Open `honk.py` via notepad or IDLE, in line 12 `driver = webdriver.Chrome('path')` instead of path set location of `chromedriver.exe` [screen](Screenshot_3.png)
  * Example my is `driver = webdriver.Chrome('D:/Chromedriver_win32/chromedriver.exe')`
* And Finally, run main script `honk.py` by giving path of csv file. 
  * Open your cmd in location of script, and type `python honk.py sample.csv` [screen](Screenshot_2.png)
  






