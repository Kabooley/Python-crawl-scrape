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


def dates():
    date_str = "202106150600"   # 2021/6/15 6:00
    # pattern = r'\d{4}\d{2}\d{2}\d{2}\d{2}'  # this doesn't work...
    pattern = r'.+\/(\d{4})(\d{2})(\d{2}).+'
    sub_str = '\\1-\\2-\\3'
    result = re.match(pattern, date_str)
    result2 = re.sub(pattern, sub_str, date_str, 0, re.MULTILINE)
    print(result2)
    if result:
        print(result)
        print(type(result))
        print(result.group()) # 202106150600
        print(result.start(), result.end()) # 0 12
        print(result.group()[2])
        print(result.group()[3])
        print(result.group()[4])
        print(result.group()[5])
    else:
        print('No match')

dates()