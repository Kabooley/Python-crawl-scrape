from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def main():
    browser = getChromeWebDriver()



def writeHtml(driver: Remote):
    # driver.page_source: str
    soup = BeautifulSoup(driver.page_source.encode('utf-8'), features="html.parser")
    table_body = soup.find("table").find("tbody")
    if table_body is None:
        print('Error: table body is not exist or not found')
        return
    file = open("table.html", "w")
    file.write(table_body)
    file.close()

def getChromeWebDriver() -> webdriver.chrome.webdriver.WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get("https://www.joqr.co.jp/qr/agregularprogram/")

    assert "レギュラー番組表" in browser.title

    try:
        # 指定した要素がDOM上に現れるまで待機する 要素が現れない場合、例外が投げられる
        # TypeError: find_element() takes from 1 to 3 positional arguments but 13 were given
        element = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.personality"))
        )
        print(type(browser))
        return browser
    finally:
        browser.quit()


main()