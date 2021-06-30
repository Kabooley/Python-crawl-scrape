from bs4 import BeautifulSoup
import re


html = '''
    <td rowspan="60" class="is-ag is-repeat">
        <div class="program-wrap">
        <div class="weeklyProgram-time">6:00</div>
        <div class="weeklyProgram-content">
            <a href="https://www.joqr.co.jp/qr/program/thecatch/">A&amp;G ARTIST ZONE樋口楓のTHE CATCH</a>
            <i class="icon_program-movie"></i>
            <span class="personality">
            <a class="this-className-is-for-temporary" href="/qr/personality/higuchikaede/">樋口楓</a>
            </span>
        </div>
        </div>
    </td>
    <td rowspan="60" class="is-ag is-repeat">
        <div class="program-wrap">
        <div class="weeklyProgram-time">6:00</div>
        <div class="weeklyProgram-content">
            <a href="https://www.joqr.co.jp/qr/program/thecatch/">A&amp;G ARTIST ZONE 亜咲花のTHE CATCH</a>
            <i class="icon_program-movie"></i>
            <span class="personality">
            <a href="/qr/personality/asaka/">亜咲花</a>
            </span>
        </div>
        </div>
    </td>
    <td rowspan="60" class="is-ag is-repeat">
        <div class="program-wrap">
        <div class="weeklyProgram-time">6:00</div>
        <div class="weeklyProgram-content">
            <a href="https://www.joqr.co.jp/qr/program/thecatch/">A&amp;G ARTIST ZONE ▽▲TRiNITY▲▽ のTHE CATCH</a>
            <i class="icon_program-movie"></i>
            <span class="personality">
            <a href="/qr/personality/trinity/">▽▲TRiNITY▲▽</a>
            </span>
        </div>
        </div>
    </td>
    <td rowspan="60" class="is-ag is-repeat">
        <div class="program-wrap">
        <div class="weeklyProgram-time">6:00</div>
        <div class="weeklyProgram-content">
            <a href="https://www.joqr.co.jp/qr/program/thecatch/">A&amp;G ARTIST ZONE 煌めき☆アンフォレントのTHE CATCH</a>
            <i class="icon_program-movie"></i>
            <span class="personality">
            <a href="/qr/personality/kiramekiunforent/">煌めき☆アンフォレント</a>
            </span>
        </div>
        </div>
    </td>
    <td rowspan="60" class="is-ag is-repeat">
        <div class="program-wrap">
        <div class="weeklyProgram-time">6:00</div>
        <div class="weeklyProgram-content">
            <a href="https://www.joqr.co.jp/qr/program/thecatch/">A&amp;G ARTIST ZONE伊東歌詞太郎 のTHE CATCH</a>
            <i class="icon_program-movie"></i>
            <span class="personality">
            <a href="/qr/personality/itokashitaro/">伊東歌詞太郎</a>
            </span>
        </div>
        </div>
    </td>
    <td rowspan="60" class="is-ag is-repeat">
        <div class="program-wrap">
        <div class="weeklyProgram-time">6:00</div>
        <div class="weeklyProgram-content">
            <a href="https://www.joqr.co.jp/qr/program/ag_sp/">超！A&amp;G+ スペシャル</a>
        </div>
        </div>
    </td>
    <td rowspan="60" class="is-ag is-repeat">
        <div class="program-wrap">
        <div class="weeklyProgram-time">6:00</div>
        <div class="weeklyProgram-content">
            <a href="https://www.joqr.co.jp/qr/program/ag_sp/">超！A&amp;G+ スペシャル</a>
        </div>
        </div>
    </td>
    '''

def main():
    soup = BeautifulSoup(html, features="html.parser")
    navigation_the_tree()
    # find_all_basic(soup)


# 
def navigation_the_tree():
    html_doc = """
        <html>
        <head><title>The Dormouse's story</title></head>
        <body>
        <p class="title"><b>The Dormouse's story</b></p>

        <p class="story">Once upon a time there were three little sisters; and their names were
        <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
        <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
        <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
        and they lived at the bottom of a well.</p>

        <p class="story">...</p>
    """

    soup = BeautifulSoup(html_doc, "html.parser")

    # soup.headのように直接の子要素を指定できる
    print(soup.head)
    print(soup.head.title)

    # 直接の子要素検索
    # 
    # contents : returns list of matched
    print('contents: ')
    print(soup.body.contents)
    # children : 以下の方法で使うことはない
    print('children: ')
    print(soup.body.children)
    # 反復処理させるために使う
    for child in soup.body.children:
        print(child)

    # 深度を深くする検索: 直接の子要素、子要素の子要素...という感じ
    # 
    # .desecendants
    print('descendants: ')
    for child in soup.head.descendants:
        print(child)
    
    # .string
    # もしも取得した要素はテキストしか持たず、それが`NavigableString`ならば.stringで取得できる
    # テキスト以外も持つ場合、Noneを返す
    print(".string: ")
    print(soup.title.string)

    # .strings
    # soup内の`NavigableString`すべて取得する
    # white-spaceがち
    print(".strings: ")
    for str_ in soup.strings:
        print(str_)
    


# all about find_all() method
# find_all(name, attrs, recursive, string, limit, **kwargs)
# ヒットした要素をリストで返す
# unmatchedで空のリストを返す
def find_all_basic(soup: BeautifulSoup):
    # name argument: 指定した文字列に完全一致するタグを検索する
    print(soup.find_all('td'))
    print(len(soup.find_all('td')))
    # keyword argument: 認識できない文字列はタグの属性の一つを指すキーワードとして扱われる
    # class名
    print("class name: ")
    print(soup.find_all(class_='weeklyProgram-content'))
    # href
    print("href: ")
    print(soup.find_all(href=re.compile("joqr")))
    # 複数セット可能
    # クラス名`.weeklyProgram-content`でかつ"joqr"が含まれる文字列をもつhref属性であるタグを検索する
    print('multiple filters: ')
    print(soup.find_all(class_="this-className-is-for-temporary", href=re.compile("higuchikaede")))
    # `data-*`属性のような一部の属性にはキーワード引数の名前として使用できない名前がある
    # data_soup = BeautifulSoup('<div data-foo="value">foo!</div>', 'html.parser')
    # data_soup.find_all(data-foo="value")
    # SyntaxError: keyword can't be an expression
    # 
    # name属性に対してキーワード引数検索はできない
    # 代わりに次ができる
    print('name attr is not for argument: ')
    name_soup = BeautifulSoup('<input name="email"/>', 'html.parser')
    print(name_soup.find_all(name="email"))
    # []
    print(name_soup.find_all(attrs={"name": "email"}))
    # [<input name="email"/>]

    # string argument
    # 
    # string引数に渡した値が存在するか検索する。あった場合そのキーワードを返す。
    # キーワードはタグ名やクラス名である必要はない
    print('strgin argument: ')
    print(soup.find_all(string="伊東歌詞太郎"))
    # ['伊東歌詞太郎']
    # 
    # multiple with string
    print(soup.find_all('a', string="ag_sp"))   # <-- ちょっとマッチしなかったので見直しを

    # limit argument
    # 検索結果に制限をかける
    print('limit argument: ')
    print(soup.find_all(class_='weeklyProgram-content', limit=3))

    # recursive argument
    # 
    # 通常find_all()は、たとえば`mytag.find_all()`で呼び出したら、`mytag`のすべての子孫を検索対象にする
    # 検索対象を「直接の子孫」にする場合、`recursive=False`にする
    # コード例めんどいから省略

    # find() method
    # document.querySelector()と同じでマッチした一番初めの要素を返す
    # unmatchedで`None`を返す
    # find_all()で`limit=1`を付与するよりもはるかに効率的
    print("find() method is better than using limit=1: ")
    print(soup.find(class_='weeklyProgram-content'))




# 
def _test():
    html = """
    <td rowspan="30" class="is-ag">
        <div class="program-wrap">
          <div class="weeklyProgram-time">26:30</div>
          <div class="weeklyProgram-content">
            <a href="https://www.joqr.co.jp/qr/program/henradi/">小野友樹と夕刻ロベルのへんならじお</a>
            <i class="icon_program-movie"></i>
            <span class="personality">
              <a href="/qr/personality/onoyuki/">小野友樹</a>
            </span>
            <span class="personality">
              <a href="/qr/personality/yukokuroberu/">夕刻ロベル</a>
            </span>
          </div>
        </div>
    </td>
    <td rowspan="180" colspan="4" class="is-joqr">
        <div class="program-wrap">
          <div class="weeklyProgram-time">27:00</div>
          <div class="weeklyProgram-content">
            放送休止
            <!-- uatdahikaru -->
          </div>
        </div>
    </td>
    <td rowspan="30" class="is-ag">
        <div class="program-wrap">
          <div class="weeklyProgram-time">15:30</div>
          <div class="weeklyProgram-content">
            新番組
            <!--<a href="https://www.joqr.co.jp/qr/program//">新番組</a>-->
            <!--<span class="personality">
              <a href="/qr/personality/amatsuki/">天月-あまつき-</a>
            </span>
            <span class="personality">
              <a href="/qr/personality/yamamotokazutomi/">山本和臣</a>
            </span>
            <span class="personality">
              <a href="/qr/personality/yuseigamebu/">遊星高校ゲーム部</a>
            </span>-->
          </div>
        </div>
    </td>
    """
    soup = BeautifulSoup(html, "html.parser")
    for td in soup.find_all('td'):

        # 模索
        # if td.find_all("div", _class="weeklyProgram-content", string="放送休止"):
        #     print(td.find_all(string="放送休止"))
        # else:
        #     print("not 放送休止")
        # print('\n\n')
        # print(td.find_all("div", class_="weeklyProgram-content"))
        # # .string returns <bs4.element.NavigableString> 扱いが面倒
        # print(td.find("div", class_="weeklyProgram-content").string)
        # # .strings also returns <bs4.element.NavigableString> 使う場面があるのだろうか...
        # # for str_ in td.find("div", class_="weeklyProgram-content").strings:
        # #     print(str_)
        # # .stripped_strings returns <class 'str'> とても扱いやすい
        # for str_ in td.find("div", class_="weeklyProgram-content").stripped_strings:
        #     print(str_)
        #     print(type(str_))
        # # returns ['\n            放送休止\n          ']
        # print(td.find("div", class_="weeklyProgram-content").contents)
        # print('\n\n')

        # # 下記のコードでは、コメントを拾ってしまうらしい...
        # # if td.find("div", class_="weeklyProgram-content").string:
        # # コメントを無視するコードを追加する


        # 一旦できたもの。.stringはコメントを拾うとNoneを返すためボツ
        # td.find("div", class_="weeklyProgram-content")以下はテキストしか含まないかどうかチェックしたい
        # .stringでは、コメントがあってもNoneを返してしまう...クソか
        if td.find("div", class_="weeklyProgram-content").string:
            print("Only text.")
            # 放送休止が含まれるかチェックする
            if "放送休止" in td.find("div", class_="weeklyProgram-content").stripped_strings:
                print("the program is over tonight.")
            # 新番組枠かチェックする
            elif "新番組" in td.find("div", class_="weeklyProgram-content").stripped_strings:
                print("New program comming soon...")
        else:
            print("More than only text.")

        # 最終的にできたもの
        # .stripped_stringsならコメントを拾わないで済む模様
        # 放送休止枠なのかチェックする
        if "放送休止" in td.find("div", class_="weeklyProgram-content").stripped_strings:
            print("the program is over tonight.")
        # 新番組枠かチェックする
        elif "新番組" in td.find("div", class_="weeklyProgram-content").stripped_strings:
            print("New program comming soon...")
        # 取得要素以下はテキスト以外を含むのかチェックする
        elif not td.find("div", class_="weeklyProgram-content").string:
            print("More than only text")
        
# main()
_test()

"""
https://www.crummy.com/software/BeautifulSoup/bs4/doc/#kinds-of-objects

## 明らかにしていきたいところ

- おおまかな利用方法
- `Navigtating the tree`のパートのメソッドはたとえばfind_allとかのメソッドと併用できるのか？
- find_allメソッドとselectメソッドの併用は可能なのか？


## フィルタの種類

文字列:  文字列に対して正確な照合を行う
正規表現:   
リスト: リスト内の各要素に対して一致する文字列を検索する
True: 可能な限りすべてに一致する
関数


## special strings

Beautiful Soupは、埋め込みCSSスタイルシート（<style>タグ内にあるすべての文字列）、
埋め込みJavascript（<script>タグ内にあるすべての文字列）、
およびHTMLテンプレート（内部の任意の文字列）に対して、
Stylesheet、Script、およびTemplateStringと呼ばれるクラスも定義します。 
<template>タグ）。
これらのクラスは、NavigableStringとまったく同じように機能します。
それらの唯一の目的は、他の何かを表す文字列を無視することによって、
ページの本文を簡単に見つけられるようにすることです。 
（これらのクラスはBeautiful Soup 4.9.0の新機能であり、html5libパーサーはそれらを使用しません。）


## .string, .strings, .stripped_strings

.string
タグ以下はテキストだけだった場合に成功する
成功：そのテキストからなる`NavigableString`という<bs4.element.NavigableString>を返す。<class 'str'>ではない点注意。
失敗：テキストだけじゃなかった場合。Noneを返す
なんと、コメントが含まれているだけでNoneを返すので必ずコメントを回避しなくてはならない


"""