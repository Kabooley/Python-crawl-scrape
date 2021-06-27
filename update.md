# 進捗とか問題とかの解決メモ

## 進捗

- 5/27
仮想環境削除:   crawl-scrape, stream-proj
仮想環境再構築：crawl_scrape
[(.venv)環境でpipインストールしたパッケージが読み込まない問題](#(.venv)環境でpipインストールしたパッケージが読み込まない問題)の解決


- 5/28
~/.sshディレクトリを作って公開鍵と秘密鍵を生成したよ
githubのリポジトリにpushしたよ


- 5/29
mongodbを~/teddy/home/以下にインストールしたよ
wsl2上ではsystemdが使えない問題を解決する
参考：https://discourse.ubuntu.com/t/using-snapd-in-wsl2/12113

上記の参考サイトの通りに実施する場合、たぶんなんかパスの設定が引き継がれないというか
とにかく前の環境と異なる環境になる模様
これをなんでか調べると人生2回くらい終了しそうなので
本題と関係ないのでほっとく

とにかくsystemdなしでsystemdコマンドを必要とするコマンドを代替できる手段がないか
模索する
systemdを使えるようにするまたは回避する方法の習得はwsl2を扱ううえで絶対に避けては通れないはずなので
なんとかするっきゃないな～

新規フォルダの追加、既存フォルダの削除　~/python-space/crawl_scrape
wsl2 + Ubuntu-20.04環境へのデータベース追加について学習中
wsl2 + Ubuntu-20.04でのMongoDBを扱うために

- 5/31
wsl2 + Ubuntu環境では`systemd`コマンドを使わない方針でいく
`systemd`抜きで`mongod`起動方法確認
テキスト3章はmongodbの使い方以外省く

5章開始。wikiのデータセットダウンロード中
ダウンロード時間かかりすぎなので基礎勉強でも...

- 6/1
Twiiter Developersに登録
テキストの内容が古いためか記述通りにいかないので
twitterAPIを使えるようにgetting startedを進める
遠回り過ぎる
いつぞやNode.jsでやったみたいにweatherAppを使えるようにするためのサービスの登録と同じ
自身でそのAPIを使えるようにするためのAPI access tokenを得られるようにする
どうやら正式に利用開始できるまでに時間がかかる模様
...さらに質問に詳しく答えないと使わせないよとのこと
別にtwitterで何かしたいわけじゃあ全然ないからもういいです
5.5章から学習を再開する

urllib.robotparserで調べた限り
クラシルはスクレイピングするのは、ランキングに関する部分や会員用コンテンツに関する部分でないならば大丈夫そうである
クラシルをちょっとスクレイピングしてみよう
playground/krashiru.py

sessionとCookieを勉強して!

- 6/2
うっかりメールアドレスとパスワードをアップしてしまう失態ぶり
[chromedriverをインストールしたけどそんなやついないっていわれる件](#chromedriverをインストールしたけどそんなやついないっていわれる件)



- 6/5
やっと両方の環境でchromeをseleniumで使えるようになった～
あとでどうしたのか記録を残すこと
今はseleniumの使用になれること


- 6/9
ag.pyの開発中で番組表の取得中。ほぼ丸パクリだけどちょうどいいね。丸パクリだけどうまくいかん部分あるのでリファクタリングしている
BeautifulSoup4で取得した要素自身の取得は.findや.selectでは取得できない
.getで取得できる


- 6/11
いまさらだけどどういうアプリケーションを作りたいのか
形にしましょう...
[アイディア形成](#アイディア形成)

- 6/12
取得したデータが正しいかどうかの検査は後回しにする
いまは取得した番組表をどう使うかを追及する
要はビジュアルで番組一覧を表示してその中から録音予約する番組を選択することになるんだけど
そうなるとどの端末での操作なのかとかが必要になってくるね...
windows10アプリケーション vs webサイト 
...
ない
アプリない
あったけどウイルス付きか「画面録画」のやつだった
「自動録画」＋「スーパー解りやすいUI」＋「スマホ」



```Python

    # 結果この方法が正しいとわかった
    # .findや.selectではtd自身を取得できないが、td自身を取得するには.getを使うといいらしい！
    # .findや.selectと、.get()の違いはそこにあるらしい
    classList = td.get("class")
    isSuspension = True if "is-joqr" in classList else False
    print(isSuspension) 
```
これをtitleが放送休止になる場合の条件に当てはめる




## アイディア形成

別ファイルにまとめます
idea.md


## 知見 experience and knowledge
-------------

### module not found にまつわる解決策集

- **VSCodeで手動でPython インタプリタを選択すること**

```
$> source .venv/bin/actiavte
```
上記を行う前にした`pyenv shell <任意のdistro>`を覚えておいて
```
(.venv) $> code .
```
VSCodeをremoteで開いたらとにもかくにもコマンドパレットを開いて、
`python: Select Interpreter`で仮想環境とpyenvで指定したインタプリタの組み合わせのインタプリタを選びましょう！！

そうしないと永遠にmodule not foundになる

- remote vscodeのターミナルが、Linuxの画面と同じじゃない場合再起動すること

もしくはまったく関係ないターミナル開いている可能性あるので注意






### how to install MongoDB into Ubuntu-20.04

official: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/


### WSL2ではsystemdコマンドが使えないよ

まずwsl2 + Ubuntuでは`systemd`コマンドが使えない
なのでsystemctlを使ったmongodb起動とかできない

参考
- systemctlつかわない例:
https://github.com/michaeltreat/Windows-Subsystem-For-Linux-Setup-Guide/blob/master/readmes/installs/MongoDB.md
- You Probably Don't Need systemd on WSL (Windows Subsystem for Linux)
https://dev.to/bowmanjd/you-probably-don-t-need-systemd-on-wsl-windows-subsystem-for-linux-49gn

- `systemd`を使えるようにする方法
https://discourse.ubuntu.com/t/using-snapd-in-wsl2/12113
ただし「環境が変わってしまう」
よく理解できていないけれど、snapdというものを使うせいなのか、それともprocessの名前空間が変わるせいなのか解っていない
-->手出ししないことにした


### `systemd`抜きで頑張ってmongodを使う

参考:https://github.com/michaeltreat/Windows-Subsystem-For-Linux-Setup-Guide/blob/master/readmes/installs/MongoDB.md

(.venv)Ubuntu側で`sudo mongod --dbpath ~/data/db`でmongod起動
VSCode側でターミナルを使う


### vscodeのターミナルでpython実行するときにpipでインストールしたライブラリがないとか言われる件

解決策：**Pythonインタプリタをコマンドパレットで選択後、ターミナルをもう一つ開く**

問題：
`code .`で開いたときのVSCodeのターミナルは環境のターミナルではないらしく
ただ単にそこのディレクトリがカレントディレクトリのターミナルであるらしい

もうひとつターミナルを開くと環境のターミナルが開かれる




### クロールにおけるサーバ負荷軽減

接続先のサーバへの負荷軽減を追及するために考えなくてはならないこと

1. 同時接続数

同時接続数とは、同じタイミングで送受信しているデータの数である
たとえば1つのサーバから4つのデータを同時にダウンロードしている状況があるとする
(HTML、image/png, CSS, JSとか)
この時同時アクセス数は4である

同時接続数は限りなく1に近づけるべき


2. クロール間隔

接続が完了して次の接続へ移る時は必ず1秒以上の間隔をあけましょう


### webサイト管理者側がクローラを制御する方法

webサイト管理者がクローラに対して特定のページをクロールしないように指示できるらしい
robots.txt
robots metaタグ

- robots.txt
robots.txtはwebサイトのトップディレクトリに配置されるテキストファイルだそうで...
試しにpixivでしらべてみたら...
https://www.pxiv.net/robots.txt  

あった  

```txt
User-agent: *
Disallow: /rpc/index.php?mode=profile_module_illusts&user_id=*&illust_id=*
Disallow: /ajax/illust/*/recommend/init
Disallow: *return_to*
Disallow: /?return_to=
Disallow: /login.php?return_to=
Disallow: /index.php?return_to=

Disallow: /artworks/unlisted/*

Disallow: /tags/* * *
Disallow: /tags/*%20*%20*

Disallow: /users/*/followers
Disallow: /users/*/mypixiv
Disallow: /users/*/bookmarks
Disallow: /novel/comments.php?id=
Disallow: /novels/unlisted/*

Disallow: /en/group

Disallow: /en/tags/* * *
Disallow: /en/tags/*%20*%20*

Disallow: /en/search/

Disallow: /en/users/*/followers
Disallow: /en/users/*/mypixiv
Disallow: /en/users/*/bookmarks
Disallow: /en/novel/comments.php?id=

Disallow: /fanbox/search
Disallow: /fanbox/tag
```
robots.txtに書いてあるからって、クローラは無視をすることができるということと
robots.txtは公開されている情報なので「ここのURLは機密だからアクセスするな」という情報はむしろ記載することはできない
つまり強制力はないけれどクローラは必ず参照しないといけない内容ってわけだ

ってことで予めこのURLはクロールしていいのかってのを確認しないとねってわけで
その時に役に立つのがPython標準ライブラリのurllib.robotparser


### Webページの自動操作

webサイトへログインするときはCoockieでセッションを維持する
セッションを維持する方法など
- RequestsのSessionオブジェクト
- MechanicalSoup(BeautifulSoup)

MechanicalSoupを使ってクラシルにログインしてお気に入り登録した料理とレシピとかを一覧表示させる
クラシル会員登録
？そもそもクラシルログイン後にスクレイピングしていいのか？確認
https://www.kurashiru.com/robots.txt
ログインページまではスクレイピング可能
ただし/account/が挟まるURLはスクレイピングダメ

ログインしてセッションを保てているのかの確認ととりあえずなんかスクレイピングできればいいので
スクレイピング禁止領域を侵さないようにやってみる


### sessionとCookieを勉強して!

### Git 履歴

まず、一旦Githubにアップしてしまった内容は、過去の変更履歴含めて世界中の人に知れ渡ることになる

例
```
git clone wainorepositorie
# これまでの変更履歴が詳細にわかる
git log -p
```

ということでそのﾘﾓｰﾄﾘﾎﾟｼﾞﾄﾘを削除するほかない

復元方法
```Python
# ローカルで
# 履歴が残っているので.gitを削除
rm -rf .git
# 再度
git init
# Githubで
#リポジトリの削除
# リポジトリの再作成

```

ついでに/LearnPuppeteer/も削除した

### Python: command line から文字列を受け取ってプログラムで利用する

Node.jsのyargsみたいなのキボンヌ

`argparse`というものがいいと聞いた
https://stackoverflow.com/questions/20063/whats-the-best-way-to-parse-command-line-arguments

標準モジュールである
https://docs.python.org/ja/3/howto/argparse.html


### chromedriverをインストールしたけどそんなやついないっていわれる件

☆chromedriverインストールにおけるいろいろ
Ubuntu-20.04

流れ

sudo apt-get update
cd /tmp/
curl -O <https://chromedriver.storage.googleapis.com/index.html?path=91.0.4472.19/ここの最新バージョンのURL>
unzip chromedriver_linux64.zip
sudo mv chromedriver <PATHが通っているところならばどこでもいいらしい。たとえば/usr/local/bin/>
(
PATHが通っている場所の確認方法
echo $PATH
見方はググれ
)
ここでchromedriver --versionしても、は？それなに？って言われてまるでpathが通っていないかのように言われる
エラー内容を確認すると
chromedriver: error while loading shared libraries: libnss3.so: cannot open shared object file: No such file or directory
ということでなんかlibnss3ってものが関係している模様
それでlddというコマンドでchromedriverに必要なドライバを一覧表示できる模様
ldd /user/local/bin/chromedriver
するといくつかのライブラリだかドライバ高がnot foundと表示されるのがわかる
とにかくそいつらをインストール
sudo apt-get isntall libnss3

ldd /usr/local/bin/chromedriver
not foundがなくなった
chromedriver --version
バージョン情報が表示された


### chromium-browserをインストールしたけどそんな奴ないって言われる件

根本的な原因はwsl2が`snap`というパッケージ管理プログラム？を使えないから
`systemd`が使えない件と同じ問題でつまり深刻である

- 経緯
sample_codes/5-6/selenium_google.pyを実行したら`chromium-browser`は機能していないというエラー

```
(The process started from chrome location /usr/bin/chromium-browser is no longer running, so ChromeDriver is assuming that Chrome has crashed.)
```
Ubuntuのbashで
```
$ chromium-brower --version

Command '/usr/bin/chromium-browser' requires the chromium snap to be installed.
Please install it with:

snap install chromium
```
とのこと。
~~つまり`snap`で`chromium`をインストールしろと~~
snapでinstallして～っていうのは定型句っぽい営業で、気にしなくてよかったかも
**とにかくsanpdはほっといてchromium-browserが認識されない問題にフォーカスする**

<!-- ```
$ sudo snap install chromium
error: cannot communicate with server: Post http://localhost/v2/snaps/chromium: dial unix /run/snapd.socket: connect: no such file or directory
```
とにかく`snapd`が動いちゃいない
参考：　公式のGithub Issue
https://github.com/microsoft/WSL/issues/5126 -->

参考になった
https://ubunlog.com/ja/chrome-algunas-formas-de-instalarlo-en-ubuntu-21-04/
https://intoli.com/blog/running-selenium-with-headless-chrome/

chromium-browserをやめて上記のwebサイトの情報通り、安定版chromeをインストールした
headlessで使えるよ
snapdいらないよ
chromedriver_binaryは必要かも
とにかくseleniumを使えるようになった...やっとか...

chromedriverのinstallation
google-chrome-stable_

### Seleniumを使った開発記

optionは"headless"じゃないとエラーになる

#### とにかくchromeをヘッドレスで使うためのインストレーションのハードルが高すぎる

- chromedriverのinstallation

```terminal
cd /tmp/

```
- google-chromeのinstallation (NOT chromium-browser)
google-chrome-stable_current_amd64.deb
- chromedriver-binaryのinstallation



#### コードにクロームとかをどうやってimportするのかとか

#### seleniumでブラウザを起動させる

。。。解決しない～これだからテキスト身ながらの開発は嫌なんだ～方法が古くなるから～


なんかいろんなエラーは割とimportの仕方とかで起こる起こらないがある
firefoxで
たぶんだけどfirefox自体と、そのドライバがないとseleniumでは使えないかも？
FireFoxをUbuntuにインストールする

### BeautifulSoup4 

```Python
 while(i2<7):
    # 
    title = td.find(class_="title-p").text.replace("\n", "", 3)
    pfm = td.find(class_="rp").text.replace("\n", "", 4)
    c = td.get("class")[0]
```
この辺の修正

`td.find(class_="title-p")`では取得できない
理由はclass名が存在しないから
最終的には番組名を取得できればいい
```Python
    title = td.select("")
```


```HTML
<td class="is-ag is-repeat" rowspan="60">
<div class="program-wrap">
<div class="weeklyProgram-time">6:00</div>
<div class="weeklyProgram-content">
<a href="https://www.joqr.co.jp/qr/program/thecatch/">A&amp;G ARTIST ZONE樋口楓のTHE CATCH</a>
<i class="icon_program-movie"></i>
<span class="personality">
<a href="/qr/personality/higuchikaede/">樋口楓</a>
</span>
</div>
</div>
</td>
```


上記のように番組名は
`div.weeklyProgram-content a`のinnerTextなので次の通りにする


```Python
    title = td.select("div.weeklyProgram-content a").text
```

例外が発生しました: AttributeError
ResultSet object has no attribute 'text'. You're probably treating a list of elements like a single element. Did you call find_all() when you meant to call find()?

まちがいまちがい
.select()は配列を返すので


```Python
    title = td.select("div.weeklyProgram-content a")[0].text
```
取得できた!



### パターン化

番組情報のHTML情報が必ずどれも同じとは限らないらしい
パターン化させる

```HTML
pe/playground/ag.py 
<td class="is-ag is-repeat" rowspan="60">
    <div class="program-wrap">
        <div class="weeklyProgram-time">6:00</div>
        <div class="weeklyProgram-content">
            <a href="https://www.joqr.co.jp/qr/program/thecatch/">A&amp;G ARTIST ZONE樋口楓のTHE CATCH</a>
            <i class="icon_program-movie"></i>
            <span class="personality">
                <a href="/qr/personality/higuchikaede/">樋口楓</a>
            </span>
            </div>
        </div>
</td>

<td class="is-ag is-repeat" rowspan="60">
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

<td class="is-ag is-repeat" rowspan="60">
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

<td class="is-ag is-repeat" rowspan="60">
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

<td class="is-ag is-repeat" rowspan="60">
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

<!-- パターン外 -->
<td class="is-ag is-repeat" rowspan="60">
<div class="program-wrap">
<div class="weeklyProgram-time">6:00</div>
<div class="weeklyProgram-content">
<a href="https://www.joqr.co.jp/qr/program/ag_sp/">超！A&amp;G+ スペシャル</a>
</div>
</div>
</td>
```

パターン外は`span.personality`がない
なので条件分岐を設ける

```Python

                # 出演者(いない場合あり)  この条件分岐は大丈夫なのか？
                if td.select("span.personality a") is not None:
                    pfm = td.select("span.personality a")[0].text.replace("\n", "", 4)
                else :
                    pfm = "なし"
```
`if td.select("span.personality a") is not None:`の部分が正しいのか試していない..
IndexError: list index out of range  

```HTML
<td class="is-ag" rowspan="30">
<div class="program-wrap">
<div class="weeklyProgram-time">12:30</div>
<div class="weeklyProgram-content">
<a href="https://www.joqr.co.jp/qr/program/rrr/">森久保祥太郎 presents IRONBUNNY'S ROCK ROCKER ROCKEST</a>
<span class="personality">
<a href="/qr/personality/morikuboshotaro/">森久保祥太郎</a>
</span>
<span class="personality">
<a href="/qr/personality/ediee-ironbunny/">Ediee Ironbunny（IRONBUNNY）</a>
</span>
<span class="personality">
<a href="/qr/personality/kotono/">Kotono（IRONBUNNY）</a>
</span>
<span class="personality">
<a href="/qr/personality/minami/">Minami（IRONBUNNY）</a>
</span>
</div>
</div>
</td>

<td class="is-ag is-repeat" rowspan="20">
<div class="program-wrap">
<div class="weeklyProgram-time">12:40</div>
<div class="weeklyProgram-content">
<a href="https://www.joqr.co.jp/qr/program/yonayona/">鷲崎健のヨルナイト×ヨルナイト</a>
<i class="icon_program-movie"></i>
<span class="personality">
<a href="/qr/personality/washizakitakeshi/">鷲崎健</a>
</span>
<span class="personality">
<a href="/qr/personality/monthlyguest/">マンスリーゲスト</a>
</span>
</div>
</div>
</td>

<td class="is-ag is-repeat" rowspan="20">
<div class="program-wrap">
<div class="weeklyProgram-time">12:40</div>
<div class="weeklyProgram-content">
<a href="https://www.joqr.co.jp/qr/program/yonayona/">鷲崎健のヨルナイト×ヨルナイト</a>
<i class="icon_program-movie"></i>
<span class="personality">
<a href="/qr/personality/washizakitakeshi/">鷲崎健</a>
</span>
<span class="personality">
<a href="/qr/personality/sawaguchikeiko/">沢口けいこ</a>
</span>
</div>
</div>
</td>
```  

- `span.personality`は複数ある場合があるのでその場合にも対応すること
- その前にエラー箇所前の全ての部分について正しく動作しているのかチェック

#### 生放送か、再放送か、動画番組か等

```HTML
    <!-- 再放送ならば、.is_repeatのクラス名がつく -->
    <td rowspan="30" class="is-ag is-repeat">
        <div class="program-wrap">
          <div class="weeklyProgram-time">7:30</div>
          <div class="weeklyProgram-content">
            <a href="https://www.joqr.co.jp/qr/program/fuwa/">井澤美香子・諏訪ななかのふわさた</a>
            <!-- 動画番組ならば、下記のアイコンタグがあるはず -->
            <i class="icon_program-movie"></i>
            <span class="personality">
              <a href="/qr/personality/izawamikako/">井澤美香子</a>
            </span>
            <span class="personality">
              <a href="/qr/personality/suwananaka/">諏訪ななか</a>
            </span>
          </div>
        </div>
      </td>

      <td rowspan="60" class="is-ag">
        <div class="program-wrap">
          <div class="weeklyProgram-time">20:00</div>
          <div class="weeklyProgram-content">
            <a href="https://www.joqr.co.jp/qr/program/cueanda/">A&amp;G NEXT ICON 超！CUE！&amp;A</a>
            <!-- 生放送ならば以下のアイコンタグが付く -->
            <i class="icon_program-live"></i>
            <i class="icon_program-movie"></i>
            <span class="personality">
              <a href="/qr/personality/uchiyamayurina/">内山悠里菜</a>
            </span>
          </div>
        </div>
      </td>
```
とりあえず要素.get()の関数の正体がわからん


- 動画放送なのか調べる方法
```HTML
            <!-- 動画番組ならば、下記のアイコンタグがあるはず -->
            <i class="icon_program-movie"></i>
```
td要素にこれが含まれていれば動画だねってわけ
```Python
 isMovie = True if td.select('i.icon_program-movie') else False
```


- Error箇所: 放送休止の場合、`div.weeklyProgram a`が存在しない...

放送休止の場合、tdタグに`.is-joqr`が含まれる
修正中102行目...
条件分岐の文法とか覚えないとわからん


```HTML
<div class="weeklyProgram-time">26:30</div>
ラジオどっとあい 202106110230 0230
<td class="is-ag" rowspan="30">
<div class="program-wrap">
<div class="weeklyProgram-time">26:30</div>
<div class="weeklyProgram-content">
<a href="https://www.joqr.co.jp/qr/program/murashiro/">村瀬くんと八代くん</a>
<span class="personality">
<a href="/qr/personality/muraseayumu/">村瀬歩</a>
</span>
<span class="personality">
<a href="/qr/personality/yashirotaku/">八代拓</a>
</span>
</div>
</div>
</td>

<td class="is-joqr" colspan="4" rowspan="180">
<div class="program-wrap">
<div class="weeklyProgram-time">27:00</div>
<div class="weeklyProgram-content">
            放送休止
          </div>
</div>
</td>


```


### ag.pyで番組が正しく取得できていない件

create_table()関数のアルゴリズムを修正する必要がある

- Pyxisの夜空の下 de Meeting

月曜日のみ12:30~12:40と24:30~24:40で登録できている
しかし
実際には月曜日から木曜日までこの番組は12:30~12:40と0:30~0:40に放送があり
火曜日以降が取得できていないことがわかる

他、
24:40~24:57まで夜ナイト夜ナイトが月～木あるけど月曜日しか取得できていない
24:57~25:00の番組が同じく月曜日から木曜日まであるけど月曜日しか取得できていない


Pyxisの夜空の下 de MeetingはHTML要素`td[colspan="4"]`で取得される
ファンキルタガタメ3分番組は同様に`td[colspan="5"]`で取得される  
つまりcolspanが指定されている要素は2日間以上にまたがって表示されている番組である


