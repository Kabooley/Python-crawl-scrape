"""
Python 正規表現　練習帳
"""
import re


def sample():
    # rを付けることを推奨。
    # バックスラッシュをそのままで分かりやすいため。
    content = r'hellow python, 123,end' 
    # ()で取りたい文字を
    pattern = '.*?(\d+).*'

    result = re.match(pattern, content)

    if result: #none以外の場合
        # group()で全文字を
        print(result.group())  # hellow python, 123,end
        # group(1)で数字を
        print(result.group(1)) # 123

    """
    hellow python, 123, end
    123
    """


# 任意の表現に置換する
def sample_sub():
    regex = r".+\/(\d{4})(\d{2})(\d{2}).+"

    test_str = "date file /20190529050003/folder "

    subst = "\\1/\\2/\\3"

    # You can manually specify the number of replacements by changing the 4th argument
    result = re.sub(regex, subst, test_str, 0, re.MULTILINE)

    if result:
        print (result)


def  my_match(regex, test_str: str):
    print("my_match()")

    pattern = re.compile(regex)
    foundall = re.findall(pattern, test_str)
    fullmatches = pattern.fullmatch(test_str)
    matches = pattern.match(test_str)
    if matches:
        print("matches")
        print(matches)
        print(matches.group(0))
    if fullmatches:
        print("full matches")
        print(fullmatches)
        print(fullmatches.group())
    if foundall:
        print("found all")
        print(foundall)

    print('-------------------------------------')



# invalid group reference 1 at position 1
def sub_date_express(pattern, date_str: str, substr):
    print('sub_date_express()')
    result = re.sub(pattern, substr, date_str, 0, re.MULTILINE)
    if result:
        print(result)


def match_group(pattern, target: str):
    print("-- match_group() --")
    rx = re.compile(pattern)
    # Match という型の変数を返す
    matches = rx.match(target)
    if matches:
        print(matches)
        print(matches.group(0))
        print(matches.group(1))
        print(matches.group(2))
        print(matches.group(3))
        print(matches.group(4))
        print(matches.group(5))



"""
タプル: ("strings", 12, 36.77, "ahead")
list: [1, 2, 3, 4, 5, 6, 7, 8, 9]

tupleとlistの違いは、前者がイミュータブルで後者がミュータブルであるところ
それ以外は
要素でアクセスできるところが同じ

つまりタプルは変更不可能の配列である

matched_object.groups()はタプルを返す
"""
def yyyymmddhhmm_2b_seperated(origin_str: str) -> tuple:
    pattern = r'\b(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})\b'
    rx = re.compile(pattern)
    matches = rx.match(origin_str)
    # print(rx.fullmatch(origin_str))
    if matches:
        return matches.groups()
    else:
        return ()


# 完全一致する場合
# matches, fullmatches, foundall すべて当てはまる
my_match(r'\b\d{4}\d{2}\d{2}\d{2}\d{2}\b', "202106150600")
# 前方一致する場合
# matches, foundallが当てはまった
# my_match(r'\b\d{4}\d{2}\d{2}\d{2}\d{2}\b', "202106150600 あ")
# # found allだけ一致
# my_match(r'\b\d{4}\d{2}\d{2}\d{2}\d{2}\b', "あ 202106150600")
# # 一致なし
# my_match(r'\b\d{4}\d{2}\d{2}\d{2}\d{2}\b', "あ 20210615060000")


sub_date_express(r'\b(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})\b', "202106150600", "\\1/\\2/\\3")


match_group(r'\b(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})\b', "202106150600")


print(yyyymmddhhmm_2b_seperated("202106150600"))

"""
Note 正規表現

- 使うには
import re



- 'r'
正規表現では、特殊な形式や表現を表すためにバックスラッシュ文字を利用する(\)
リテラルとしてのバックスラッシュを正規表現でマッチさせるためには`\\\\`と記述しなくてはならない
これは面倒ということで正規表現パターンですよという予約語として
`r"正規表現パターン"`という"r"のキーワードを用いる

- コンパイル済オブジェクトとは
何度も使う正規表現オブジェクトは、コンパイルすると効率的らしい。
ちょっとしか使わないような正規表現オブジェクトはコンパイルする必要はないらしい
つまり全然必須じゃないよってわけですね
ただある表現がオブジェクトとして渡されるから、変数を扱うだけで済むから
何度も正規表現の文字列を打つ必要がなくなって少し楽だねって話
正規表現であるオブジェクトを使うか
正規表現そのものをつかうか
のどちらを選択するのかって話

でもコンパイル済オブジェクトにすると、reのメソッドをオブジェクトが使えるようになる




"""