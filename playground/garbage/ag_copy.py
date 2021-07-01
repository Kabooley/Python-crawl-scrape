"""
超a&g+の番組表ページから番組情報を取得してJSONファイルに保存する

7/1:
このファイルは一時的なコピーファイルだよ
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
        element = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, GLOBALS["selector"]))
        )
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

            # -- 番組開始時間取得パート tmp_dtは開始時間を表す時間データ----------
            time_str = td.find(class_="weeklyProgram-time").text.replace("\n", "", 3).replace(" 頃", "").split(":")
            # もしも6 >= 24 なら
            if int(time_str[0]) >= 24:
                time_str[0] = format(int(time_str[0]) - 24,  "02")
            time_str = time_str[0] + time_str[1]
            # datetime にする
            tmp_dt = datetime.datetime.strptime(time_str, "%H%M")

            # iやi2はイテレータであり曜日を意味する
            i2 = i
            while(i2<7):
                classes = td.get('class')
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
                    
                # -- main_dataへ番組情報dictを挿入していくパート ------------------
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


def updated_create_table(table):
    # 月曜の日付（基準）を取得する
    today = datetime.date.today()
    monday = (today - datetime.timedelta(days=today.weekday())).strftime("%Y%m%d")
    # 切替基準時間: 6:00になるはず
    criterion = datetime.datetime.strptime("06:00", "%H:%M")
    # 曜日ごとの「終了時間」を更新するためのリスト
    end_times = [datetime.datetime.strptime("06:00", "%H:%M")] * 7
    # 日付がかわってから基準時間までの番組を挿入するためのリスト
    main_data = []
    # 基準時間から日付が変わるまでの間の番組を挿入するためのリスト
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
        # itrは0~6をループするはず
        for itr in range(len(td_all)):
            td = td_all[itr]

            # 
            # -- 番組開始時間取得パート-------- 
            # 
            # tmp_dtは開始時間を表す時間データ
            time_str = td.find(class_="weeklyProgram-time").text.replace("\n", "", 3).replace(" 頃", "").split(":")
            # もしも6 >= 24 なら
            if int(time_str[0]) >= 24:
                time_str[0] = format(int(time_str[0]) - 24,  "02")
            time_str = time_str[0] + time_str[1]
            # datetime にする
            tmp_dt = datetime.datetime.strptime(time_str, "%H%M")




            iterator2 = itr
            while(iterator2 < 7):
                # 
                # -- 番組情報取得パート -------
                # 
                # 放送休止枠なのかチェックする
                # 複数曜日にまたがっているので要修正
                if "放送休止" in td.find("div", class_="weeklyProgram-content").stripped_strings:
                    title = "放送休止枠"
                    pfm = ""
                    isRepeat = False
                    isMovie = False
                    isBroadcast = False
                # 新番組枠かチェックする
                elif "新番組" in td.find("div", class_="weeklyProgram-content").stripped_strings:
                    title = "未定枠"
                    pfm = ""
                    isRepeat = False
                    isMovie = False
                    isBroadcast = False
                # 取得要素以下はテキスト以外を含むのかチェックする
                elif not td.find("div", class_="weeklyProgram-content").string:
                    title = td.select("div.weeklyProgram-content a")[0].text.replace("\n", "", 3)
                    pfm = td.select("span.personality a")[0].text.replace("\n", "", 4) if td.select("span.personality a") else "None"
                    isRepeat = True if "is-repeat" in td.get('class') else False
                    isMovie = True if td.select('i.icon_program-movie') else False
                    isBroadcast = True if td.select('i.icon_program-live') else False
                
                if td.has_attr('colspan'):
                    print('colspan is set')
                    # ここにcolspanでセットされている値の回数だけ、時間更新パートをじっこうすればいいかも
                    # ただしend_timesの更新方法に注意
                else:
                    print('no colspan')
                    # 同様。ただしループの必要がない
                # 
                # -- 時間更新パート -----
                # 
                # 24:00~6:00までの番組はmain_dataへ突っ込む
                # 6:00~24:00まので番組はmain_data2へ突っ込む
                # 
                # 
                # end_time が1900/1/2になったら分岐する
                if tmp_dt < criterion:
                    tmp_dt2 = tmp_dt + datetime.timedelta(days=1)
                    # new_iは1~7の数値を繰り返す
                    # (itrとiterator2はインクリメントしていくだけだから)
                    new_i = (iterator2 + 1) % 7
                    if tmp_dt2 == end_times[new_i]:
                        # endtime を更新 「分」だけ更新する。日付は更新しない。
                        end_times[new_i] += datetime.timedelta(minutes=int(td.get("rowspan")))
                        # 日付が変わるから日付を更新する
                        ft = datetime.datetime.strptime(monday + time_str, "%Y%m%d%H%M") + datetime.timedelta(days=new_i)
                        to = ft + datetime.timedelta(minutes=int(td.get("rowspan")))
                        new_data = {
                            "title": title,
                            "ft": ft.strftime("%Y%m%d%H%M"),
                            "to": to.strftime("%Y%m%d%H%M"),
                            "pfm": pfm,
                            "isBroadcast": isBroadcast
                        }
                        if isBroadcast:
                            new_data["isRepeat"] = isRepeat
                        main_data[new_i].append(new_data)
                        break
                else:
                    if tmp_dt == end_times[iterator2]:
                        # endtime を更新
                        end_times[iterator2] += datetime.timedelta(minutes=int(td.get("rowspan")))
                        ft = datetime.datetime.strptime(monday + time_str, "%Y%m%d%H%M") + datetime.timedelta(days=iterator2)
                        to = ft + datetime.timedelta(minutes=int(td.get("rowspan")))
                        new_data = {
                            "title": title,
                            "ft": ft.strftime("%Y%m%d%H%M"),
                            "to": to.strftime("%Y%m%d%H%M"),
                            "pfm": pfm,
                            "isBroadcast": isBroadcast
                        }
                        if isBroadcast:
                            new_data["isRepeat"] = isRepeat
                        main_data2[iterator2].append(new_data)
                        break
                iterator2 += 1



# while(iterator2 < 7)以下をcolspan番組を正しく取得するためだけに作ってみる
# td要素は一つだけ取得して、colspan分の曜日だけ同じ番組をmain_dataへ追加できるようにする
def colspaned_program_capture(td, colspan: int, itr: int):
    today = datetime.date.today()
    monday = (today - datetime.timedelta(days=today.weekday())).strftime("%Y%m%d")
    # 切替基準時間: 6:00になるはず
    criterion = datetime.datetime.strptime("06:00", "%H:%M")
    # 曜日ごとの「終了時間」を更新するためのリスト
    end_times = [datetime.datetime.strptime("06:00", "%H:%M")] * 7

    tmp_main_data = []
    for i in range(7):
        tmp_main_data.append([])

    # 
    # -- 番組情報取得パート -------
    # 
    # 放送休止枠なのかチェックする
    # 複数曜日にまたがっているので要修正
    if "放送休止" in td.find("div", class_="weeklyProgram-content").stripped_strings:
        title = "放送休止枠"
        pfm = ""
        isRepeat = False
        isMovie = False
        isBroadcast = False
    # 新番組枠かチェックする
    elif "新番組" in td.find("div", class_="weeklyProgram-content").stripped_strings:
        title = "未定枠"
        pfm = ""
        isRepeat = False
        isMovie = False
        isBroadcast = False
    # 取得要素以下はテキスト以外を含むのかチェックする
    elif not td.find("div", class_="weeklyProgram-content").string:
        title = td.select("div.weeklyProgram-content a")[0].text.replace("\n", "", 3)
        pfm = td.select("span.personality a")[0].text.replace("\n", "", 4) if td.select("span.personality a") else "None"
        isRepeat = True if "is-repeat" in td.get('class') else False
        isMovie = True if td.select('i.icon_program-movie') else False
        isBroadcast = True if td.select('i.icon_program-live') else False

    itr_ = itr
    while(itr_ < itr + colspan):
        print("itr", itr)
        # end_timesの更新
        # 





main()


"""
番組表URL: https://www.joqr.co.jp/qr/agregularprogram/

## 時間更新パート

`colspan`が設定されている番組はひとつのtd要素で複数日にまたいでいる
なのでcolspan番組に遭遇したら
通常のループ処理を逸脱して処理を施さなくてはならない


break文に行きつかなければ、while文の一番最後の`i2 += 1`へたどり着いて、
イテレータを更新してくれるはず

- td_all: tdタグを持つtrタグが入ることになる。つまり長さは最大で7になるはず
- td: ひと番組の情報。イテレータitrと対応する
- itr: td_allで取得される番組のインデックス。
そのまま曜日としてみなせるけれど、たとえばtd_allに含まれるtdの数は必ず7つとは限らない
その場合、曜日としてみなすのは危険である
ただしく更新できるようにしなくてはならない
- iterator2: itrの値を引き継ぐイテレータ
"""