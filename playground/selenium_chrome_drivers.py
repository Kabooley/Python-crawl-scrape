"""
from selenium import webdriver

上記のインポートで以下にアクセスできる

webdriver.Firefox
webdriver.FirefoxProfile
webdriver.Chrome
webdriver.ChromeOptions
webdriver.Ie
webdriver.Opera
webdriver.PhantomJS
webdriver.Remote
webdriver.DesiredCapabilities
webdriver.ActionChains
webdriver.TouchActions
webdriver.Proxy


https://www.joqr.co.jp/qr/agregularprogram/
"""
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(options)

driver.get('https://www.joqr.co.jp/qr/agregularprogram/')

