import chromedriver_binary
import selenium
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
# options.add_argument('window-size=1200x600')
browser = webdriver.Chrome(options=options)
browser.get('http://google.com/')
browser.quit()


"""


## optionsに"headless"modeを指定しないといろいろエラーが起こる

必ず指定すること


"""