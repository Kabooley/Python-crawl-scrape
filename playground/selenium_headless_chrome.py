import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()


options.add_argument('headless')
# set the window size
options.add_argument('window-size=1200x600')

# initialize the driver
driver = webdriver.Chrome(options=options)

# Googleのトップ画面を開く。
driver.get('https://www.google.co.jp/')

# タイトルに'Google'が含まれていることを確認する。
assert 'Google' in driver.title

# 検索語を入力して送信する。
input_element = driver.find_element_by_name('q')
input_element.send_keys('Python')
input_element.send_keys(Keys.RETURN)

# タイトルに'Python'が含まれていることを確認する。
assert 'Python' in driver.title

# スクリーンショットを撮る。
driver.save_screenshot('search_results.png')

# 検索結果を表示する。
for h3 in driver.find_elements_by_css_selector('a > h3'):
    a = h3.find_element_by_xpath('..')  # h3の親要素を取得。
    print(h3.text)
    print(a.get_attribute('href'))

driver.quit()  # ブラウザーを終了する。