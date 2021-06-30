"""
超a&g+の番組表ページから番組情報を取得してJSONファイルに保存する

- コマンドライン
    "o-json": 必須。出力するJSONファイルのファイル名
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from cerberus import Validator
import requests
import datetime
import json
import sys

GLOBALS = {
    "URL": "https://www.joqr.co.jp/qr/agregularprogram/",
    "output_json": "",
    "selector": "span.personality"
}
Selector = "span.personality"

# Validations for command line
schema = {
    # 出力するcreate_table.jsonのファイル名をコマンドラインで取得するため
    "json": {
        'type': 'string',
        'required': True,
        'regex': r"^[\w,\s-]+\.json"
    }
}



def commandline_validator(args) -> bool:
    cmnd_validator = Validator(schema)
    if len(args) > 1:
        result = cmnd_validator.validate({"json": args[1]})
        if not result: 
            print("Error: Command line Validation: ", cmnd_validator.errors)
        return result
    else:
        return False

# スクレイピングでどうにかする
def main():
    args = sys.argv
    if not commandline_validator(args):
        return
    else:
        GLOBALS["output_json"] = args[1]

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get(GLOBALS["URL"])

    assert "レギュラー番組表" in browser.title

    try:
        # 指定した要素がDOM上に現れるまで待機する 要素が現れない場合、例外が投げられる
        # TypeError: find_element() takes from 1 to 3 positional arguments but 13 were given
        element = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, GLOBALS["selector"]))
        )
        # 問題なければBeautifulSoup4でHTMLを取得しよう
        create_json(browser)
    finally:
        browser.quit()





def create_json(driver: Remote) -> str:
    # driver.page_source: str
    soup = BeautifulSoup(driver.page_source.encode('utf-8'), features="html.parser")
    table_body = soup.find("table").find("tbody")
    if table_body is None:
        print('Error: table body is not exist or not found')
        return
    new_table = create_table(table_body)
    f = open(GLOBALS["output_json"], "w", encoding="utf-8")
    json.dump(new_table, f, ensure_ascii=False)
    f.close()


# Qiitaのあれに修正を加えている
def create_table(table):
    # 月曜の日付（基準）を取得する
    today = datetime.date.today()
    monday = (today - datetime.timedelta(days=today.weekday())).strftime("%Y%m%d")
    # 切り替えの基準を作る
    # criterion は 6:00 の時間データである
    # 6:00であるのは、超a&g+が朝6時から放送開始するから
    criterion = datetime.datetime.strptime("06:00", "%H:%M")
    # 曜日ごとの「終了時間」を更新するためのリスト
    end_times = [datetime.datetime.strptime("06:00", "%H:%M")] * 7
    main_data = []
    main_data2 = []
    for i in range(7):
        main_data.append([])
        main_data2.append([])
    for tr in table.find_all("tr"):
        # <tr>内の<td>すべてを取得する
        td_all = tr.find_all("td")
        # 空の<tr>無視
        if (td_all is None) or (len(td_all) == 0):
            continue
        for i in range(len(td_all)):
            td = td_all[i]

            # -- 番組開始時間取得パート ----------

            # print(td)
            # time が24時を超えた場合のアレ
            # 
            # AttributeError :'NoneType' object has no attribute 'text'
            # prints : <div class="weeklyProgram-time">6:00</div>
            # find()はbs4のメソッドであった...
            # time_str = "600"
            time_str = td.find(class_="weeklyProgram-time").text.replace("\n", "", 3).replace(" 頃", "").split(":")
            # もしも6 >= 24 なら
            if int(time_str[0]) >= 24:
                time_str[0] = format(int(time_str[0]) - 24,  "02")
            time_str = time_str[0] + time_str[1]
            # datetime にする
            tmp_dt = datetime.datetime.strptime(time_str, "%H%M")

            # datetimeに直した日時
            # print(tmp_dt)

            # iやi2はイテレータであり曜日を意味する
            i2 = i
            while(i2<7):
                classes = td.get('class')
                # もしも`colspan`が`None`じゃなくて数値を返す場合、その番組は番組表の複数日にまたがって表示されている

                # 番組名 
                if "is-joqr" in classes:
                    title = "放送休止"
                    pfm = ""
                    isRepeat = False
                    isMovie = False
                    isBroadcast = False
                # 6/29追記：もう一段挟む必要がある。「新番組」で未定が発生するような場合
                # "div.weeklyProgram-content"以下にアンカー要素が一つもないこと
                elif td.select("div.weeklyProgram-content")[0].find_all('a') == []:
                    print('未定')
                    title = "pending-space"
                    pfm = ""
                    isRepeat = False
                    isMovie = False
                    isBroadcast = False
                else:
                    title = td.select("div.weeklyProgram-content a")[0].text.replace("\n", "", 3)
                    # print(title)
                    # 出演者取得
                    # 出演者が複数の場合に対応していない
                    if td.select("span.personality a") :
                        pfm = td.select("span.personality a")[0].text.replace("\n", "", 4)
                    else :
                        pfm = "なし"
                    # print(pfm)

                    # 再放送か
                    isRepeat = True if "is-repeat" in classes else False
                    # 動画か
                    isMovie = True if td.select('i.icon_program-movie') else False
                    # 生放送か
                    isBroadcast = True if td.select('i.icon_program-live') else False
                    
                # end_time が1900/1/2になったら分岐する
                # >>part-1<<
                if tmp_dt < criterion:
                    tmp_dt2 = tmp_dt + datetime.timedelta(days=1)
                    new_i = (i2 + 1) % 7
                    # >>part-2<<
                    if tmp_dt2 == end_times[new_i]:
                        # colspanが設定されていると、曜日をまたいで同じ番組が組み込まれている
                        if td.has_attr('colspan'):
                            multiple_days = int(td.get('colspan'))
                            min = int(td.get("rowspan"))
                            ft = datetime.datetime.strptime(monday + time_str, "%Y%m%d%H%M") + datetime.timedelta(days=new_i)
                            to = ft + datetime.timedelta(minutes=int(td.get("rowspan")))
                            new_data = {
                                "title": title,
                                "ft": ft.strftime("%Y%m%d%H%M"),
                                "to": to.strftime("%Y%m%d%H%M"),
                                "pfm": pfm,
                                "isBroadcast": isBroadcast,
                                "isMovie": isMovie
                            }
                            for itr in range(new_i, multiple_days):
                                end_times[itr] += datetime.timedelta(minutes=min)
                                if isBroadcast:
                                    new_data["isRepeat"] = isRepeat
                                else:
                                    new_data["isRepeat"] = True
                                main_data[itr].append(new_data)

                        # endtime を更新
                        # `rowspan`はtd要素の属性値で番組の長さをそのまま表している
                        # `rowspan = 60`で60分番組
                        # >>part-3<<
                        else:
                            # end_timesの更新
                            end_times[new_i] += datetime.timedelta(minutes=int(td.get("rowspan")))
                            ft = datetime.datetime.strptime(monday + time_str, "%Y%m%d%H%M") + datetime.timedelta(days=new_i)
                            to = ft + datetime.timedelta(minutes=int(td.get("rowspan")))
                            new_data = {
                                "title": title,
                                "ft": ft.strftime("%Y%m%d%H%M"),
                                "to": to.strftime("%Y%m%d%H%M"),
                                "pfm": pfm,
                                "isBroadcast": isBroadcast,
                                "isMovie": isMovie,
                            }
                            if isBroadcast:
                                new_data["isRepeat"] = isRepeat
                            else:
                                new_data["isRepeat"] = True
                            main_data[new_i].append(new_data)
                        break
                # if tmp_dt < criterion:
                #     tmp_dt2 = tmp_dt + datetime.timedelta(days=1)
                #     new_i = (i2 + 1) % 7
                #     if tmp_dt2 == end_times[new_i]:
                #         # endtime を更新
                #         # `rowspan`はtd要素の属性値で番組の長さをそのまま表している
                #         # `rowspan = 60`で60分番組

                #         # end_timesの更新
                #         end_times[new_i] += datetime.timedelta(minutes=int(td.get("rowspan")))
                #         ft = datetime.datetime.strptime(monday + time_str, "%Y%m%d%H%M") + datetime.timedelta(days=new_i)
                #         to = ft + datetime.timedelta(minutes=int(td.get("rowspan")))
                #         new_data = {
                #             "title": title,
                #             "ft": ft.strftime("%Y%m%d%H%M"),
                #             "to": to.strftime("%Y%m%d%H%M"),
                #             "pfm": pfm,
                #             "isBroadcast": isBroadcast,
                #             "isMovie": isMovie,
                #         }
                #         if isBroadcast:
                #             new_data["isRepeat"] = isRepeat
                #         else:
                #             new_data["isRepeat"] = True
                #         main_data[new_i].append(new_data)
                #         break

                # 日付をまたがない分(以下のelseｽｺｰﾌﾟ)は正しく取得できる
                # >>part-4<<
                else:
                    # >>part-5<<
                    if tmp_dt == end_times[i2]:
                        # colspanが設定されていると、曜日をまたいで同じ番組が組み込まれている
                        if td.has_attr('colspan'):
                            # colspanの数値分だけi2とまたいでいる曜日の終了時間を更新する必要がある
                            # ここでその処理を行ってしまうと、他の処理が面倒になるから終了時間だけ更新すれば「あとから挿入」で済むかしら？
                            multiple_days = int(td.get('colspan'))
                            min = int(td.get("rowspan"))
                            # ft = datetime.datetime.strptime(monday + time_str, "%Y%m%d%H%M") + datetime.timedelta(days=i2)
                            # to = ft + datetime.timedelta(minutes=int(td.get("rowspan")))
                            # new_data = {
                            #     "title": title,
                            #     "ft": ft.strftime("%Y%m%d%H%M"),
                            #     "to": to.strftime("%Y%m%d%H%M"),
                            #     "pfm": pfm,
                            #     "isBroadcast": isBroadcast,
                            #     "isMovie": isMovie
                            # }
                            # またがっている曜日分、end_timesを更新する
                            for itr in range(i2, multiple_days):
                                end_times[itr] += datetime.timedelta(days= (itr - i2), minutes=min)

                                min = int(td.get("rowspan"))
                                ft = datetime.datetime.strptime(monday + time_str, "%Y%m%d%H%M") + datetime.timedelta(days=itr)
                                to = ft + datetime.timedelta(minutes=int(td.get("rowspan")))
                                new_data = {
                                    "title": title,
                                    "ft": ft.strftime("%Y%m%d%H%M"),
                                    "to": to.strftime("%Y%m%d%H%M"),
                                    "pfm": pfm,
                                    "isBroadcast": isBroadcast,
                                    "isMovie": isMovie
                                }
                                if isBroadcast:
                                    new_data["isRepeat"] = isRepeat
                                else:
                                    new_data["isRepeat"] = True
                                main_data2[itr].append(new_data)
                        # >>part-6<<
                        else:
                            end_times[i2] += datetime.timedelta(minutes=int(td.get("rowspan")))
                            ft = datetime.datetime.strptime(monday + time_str, "%Y%m%d%H%M") + datetime.timedelta(days=i2)
                            to = ft + datetime.timedelta(minutes=int(td.get("rowspan")))
                            new_data = {
                                "title": title,
                                "ft": ft.strftime("%Y%m%d%H%M"),
                                "to": to.strftime("%Y%m%d%H%M"),
                                "pfm": pfm,
                                "isBroadcast": isBroadcast,
                                "isMovie": isMovie
                            }
                            if isBroadcast:
                                new_data["isRepeat"] = isRepeat
                            else:
                                new_data["isRepeat"] = True
                            main_data2[i2].append(new_data)
                        # ft = datetime.datetime.strptime(monday + time_str, "%Y%m%d%H%M") + datetime.timedelta(days=i2)
                        # to = ft + datetime.timedelta(minutes=int(td.get("rowspan")))
                        # new_data = {
                        #     "title": title,
                        #     "ft": ft.strftime("%Y%m%d%H%M"),
                        #     "to": to.strftime("%Y%m%d%H%M"),
                        #     "pfm": pfm,
                        #     "isBroadcast": isBroadcast,
                        #     "isMovie": isMovie
                        # }
                        # if isBroadcast:
                        #     new_data["isRepeat"] = isRepeat
                        # else:
                        #     new_data["isRepeat"] = True
                        # main_data2[i2].append(new_data)
                        break
                i2 += 1
    for i in range(7):
        main_data[i].extend(main_data2[i])
    return main_data




main()


"""
番組表URL: https://www.joqr.co.jp/qr/agregularprogram/


WebDriver API: https://kurozumi.github.io/selenium-python/api.html
逆引きAPI: https://www.seleniumqref.com/api/webdriver_gyaku.html

## 要素取得に関して

puppeteerみたいに操作できるかはまだ不明
要素が見つからない場合例外が発生する("NoSuchEelementException")


BeautifulSoup4でHTMLを取得してからそれをいじるのもいいけれど
HTMLがロードされてからJavaScriptでHTMLが走査されている可能性は充分ある
ということでHTMLがロードされてから、「しばらくたったら」HTMLを取得する

実際に取得できたかどうかを比べてみよう
(BeautifulSoup4でも)


## selenium.webdriver.common.by.By

(By.CLASS_NAME, "form.submit-forms")で"form.submit-forms"というcss_selectorの指定

別にfind_element_by_css_selectorであればBy要らないんだけどね


## 人気なライブラリとかのおさらい

bs4: htmlファイルから要素を探したりとか。静的HTMLファイル向け


## 番組内容のJSONファイル

どういう番組情報が欲しいのか
番組名
パーソナリティ
(あるか？)ゲスト
何曜日何時何分から配信開始なのか
(ffmepgでm3u8ファイルを取得するけれど、m3u8のURLが切り替わるタイミングをばっちり反映してほしい)
何時何分に配信終了なのか
初回放送か再放送か


ゲストがどうかの情報は取得できないしツイッターのリンクとかもない

{
    "Monday": [
        "番組開始時間": {
            番組内容
        },
        "番組開始時間": {
            番組内容
        },
        ...
    ],
    "Tuesday": [

    ]
}
"""
"""
#メソッドメモ

## str.find(sub[, start[, end]])

文字列のスライスに部分文字列subが含まれる場合、
その最小のインデックスを返す
find()メソッドはsubの位置を知りたいときにのみ使うべきである


## datetime

親クラス: datetime 

datetime.datetimeオブジェクトはdatetime.dateオブジェクトおよびdatetime.timeオブジェクトのすべてが入っているオブジェクトだそうです

```Python
# 2021-06-23
datetime.date.today()
# 2021-06-23 19:54:28.772180
datetime.datetime.now()
# 2021-06-23 19:54:28.772180
datetime.datetime.today()

```

```Python
    # 2021-06-23
    today = datetime.date.today()
    # 基準時間: '20210621'
    monday = (today - datetime.timedelta(days=today.weekday())).strftime("%Y%m%d")
    # datetime.datetime(1900, 1, 1, 6, 0)
    criterion = datetime.datetime.strptime("06:00", "%H:%M")
    # [datetime.datetime(1900, 1, 1, 6, 0), datetime.datetime(1900, 1, 1, 6, 0), datetime.datetime(1900, 1, 1, 6, 0), datetime.datetime(1900, 1, 1, 6, 0), datetime.datetime(1900, 1, 1, 6, 0), datetime.datetime(1900, 1, 1, 6, 0), datetime.datetime(1900, 1, 1, 6, 0)]
    end_times = [datetime.datetime.strptime("06:00", "%H:%M")] * 7

    # time_strの値をdatetimeオブジェクトにする
    tmp_dt = datetime.datetime.strptime(time_str, "%H%M")


    # datetime.datetime(1900, 1, 1, 6, 0) < datetime.datetime(1900, 1, 1, 6, 0)の比較
    if tmp_dt < criterion:

```
`if tmp_dt < criterion:`の比較は実際には何を比較しているのか
datetime.datetime(year, month, date, hour, minute, second, tzinfo, fold)
引数で構成される時間の比較をしている
つまり
```Python
>>> datetime.datetime(1900, 1, 1, 6, 0) > datetime.datetime(1900, 1, 1, 5, 0)
True
>>> datetime.datetime(1900, 1, 1, 6, 0) > datetime.datetime(1900, 1, 1, 7, 0)
False
```



6/29:
ag.pyの現状確認できる問題
1. 
2. colspanがある番組の組み込みをどうやって実装するべきか
5. パーソナリティ複数名でも一人しか取得できていない
6. 初回放送なのにリピート放送扱いになっている
7. 同じ枠に2番組以上はいる奴は取得できていない件


"""