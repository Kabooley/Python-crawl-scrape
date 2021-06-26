# How to use 


まどろっこしい。
ページ丸っと翻訳して読み解く方に時間を割いて

## 目標：ストリーミング配信されている`.m3u8`ファイルをローカルに保存するよ



## 参考

公式Documentation:
https://www.ffmpeg.org/ffmpeg.html#Synopsis

見つけたサイト：
https://blog.katsubemakito.net/macos/ffmpeg

https://qiita.com/uupaa/items/c76c76cb149470bf89f2

## installation to Ubuntu-20.04

https://goto-linux.com/ja/2019/8/22/ubuntu-20.04-ffmpeg%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB/


## とにかく公式のDocumentationを読み解く

`ffmpeg`は生放送の音声・動画を変換してくれる（ソフトウェアです）

ffmpegは、-iオプションで指定された任意の数の入力「ファイル」（通常のファイル、パイプ、ネットワークストリーム、グラブデバイスなど）から読み取り、

任意の数の出力「ファイル」に書き込みます

各入力または出力URLには原則として様々なタイプのストリームをいくつでも含めることができる

どの入力から度の出力に入るストリームを選択するかは、自動または`-map`オプションで指定できる


### ファイルの数はいくつでも

入力ファイル(ストリーム)、出力ファイル（ストリーム）はそれぞれいくつでも含めることができる

### どの入力をどの出力につなげるのかの指定

何も指定していなければ自動で
`-map`オプションで明示的に指定可能

### 複数ファイルを指定しているばあにどのファイルを個別に参照するのか

インデックス番号で指定する

オプションで入力ファイルを参照するにはそれらのインデックス番号を使用する

index番号なので一番初めのファイルは`0`, そのつぎは`1`のように

`2:3`で3番目のファイルと4番目のファイルを参照する

### オプションの適用対象

オプション ファイルの順番
オプションの次に指定されたファイルにそのオプションがファイルに適用される
なので
順番は重要だよという話

### 順番：入力ファイルと出力ファイルはまとめて

入力ファイルと出力ファイルは混ぜないで
入力ファイルをすべて書いてから出力ファイルを書きましょう


### samples

```terminal
>$ ffmpeg -i input.avi -b:v 64k -bufsize 64k output.avi
```
入力ファイル: `input.avi`
出力ファイル: `output.avi`
`-i`オプションの対象: `input.avi`
`-b:v 64k -bufsize 64k`の意味：


## Options

### Stream Specifiers ストリーム特定子

例
`-codec:a:1 ac3`

意味: 
二番目のファイル（またはストリーム）に一致する`a:1`に対して、`ac3`コーデックを適用する

説明:
ストリーム指定子は通常、オプションに追記される形で記載される
コロンで区切られた文字列で例えば上記のような感じ

例
`-b:a 128k`

上記のようにストリームのインデックスを特定しない場合、そのストリームすべてにオプションを適用させる

例
`-codec copy`

上記のように、空白の（何も指定しない）場合、すべてのストリームにオプションが適用される


#### stream_index

`-threads:1 4`
"2番目のストリームをカウント４のスレッドにセットする"
下記のように`stream_type`が指定されているうえで利用する場合
たとえば`v`にマッチするストリームのうちからｲﾝﾃﾞｯｸｽで選択する形になる
（つまり`stream_type`が優先される形）


#### stream_type[:additional_stream_specifier]

- v or V: video      `v`はすべてのビデオストリームに一致する `V`はサムネイルやピクチャー、カバーアートにアタッチされていないビデオストリームの身に一致する

- a: audio
- s: subtitle
- d: data
- t: attatchments

もしも`additional_stream_specifier`が使用されている場合
`additional_stream_specifier`と一致するストリームと、
`additional_stream_specifier`のタイプを持つストリームと一致する

#### p:program_id[:additional_stream_specifier]



## Detailed Description

inputfile
--> `demuxer`
--> `decoder`
--> `decode frames`
--> `encoder`
--> `encoded data packets`
--> `muxer`
--> outputfile

トランスコーディング・プロセスによる各出力は下記の画像の通りに説明可能である
![detailed_description_1]("./ffmpeg_detailed_description_1.PNG")


- inputファイルの処理：
`libavformat`ライブラリ(`demuxers`含む)を呼び出して`input`ファイルを読み込み
ファイルの中からエンコードされたデータを含むパケットを取得する

もしも複数ファイルが存在する場合、
アクティブな入力ストリームのうちもっとも低いタイムスタンプをトラッキングすることで、
複数ストリームを同期しようとする

取得したパケットはデコーダへ送られる
デコーダは非圧縮フレームを生成する(フィルタリングを施すこともできる）

### filtering

エンコーディング前に、`libavfilter`ライブラリを使って生のオーディオや動画を処理することができる
複数の連鎖フィルターがフィルターグラフを形成する
ffmpegは`simple filtergraph`と`complex filtergraph`の2種類のフィルターグラフに区別する

### simple filtergraph

単一input-file、単一output-file
`per-stream -filter`オプションでsimple filtergraphを命令できる


### complex filtergraph

複数input-file、非同数複数output-fileになる場合がある
`-filter_complex`オプションで指定する このオプションはｸﾞﾛｰﾊﾞﾙである
故に単一ストリームにのみに対して適用できない



### Stream Copy

stream copyは`-codec`オプションに`copy`パラメータを渡したときのモードである
でコードとエンコードを省略させてdemuxingとmuxingのみさせる

これはコンテナのフォーマットの変更やコンテナレベルのメタデータの変更を実施するのに便利である

エンコードとでコードがないからとっても処理が早くて質のロスがない
いっぽうで様々の理由でうまくいかない場合が多い


## Stream Selection

streamの選択方法について
`-map`オプションは各outputファイルに対して手動のストリーム選択操作を実現する

`-map`をスキップして自動選択させることも可能である
-vn / -an / -sn / -dnオプションを使用すると、複雑なフィルターグラフの出力であるストリームを除いて、手動でマッピングするか自動で選択するかにかかわらず、ビデオ、オーディオ、字幕、データストリームの包含をスキップできます。


## 実際に超a&g+からffmpegでストリーミング配信を保存してみる

コマンド例
```terminal
>$ ffmpeg -i {URL} -t {DURATION} -movflags faststart -ar 48000 -c copy {OUTPUT_FILE}
```


URLはインプットストリーム
DURATIONは番組の時間
OUTPUT_FILEは出力ファイル名である

なんかyoutubeのくっそ怪しい動画をいくつか参考にしてみよう
これとか？
https://www.youtube.com/watch?v=SC4cZzqJhAQ&t=185s


#### はじめてやってみた

Qiitaの記事を参考にターミナルでやってみた

```terminal
$ ffmpeg -i https://www.uniqueradio.jp/agplayer5/hls/mbr-0.m3u8 -movflags faststart -c copy -bsf:a aac_adtstoasc first_rec.mp4
```

問題
- 超a&g+のHLSのURLをinputにしたら、とくに番組ごとにURLは変更されないらしく、永遠に取得し続けてしまう。なので時間指定しないといかんな
- 映像がとれていない。

