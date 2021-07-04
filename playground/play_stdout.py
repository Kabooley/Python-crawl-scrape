"""
standard out 

jsonファイルの内容を読み込んで、
その内容を標準出力させる

標準出力はjsonファイルの内容を箇条書きで出力して
その箇条書きのリストから、カーソルとエンターキーで一つを選択させる
という機能を実装する

- 処理チャート:

jsonファイルの内容を読み取る（曜日ごとに分けられたリストである、曜日ごとにはその曜日に放送する番組がリストされている）
-->
コンソールへ曜日を表示する
-->
ユーザは出力されているカーソルをキーボードの十字キーで操作する
-->
コンソールは十字キーの入力を受け取るたびに、「曜日選択画面」を上書きする（コンソールの位置も更新されている）
-->
エンターキーを受け取ったら、カーソルが指している曜日のリストを表示する画面を出力する
-->
同様に十字キーを操作して上書き表示する画面を出力する
-->
最終的に一つの番組を選択する
-->
選択された番組を最後にコンソールへ出力する
"""

import sys
import time
import json, os
import curses

this_scope_global = {
    "json_path": "./create_table__.json"
}

stdscr = curses.initscr()


def main():
    # output_to_each('./playground/out/stdout_to_file.txt')
    # output_line_recursively()
    # output_lines_recursively()
    # temp()

    # table = read_file(this_scope_global["json_path"])
    # while True:
    #     print(stdin_interface())

    output_weekday()



def output_weekday():
    sys.stdout = sys.__stdout__
    template ='\n'\
                    '===============\n'\
                    '= Program Resevation =\n'\
                    '===============\n'\
                    '      カーソルを移動して曜日を選択してエンターキー\n'\
                    '\n'\
                    '        --------------------------------------------------\n'\
                    '        =>      Monday:  7/5\n'\
                    '        =>      Monday:  7/5\n'\
                    '        =>      Monday:  7/5\n'\
                    '        =>      Monday:  7/5\n'\
                    '        =>      Monday:  7/5\n'\
                    '        =>      Monday:  7/5\n'\
                    '        --------------------------------------------------\n'
    print(template)

# basic usage
def output_to_each(file_path: str):
    # openしたファイルにだけ書き込まれて、
    sys.stdout = open(file_path, "w")
    print("ooooohhhhhaaaahhhhhhhh")
    # コンソールにだけ出力される
    sys.stdout = sys.__stdout__
    print("coooooonnnsooooooolllleeeeeeeeeeeeeeeeee")



# basic usage
def output_line_recursively():
    # 同じ場所に10カウントする番号が表示される
    for i in range(10):
        print("\r"+str(i),end="")
        time.sleep(1)

def output_lines_recursively():
    for i in range(10):
        print(str(i)+"\n"+str(i)+"\n"+str(i)+"\n"+"\033[3A",end="")
        time.sleep(1)

def temp():
    for num, i in enumerate(range(100)):
        sys.stdout.write("\r%d" % num)
        sys.stdout.flush()
        time.sleep(0.01)


# 無限ループの中で呼び出されて、入力されたキーを返す
# input()関数に対してキーボードの方向キーを入力すると、コンソール上のカーソルが移動して
# 出力場所を上書きしてしまう場合がある...
# なのでカーソルの場所も制御する必要があるかと...
def stdin_interface() -> str:
    # 引数の文字列を画面に出力して、入力された内容(入力完了はエンターキー)は次の行に表示される
    # 最終的に上書き表示したいので、入力内容が画面に出力されてしまうのはNG
    return input('stroke a key: ')

# def cureses_():
#     while True:
#         c = stdscr.getch()
#         if c == ord('p'):
#             PrintDocument()
#         elif c == ord('q'):
#             break  # Exit the while loop
#         elif c == curses.KEY_HOME:
#             x = y = 0




def read_file(path: str) -> list:
    if not os.path.exists(path):
        return []
    f = open(path, "r", encoding="utf-8")
    file = json.load(f)
    return file

main()

"""
sys

standard outputはストリームである
ストリームをパイプするには代入を使うことで
「どこへ」出力するのか任意に変更することができる

## キーボードから一文字だけ入力を受け取る方法

自前
curses（標準だけど別窓が開く)
kbhit.py（ｻｰﾄﾞﾊﾟｰﾃｨ）

## curses

いろいろ面倒な模様なので
便利なことにcursesラッパークラスを標準で用意してくれている

```Python
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 11):
        v = i-10
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
```


## 参考
https://segafreder.hatenablog.com/entry/2015/07/28/001716
https://www.lifewithpython.com/2018/01/python-change-output-by-standard-output-type.html
https://docs.python.org/ja/3/library/curses.html#constants
https://note.nkmk.me/python-string-line-break/
https://stackoverflow.com/questions/26413847/terminal-messed-up-not-displaying-new-lines-after-running-python-script

"""

"""
View 例

- top

曜日から選ぶ
or 
検索キーワードで該当番組を表示する

- 曜日から選ぶ

```terminal
# > youraccount/currentdirectory$ 実行したとして
===============
= Program Resevation =
===============
        カーソルを移動して曜日を選択してエンターキー

        --------------------------------------------------
        =>      Monday:  7/5
                   Tuesday: 7/6
                   Wednesday: 7/6
                   Thursday: 7/6
                   Friday: 7/6
                   Saturday: 7/6
                   Sunday: 7/6
        --------------------------------------------------
```
上記`----`の間をキー入力のたびに上書き表示する
各曜日を表示するかどうかは、create_table__.jsonの内容次第
取得した番組表で、一つも番組がない曜日があったらその曜日は表示しないなど
選択中の行は太字にするとか...


ひとまず上記をprintしてみる

- try 1
```Python
template = '===============\n'\
                 '= Program Resevation =\n'\
                 '===============\n'\
                 '      カーソルを移動して曜日を選択してエンターキー\n'\
                 '\n'\
                 '        --------------------------------------------------\n'\
                 '        =>      Monday:  7/5\n'\
                 '        =>      Monday:  7/5\n'\
                 '        =>      Monday:  7/5\n'\
                 '        =>      Monday:  7/5\n'\
                 '        =>      Monday:  7/5\n'\
                 '        =>      Monday:  7/5\n'\
                 '        --------------------------------------------------\n'

```
やっぱり余計なインデントが入る
あとこれを実行して以降のコンソールの挙動がおかしい
以降のコンソールの表示がまるで`template`の書式に従って表示されるかのようである
stdoutについてひととおり学習が必要である

プログラムを終了する前に「正常に戻す」処理が必要なのかもしれん


"""