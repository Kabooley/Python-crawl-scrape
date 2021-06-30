"""
Order Json to CSV file 

jsonファイルの内容を部分返還してcsvファイルにするよ


## dictのコピーの生成お作法


"""

"""
要検討　その１

日付、開始時間順に昇順ソートする

prerequisities:
    まずJSONファイルから読み込んだLISTファイルは7つの配列が含まれていて
    その配列は同じ日付で分けられている
    つまり
    おなじ配列ならば同じ日付なので、つまり「開始時間」のソートだけすればよい

How to Sort:
    "06:00"というようなフォーマットの文字列をソートする
"""
import json
import os
import csv
import re


tmp_globals = {
    "read-file-path": "./create_table_3.json",
    "write-file-path": "./playground/out/joqr_programs_4.csv"
}


def main():
    # read json file
    path = tmp_globals
    # This file includes 7 list and many dict in its each list
    program_file = readFile(tmp_globals["read-file-path"])

    submain(program_file)




def submain(program_file):
    print(type(program_file))
    converted_program_file = []
    for list in program_file:
        new_list = []
        for dict in list:
            # 変換処理、
            new_dict = convert_program_format(dict)
            # new_listにpushする
            new_list.append(new_dict)
        converted_program_file.append(new_list)
    
    counter = 0
    for list in converted_program_file:
        # 上書き保存なのか、続きから追加してくれるのかは知らん
        print(counter)
        write_dict_csv_by_row(list)
        counter += 1


def readFile(path: str) -> list:
    if not os.path.exists(path):
        return []
    f = open(path, "r", encoding="utf-8")
    file = json.load(f)
    return file



# ヘッダに辞書のキーを、各行に辞書の値を、辞書の数だけcsvとして書き込んでいく
# 書き込みデータ例：{'title': '鷲崎健のヨルナイト×ヨルナイト', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False, 'date': '20210607', 'start': '00:00', 'close': '00:30'}
# header: ['title', 'pfm', 'isBroadcast', 'isMovie', 'isRepeat', 'date', 'start', 'close']
def write_dict_csv_by_row(data: list):
    with open(tmp_globals['write-file-path'], "a",encoding="utf_8_sig", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['title', 'pfm', 'isBroadcast', 'isMovie', 'isRepeat', 'date', 'start', 'close'])
        writer.writeheader()
        for dict in data:
            # 'isBroadcast', 'isMovie', 'isRepeat'がTrueだとcsvへの出力が省略されてしまう...
            # あとなぜか番組が12個しか書き込まれなかった
            # どうやら上書きされてしまっている模様...

            writer.writerow(dict)

# 例
# match_group(r'\b(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})\b', "202106150600")
def re_matched_groups(pattern, target: str) -> list:
    rx = re.compile(pattern)
    # matches is match object
    matches = rx.match(target)
    if matches:
        return list(matches.groups())
    else:
        return []


# {'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202106070000', 'to': '202106070030', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False}
# converted to...
# {'title': '鷲崎健のヨルナイト×ヨルナイト', 'date': '20210607', 'start': '00:00', 'close': '0030', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False}
# つまり日付と開始時間と終了時間の表現を変更するわけです
def convert_program_format(program: dict) -> dict:
    start_time_group = re_matched_groups(r'\b(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})\b', program['ft'])
    close_time_group = re_matched_groups(r'\b(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})\b', program['to'])
    # dict
    converted_program = program.copy()
    # 要素削除
    del converted_program['ft']
    del converted_program['to']
    # 追加するプロパティをタプルとして生成しておく
    converted_program['date'] = start_time_group[0] + start_time_group[1] + start_time_group[2]
    converted_program['start'] = start_time_group[3] + ':' + start_time_group[4]
    converted_program['close'] = close_time_group[3] + ':' + close_time_group[4]

    return converted_program



# この関数は何度も呼出すけれど、「同じcsvファイル」に「続きを書き込みたい」ので
# そのための特別なファイル操作が必要である
# def write_program_2_csv(program: dict):




# HELPER FUNCTION
def _length(program_file, converted_program_file):
    print(len(program_file[0])
        + len(program_file[1])
        + len(program_file[2])
        + len(program_file[3])
        + len(program_file[4])
        + len(program_file[5])
        + len(program_file[6])
    )
    print(len(converted_program_file[0])
        + len(converted_program_file[1])
        + len(converted_program_file[2])
        + len(converted_program_file[3])
        + len(converted_program_file[4])
        + len(converted_program_file[5])
        + len(converted_program_file[6])
    )




main()


"""
# 開発進捗メモ

## 問題
- isBroadcast, isMovie, isRepeatなどのBooleanがCSVへ出力するときに正しく書き込まれない
- 実際にExcelでCSVファイルを開くと文字化けする
- ヘッダーと同じ列に同じデータが出力されていない( --> 文字化けのせいで、解決した)


### isBroadcast, isMovie, isRepeatなどのBooleanがCSVへ出力するときに正しく書き込まれない
そもそも読み取り側のデータにそのプロパティが含まれていなかった...
create_table.txtへ出力されているデータの時点で`isBroadcast`以外パラメータが記載されていなかったので
書き込み時点の問題
--> ap.pyを修正しよう
修正した

ag.pyで、`create_table.json`に書き込みデータがすでにisBroadcast, isMovie, isRepeatがついていない

### 実際にExcelでCSVファイルを開くと文字化けする

JSON書き込み時点にさかのぼってエンドーディングとデコーディングが正しいかチェックする

```Python
    # 書き込み時点
    f = open("create_table.json", "w")
    json.dump(new_table, f, ensure_ascii=False)
```
上記open()にencoding='utf-8'パラメータを追加する
--> 結果、order_json_2_csv_.csvはやっぱり文字化けのまま

```Python
def readFile(path: str) -> list:
    if not os.path.exists(path):
        return []
    # 読み取り時点
    f = open(path, "r")
    file = json.load(f)
    return file
```

ここにエンコーダパラメータを追記する
--> やっぱりだめだ

よくみたら英語は完全に表現できているので、日本語だからダメなのか？...
参考：https://qiita.com/kino15/items/c9c06bdfc8e4a6ad34e3
つまり
```Python
with open('file_path', 'w', encoding='utf_8_sig'):
    writer = csv.DictWriter(...)
```
'utf_8_sig'という文字コードを指定すると解決した


これでcsvファイル出力は望みどおりにおおむねできている
あとはag.pyで足りないパラメータを出力させるだけ



## 実際に比較する
Pythonで取得した側のファイルは用意できた
比較した結果

やっぱりちゃんと取れていない部分がある
要修正...

"""