# Note BeautifulSoup4

## find()

```Python
find(name, attrs, recursive, string, **kargs)
```

usage:

- Searching by CSS class

```Python
soup.find_all("a" class_="sister")

# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
```

"class"というキーワードは既にPythonで予約語として定義されている都合上、
"class_"というキーワードをbs4では採用している

`class_`には文字列、正規表現、関数、`True`を渡すことができる

単一のタグがそのclass属性に複数の値を持つことができることに注意しましょう
特定のcssクラスに一致するtagを検索すると、そのCSSクラスのいずれかと一致します

```Python
css_soup = BeautifulSoup('<p class="body strikeout"></p>', 'html.parser')

# クラス名の一部でも検索可能
css_soup.find_all("p", class_="strikeout")
# [<p class="body strikeout"></p>]
css_soup.find_all("p", class_="body")
# [<p class="body strikeout"></p>]
# 完全一致検索でもおｋ
css_soup.find_all("p", class_="body strikeout")
# [<p class="body strikeout"></p>]

```

もしも`div.strikeout`みたいに複数のcssセレクタで検索したい場合は
css-selectorのメソッドを使いましょう  
```Python
css_soup.select("p.strikeout.body")
# [<p class="body strikeout"></p>]
```


### select()とfind_all()

selectもfind_allもどちらもリストを返す
マッチした要素と、その子要素を含んだ全部を1つの配列要素として扱う
なのでマッチした要素からさらにその子要素を取得したい場合
ひとつの例として下記のようにする

両者は同じ  

```Python
    # tdはbs4で取得した要素
    print(td.find_all("div", class_="weeklyProgram-content")[0].find_all('a'))
    print(td.select("div.weeklyProgram-content")[0].find_all('a'))
    print(td.select("div.weeklyProgram-content")[0].select('a'))
```