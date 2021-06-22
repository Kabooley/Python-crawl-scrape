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


def main():
    # read json file
    path = "./playground/out/create_table.json"
    # This file includes 7 list and many dict in its each list
    program_file = readFile(path)

    converted_program_file = []
    for list in program_file:
        new_list = []
        for dict in list:
            # 変換処理、
            new_dict = convert_program_format(dict)
            # new_listにpushする
            new_list.append(new_dict)
        converted_program_file.append(new_list)
    
    for list in converted_program_file:
        for dict in list:
            # 上書き保存なのか、続きから追加してくれるのかは知らん
            write_dict_csv_by_row(dict)



def readFile(path: str) -> list:
    if not os.path.exists(path):
        return []
    f = open(path, "r")
    file = json.load(f)
    return file



# ヘッダに辞書のキーを、各行に辞書の値を、辞書の数だけcsvとして書き込んでいく
def write_dict_csv_by_row(data: dict):
    print(data)
    with open("playground/out/fckncsv.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "performer", "start", "close"])
        writer.writeheader()
        for dict in data:
            # 'str' object has no attribute 'keys'
            writer.writerow(dict)

# 例
# match_group(r'\b(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})\b', "202106150600")
def re_matched_groups(pattern, target: str) -> list:
    print("-- match_group() --")
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
