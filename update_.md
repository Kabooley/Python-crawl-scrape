# 開発日報

よけいな情報でなんだか見づらくなるので
書き方のルールを決めて書いていく

以下、サンプル

## 日付

進捗

------------
目標：何を成し遂げるのか明確な目標をここに書く  


工程: 大きな開発課題をロードマップ的に書く  


    例：
    1. 設計
    2. プログラム構成       <-- イマココ
    3. コントロールの作成
    4. モデルの作成
    5. ビューの作成
    とか
タスク：大きな開発課題の達成のために解決すべきタスクを書く

    例：
    @ プログラムの構成
    1. 処理内容のアイディアをひねり出す     済
    2. 処理イメージを絵にかきだす       済
    3. 各処理の細かな内容を詰める       <-- イマココ
    4. 各処理の役割を明確にする
    5. チームへの報告
    とか

------------

タスク達成のための成果や問題を端的に書き出す

1. 処理内容にアイディアをひねり出す


## 6/30

進捗  
-----------------------------------------------------  
目標：

    ネイティブアプリでwebラジオを自動録音・保存・通知するアプリケーションの作成

工程:

    1. 番組表取得パート     <-- イマココ
    2. 予約機能パート
    3. UIパート


問題：

    1. サーバをレンタルする必要があるか
    2. 

タスク：
    @ 番組取得パート
    - `if tmp_dt < criterion:`以降の処理では日付を追うごとに番組が取得できなくなる 主に`colpsan`に対応してから
    - 
---------------------------------------------------



ag.pyは最終的にmain_dataを返す
main_data2はmain_dataを返す前にmain_dataへ統合される

ちゃんと調べていないけれど、
日付を過ぎてからの番組はmain_dataへ
6:00~24:00までの番組はmain_data2へ挿入される仕組みの模様

おそらく問題は、リスト1~3の中身が空っぽであるところ
ag.py::create_table()で出力できた、main_data
```Python
# main_data
# [[{...}], [], [], [], [{...}, {...}, {...}, {...}, {...}, {...}, {...}], [{...}, {...}, {...}, {...}, {...}, {...}, {...}], [{...}]]
# どういうわけかこの時点で月曜日の0:00の番組が入っていることになっている
0: [
        {'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202106280000', 'to': '202106280030', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False}
    ]
1: []
2: []
3: []
4: [
        {'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202107020000', 'to': '202107020030', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False},
        {'title': '石見舞菜香・ファイルーズあいの凸凹Saturday Night☆～マジ東風イェア～', 'ft': '202107020030', 'to': '202107020100', 'pfm': '石見舞菜香', 'isBroadcast': False, 'isMovie': True, 'isRepeat': True},
        {'title': '河瀬茉希と赤尾ひかるの今夜もイチヤヅケ！', 'ft': '202107020100', 'to': '202107020130', 'pfm': '河瀬茉希', 'isBroadcast': False, 'isMovie': False, 'isRepeat': True}, 
        {'title': 'Lynnのおしゃべりんらじお', 'ft': '202107020130', 'to': '202107020200', 'pfm': 'Lynn', 'isBroadcast': False, 'isMovie': True, 'isRepeat': True},
        {'title': '三澤紗千香のラジオを聴くじゃんね！', 'ft': '202107020200', 'to': '202107020230', 'pfm': '三澤紗千香', 'isBroadcast': False, 'isMovie': False, 'isRepeat': True}, 
        {'title': '佐藤亜美菜のアミメン！', 'ft': '202107020230', 'to': '202107020300', 'pfm': '佐藤亜美菜', 'isBroadcast': False, 'isMovie': True, 'isRepeat': True},
        {'title': '裏方', 'ft': '202107020300', 'to': '202107020330', 'pfm': '松原秀', 'isBroadcast': False, 'isMovie': False, 'isRepeat': True}
     ]
5: [
        {'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202107030000', 'to': '202107030030', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False}, 
        {'title': '石川界人のとまどいイルカ', 'ft': '202107030030', 'to': '202107030100', 'pfm': '石川界人', 'isBroadcast': False, 'isMovie': False, 'isRepeat': True},
         {'title': '洲崎西', 'ft': '202107030100', 'to': '202107030130', 'pfm': '洲崎綾', 'isBroadcast': False, 'isMovie': False, 'isRepeat': True}, 
         {'title': '安野希世乃のきよなび！', 'ft': '202107030130', 'to': '202107030200', 'pfm': '安野希世乃', 'isBroadcast': False, 'isMovie': False, 'isRepeat': True}, 
         {'title': '高垣彩陽のあしたも晴レルヤ', 'ft': '202107030200', 'to': '202107030230', 'pfm': '高垣彩陽', 'isBroadcast': False, 'isMovie': False, 'isRepeat': True}, 
         {'title': '伊福部崇のラジオのラジオ', 'ft': '202107030230', 'to': '202107030300', 'pfm': '伊福部崇', 'isBroadcast': False, 'isMovie': False, 'isRepeat': True}, 
         {'title': 'MAN TWO MONTH RADIO', 'ft': '202107030300', 'to': '202107030330', 'pfm': 'なし', 'isBroadcast': False, 'isMovie': False, 'isRepeat': True}
    ]
6: [
    {'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202107040000', 'to': '202107040030', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False}
    ]
```

```Python
# ag.py::create_table()

for i in range(7):
    main_data[i].extend(main_data2[i])
```
上記のコードでmain_data2をmain_dataへ統合していく
ループは昇順で実施されて、ｲﾃﾚｰﾀはそのまま曜日を表す
(i == 0は月曜日)

1周目：
main_data[0]にすでに
```Python
        {'title': '鷲崎健のヨルナイト×ヨルナイト', 'ft': '202106280000', 'to': '202106280030', 'pfm': '鷲崎健', 'isBroadcast': True, 'isMovie': True, 'isRepeat': False}
```
が入っており、これのせいで月曜日のしょっぱなの番組が0:00からの番組になってしまっている

2周目：
main_data[1]は空である。そのため火曜日0:00~の番組が一切入っていない。
main_data2[1]もなぜか12:30~24:00までの番組が一切入っていない。
故にmain_data2[1]の内容しか出力されていない

3週目、4週目：
2週目と同じ状況


- 検証
2,3,4周目だけmain_dataが空っぽなのはおそらく`colspan`のパートが関係している可能性

283行目～：
`ft`と`to`の日付を更新していなかったのが原因
end_timesは更新できて...正しく更新できていなかった。daysは更新の必要がないかもしれない
```Python
                        if td.has_attr('colspan'):
                            # colspanの数値分だけi2とまたいでいる曜日の終了時間を更新する必要がある
                            # ここでその処理を行ってしまうと、他の処理が面倒になるから終了時間だけ更新すれば「あとから挿入」で済むかしら？
                            multiple_days = int(td.get('colspan'))
                            min = int(td.get("rowspan"))
                            # 
                            # 修正前
                            # 
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

                                # 修正後
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
```

結果、12:30~12:40の番組は取得できるようになった

7/1:

ag_copy.pyを作成
ｲﾃﾚｰﾀの役割
itrとiterator2は同じ値をとる
itrはwhile()ループ中は使わないので、
while()ループ中はiterator2が最終的にitrと帳尻が合えばよい


