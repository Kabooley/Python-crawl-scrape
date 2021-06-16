"""
ag.pyで取得したJSONファイルの情報を抽出して
超a&g+の番組表にある情報を完全に取得できているのか確認するためのファイル


とにかく「完全に一致しているのか」チェックしたい...

https://qiita.com/Morio/items/7538a939cc441367070d

32
39
38
10
36
11
12

各曜日、各時間正しい番組情報が取得できているか

比較用のエクセルファイルはonedrive上で管理すること

jsonファイルをcsvで出力して、あらかじめ用意しておいた（くっそ手入力の）csvファイルと
diffmergeで比較する

あらかじめ手入力csvファイルは番組情報が完全に取得できていることを確認しておくこと
めんどい(;´Д｀)

表示形式


"""
import json
import os
import re

def main():
    path = "./playground/out/create_table.json"
    if not os.path.exists(path):
        return
    
    f = open(path, "r")
    jsonfile = json.load(f)

    # list
    # print(type(jsonfile))
    # 7
    print(len(jsonfile))
    for lists in jsonfile:
        for list in lists:
            # 各番組所法は{}の辞書型
            print(list)


# crate_table.jsonから、番組を整列させる
# 日付と開始時間の昇順
# 新しいlistを用意して、昇順で{}を並び変える
# {'ft': '202106120600', 'to': '202106120700'}のデータを日付：6/12 開始時間: 6:00、終了時間: 7:00で生成しなおす
# def order(table: json):



def yyyymmddhhmm_2b_seperated(origin_str: str) -> tuple:
    pattern = r'\b(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})\b'
    rx = re.compile(pattern)
    matches = rx.match(origin_str)
    # print(rx.fullmatch(origin_str))
    if matches:
        return matches.groups()
    else:
        return ()

main()