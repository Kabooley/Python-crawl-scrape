"""
超a&g+番組表のHTMLをちょっとだけいじるだけのファイル
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import datetime
import json
import os

URL = "https://www.joqr.co.jp/qr/agregularprogram/"
Selector = "span.personality"
HTML_FILE_NAME = "regular-program.html"


# main
def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get(URL)

    assert "レギュラー番組表" in browser.title

    try:
        # 指定した要素がDOM上に現れるまで待機する 要素が現れない場合、例外が投げられる
        element = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, Selector))
        )

        # 一度だけHTML保存。ローカルに指定のファイルが保存されていなければ保存処理
        # if not os.path.exists("./regular-program.html"):
            # saveHTML(browser.page_source.encode('utf-8'))
        souping(browser.page_source.encode('utf-8'))
    finally:
        browser.quit()


# HTMlファイルをローカルに保存する
def saveHTML(html: str):
    with open('regular-program.html', 'w', encoding='utf-8') as f:
        f.write(html)


# この中身をいじること
def souping(html: str):
    soup = BeautifulSoup(html, features="html.parser")
    table_body = soup.find("table").find("tbody")
    if table_body is None:
        print('Error: table body is not exist or not found')
        return
    
    # [`td.is-joqr`が取得できない件] こっちでは取得できるけれど
    # result = table_body.find_all('td', class_="is-joqr")
    # print(result)
    
    for tr in table_body.find_all("tr"):
        # <tr>内の<td>すべてを取得する
        td_all = tr.find_all("td")
        # 空の<tr>無視
        if (td_all is None) or (len(td_all) == 0):
            continue
        for i in range(len(td_all)):
            td = td_all[i]
            scrapeTd(soup, td)



def scrapeTd(soup: BeautifulSoup, td: str):
    print("-- scrapeTd() ---------------")
    print(td)
    # [`td.is-joqr`が取得できない件] こっちでは取得できない
    # result = td.find(class_="is-joqr")
    # もしかしたらtdは自身(td要素自身)を取得できないのかもしれない
    # お試し...結果全てにおいてNoneであった...
    # result2 = td.find('td')
    # tdを文字列として扱ってみてもダメ
    # print("is-joqr" in td)
    # print(result2)

    # 結果この方法が正しいとわかった
    # .findや.selectではtd自身を取得できないが、td自身を取得するには.getを使うといいらしい！
    # .findや.selectと、.get()の違いはそこにあるらしい
    classList = td.get("class")
    isSuspension = True if "is-joqr" in classList else False
    print(isSuspension) 
    


main()

"""

- 条件分岐
放送休止だと...
出演者がいない


"""