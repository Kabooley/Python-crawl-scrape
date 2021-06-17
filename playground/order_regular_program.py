"""
ag.pyで取得したJSONファイルの情報を抽出して
超a&g+の番組表にある情報を完全に取得できているのか確認するためのファイル

どうなればいいのか
Qiitaからひろってきたapiが正しく出力されていることが確認できれば良い
csvファイルを出力して、実際の番組表とあっているのか比較する
csvファイルの出力書式とかを決めればよい

https://www.delftstack.com/ja/howto/python/python-dictionary-to-csv/
上記のサイトを参考にすると
辞書型はkeyと値を1行として、
その次のペアをその下の行に書き込む
つまりこう

```Python
    {'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202106070000', 'to': '202106070030', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False}
```
```csv
    title, 鷲崎健のヨルナイト×ヨルナイト,
    ft, 202106070000,
    to, 202106070030,
    pfm, 鷲崎健,
    isBroadcast, True, 
    isMovie, True, 
    isRepeat, False,

```
とはいえ実装方法に依存するので別に次のようにもできる
```
title, ft, to, pfm, isBroadcast, isMovie, isRepeat,
鷲崎健のヨルナイト×ヨルナイト, 202106070000, 202106070030, 鷲崎健, True, True, False
鷲崎健のヨルナイト×ヨルナイト, 202106070000, 202106070030, 鷲崎健, True, True, False
鷲崎健のヨルナイト×ヨルナイト, 202106070000, 202106070030, 鷲崎健, True, True, False
```

楽なので上記の通りの書式にしよう

タスク
1. プログラム側で上記の書式のcsvファイルを出力する
2. 上記の書式のcsvファイルを手入力で番組表から用意する
3．両者を比較する(diffmergeとか)

"""

"""
書式


"""
import json
import os
import re

def main():
    path = "./playground/out/create_table.json"
    lists = readFile(path)
    convertedList = []
    for list in lists:
        for program in list:
            print(program)


def readFile(path: str) -> list:
    if not os.path.exists(path):
        return []
    f = open(path, "r")
    file = json.load(f)
    return file

# crate_table.jsonから、番組を整列させる
# 日付と開始時間の昇順
# 新しいlistを用意して、昇順で{}を並び変える
# {'ft': '202106120600', 'to': '202106120700'}のデータを{date：6/12 start: 6:00、close: 7:00}で生成しなおす
# def convertDate():




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

"""
file: 
0: [{'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202106070000', 'to': '202106070030', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False}, {'title': 'A&G ARTIST ZONE樋口楓のTHE CATCH', 'ft': '202106070600', 'to': '202106070700', 'pfm': '樋口楓', 'isBroadcast': False}, {'title': '白石晴香のぽかぽかたいむ', 'ft': '202106070700', 'to': '202106070730', 'pfm': '白石晴香', 'isBroadcast': False}, {'title': '伊波杏樹のRadio Curtain Call', 'ft': '202106070730', 'to': '202106070800', 'pfm': '伊波杏樹', 'isBroadcast': False}, {'title': '学園祭学園 青木佑磨のザ・ゴールデン・ゴールド・ゴー・ゴー', 'ft': '202106070800', 'to': '202106070900', 'pfm': '青木佑磨', 'isBroadcast': False}, {'title': 'Fate/Grand Order カルデア・ラジオ局Plus', 'ft': '202106070900', 'to': '202106071000', 'pfm': '大久保瑠美', 'isBroadcast': False}, {'title': '超！A&G+ × ABEMAアニメ Special Radio Program', 'ft': '202106071000', 'to': '202106071030', 'pfm': '週替わり', 'isBroadcast': False}, {'title': '駒田航 K-WAVE Radio', 'ft': '202106071030', 'to': '202106071100', 'pfm': '駒田航', 'isBroadcast': False}, {'title': '斉藤壮馬 Strange dayS', 'ft': '202106071100', 'to': '202106071130', 'pfm': '斉藤壮馬', 'isBroadcast': False}, {'title': '思春期が終わりません！！', 'ft': '202106071130', 'to': '202106071200', 'pfm': '浅沼晋太郎', 'isBroadcast': False}, {'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202106071200', 'to': '202106071230', 'pfm': '鷲崎健', 'isBroadcast': False}, {'title': 'Pyxisの夜空の下 de Meeting', 'ft': '202106071230', 'to': '202106071240', 'pfm': '伊藤美来', 'isBroadcast': False}, {'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202106071240', 'to': '202106071300', 'pfm': '鷲崎健', 'isBroadcast': False}, {'title': 'セブン－イレブン presents 江口拓也のラジオ道場', 'ft': '202106071300', 'to': '202106071330', 'pfm': '江口拓也', 'isBroadcast': False}, ...]

1: [{'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202106080000', 'to': '202106080030', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False}, {'title': 'Pyxisの夜空の下 de Meeting', 'ft': '202106080030', 'to': '202106080040', 'pfm': '伊藤美来', 'isBroadcast': False, 'isMovie': True}, {'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202106080040', 'to': '202106080057', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False}, {'title': 'ファンキル・タガタメ Presents 今泉Pと王子的3分間', 'ft': '202106080057', 'to': '202106080100', 'pfm': '今泉潤', 'isBroadcast': False, 'isMovie': True}, {'title': '河瀬茉希と赤尾ひかるの今夜もイチヤヅケ！', 'ft': '202106080100', 'to': '202106080130', 'pfm': '河瀬茉希', 'isBroadcast': False, 'isMovie': False}, {'title': 'Lynnのおしゃべりんらじお', 'ft': '202106080130', 'to': '202106080200', 'pfm': 'Lynn', 'isBroadcast': False, 'isMovie': True}, {'title': '三澤紗千香のラジオを聴くじゃんね！', 'ft': '202106080200', 'to': '202106080230', 'pfm': '三澤紗千香', 'isBroadcast': False, 'isMovie': False}, {'title': '佐藤亜美菜のアミメン！', 'ft': '202106080230', 'to': '202106080300', 'pfm': '佐藤亜美菜', 'isBroadcast': False, 'isMovie': True}, {'title': '放送休止', 'ft': '202106080300', 'to': '202106080600', 'pfm': '', 'isBroadcast': False, 'isMovie': False}, {'title': 'A&G ARTIST ZONE 亜咲花のTHE CATCH', 'ft': '202106080600', 'to': '202106080700', 'pfm': '亜咲花', 'isBroadcast': False}, {'title': '小原好美のココロおきなく', 'ft': '202106080700', 'to': '202106080730', 'pfm': '小原好美', 'isBroadcast': False}, {'title': '井澤美香子・諏訪ななかのふわさた', 'ft': '202106080730', 'to': '202106080800', 'pfm': '井澤美香子', 'isBroadcast': False}, {'title': 'A&G NEXT ICON 超！CUE！&A', 'ft': '202106080800', 'to': '202106080900', 'pfm': '内山悠里菜', 'isBroadcast': False}, {'title': 'セブン－イレブン presents 内田真礼とおはなししません？', 'ft': '202106080900', 'to': '202106080930', 'pfm': '内田真礼', 'isBroadcast': False}, ...]
...
と要素数は7つのリストinリスト
"""