# Note about HLS and .m3u8 file

> HLSはMPEG-DASHに似ており、ストリーム全体を一連の小さなHTTPベースのファイルダウンロードに分割し、
> それぞれが制限のない可能性のあるトランスポートストリーム全体の短いチャンクを1つダウンロードします。
> さまざまなビットレートでエンコードされた利用可能なストリームのリストは、
> 拡張M3Uプレイリストを使用してクライアントに送信されます  

つまり
ストリーム配信するビデオを、HLSでは分割してクライアントへ送信している
ストリームは小さなチャンクに分割されてクライアントはそのチャンクをダウンロードする
クライアントは分割して送信されるチャンクをクライアントで「再構成」する
この再構成に必要なのが「プレイリスト」で要はバラバラなチャンクでどの順番でくっつけたら
もとのファイルを再構成できるのか書いてある設計図である


### Architecture

HLSの構成コンポーネント

1. サーバ 
入力ビデオフローを、配信に適した形式で体系化してカプセル化します。
次に、さまざまなファイルにセグメント化して配布の準備をします。
取り込みの過程で、ビデオはエンコードおよびセグメント化されて、
ビデオフラグメントとインデックスファイルが生成されます。 

- エンコーダー:
ビデオファイルをH.264形式でコード化し、オーディオをAAC、MP3、AC-3、またはEC-3でコード化します。これは、MPEG-2トランスポートストリームまたはMPEG-4_Part_14によってカプセル化されて運ばれます。 
- セグメンター：
ストリームを同じ長さのフラグメントに分割します。また、.m3u8として保存された、断片化されたファイルの参照を含むインデックスファイルを作成します。 

つまり、サーバは入力ビデオを配信に適した形式に変換する
映像と音声はエンコードされ、HTTP通信に適した形式へカプセル化する
ストリームを同じ長さに分割する（.tsセグメントファイルの生成）
分割されたファイルのプレイリストの生成（.m3u8ファイルの生成）




2. ディストリビューター 標準のWebサーバーによって形成され、クライアントからの要求を受け入れ、ストリーミングに必要なすべてのリソース（.m3u8プレイリストファイルと.tsセグメントファイル）を配信します。 

3. クライアント すべてのファイルとリソースをリクエストしてダウンロードし、それらを組み立てて、連続フロービデオとしてユーザーに提示できるようにします。クライアントソフトウェアは、最初にURLを介してインデックスファイルをダウンロードし、次に利用可能ないくつかのメディアファイルをダウンロードします。再生ソフトウェアはシーケンスを組み立てて、ユーザーに継続して表示できるようにします。

つまりHLSを用いたストリーミング配信を見るには
クライアントはHLS配信しているリソースを再構成できる環境が必要である
だいたいのブラウザが採用しているのでだいたい問題なく見れる
クライアントは.tsファイルと.m3u8ファイルの情報をもとに配信映像・音声を再構成する


