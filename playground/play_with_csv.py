"""
PLAY WITH CSV

コアメソッド:
 writeCsvRowByRow

"""

import csv
import json
import os
import re

fuckin_data = [
    {"date": "2021/06/15","performer": "washizaki","start": "06:00","close": "06:30",},
    {"date": "2021/06/15","performer": "washizaki","start": "06:00","close": "06:30",},
    {"date": "2021/06/15","performer": "washizaki","start": "06:00","close": "06:30",},
    {"date": "2021/06/15","performer": "washizaki","start": "06:00","close": "06:30",},
    {"date": "2021/06/15","performer": "washizaki","start": "06:00","close": "06:30",},
    {"date": "2021/06/15","performer": "washizaki","start": "06:00","close": "06:30",},
    ]

def main():
    with open("playground/out/fckncsv.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "performer", "start", "close"])
        writer.writeheader()
        for dict in fuckin_data:
            writer.writerow(dict)

main()

# 
def writeCsvRowByRow(data: dict):
    with open("playground/out/fckncsv.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "performer", "start", "close"])
        writer.writeheader()
        for dict in fuckin_data:
            writer.writerow(dict)


# {'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202106070000', 'to': '202106070030', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False}
# {'title': '鷲崎健のヨルナイト×ヨルナイト', 'date': '2021/06/07', 'ft': '202106070000', 'to': '202106070030', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False}
def divide_date_data():



def match_group(pattern, target: str) -> Match:
    print("-- match_group() --")
    rx = re.compile(pattern)
    # Match という型の変数を返す
    matches = rx.match(target)
    if matches:
        # print(matches)
        # print(matches.group(0))
        # print(matches.group(1))
        # print(matches.group(2))
        # print(matches.group(3))
        # print(matches.group(4))
        # print(matches.group(5))
        return matches



def readFile() -> list:
    path = "playground/out/create_table.json"
    if not os.path.exists(path):
        return []
    f = open(path, "r")
    file = json.load(f)
    return file