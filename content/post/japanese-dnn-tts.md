+++
date = "2017-08-16T23:10:56+09:00"
draft = false
title = "DNN音声合成のためのライブラリの紹介とDNN日本語音声合成の実装例"
tags  = [ "Speech synthesis", "DNN", "Python"]
categories = ["Speech synthesis", "Python"]
+++

[nnmnkwii](https://github.com/r9y9/nnmnkwii) というDNN音声合成のためのライブラリを公開しましたので、その紹介をします。

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr"><a href="https://t.co/p8MnOxkVoH">https://t.co/p8MnOxkVoH</a> Library to build speech synthesis systems designed for easy and fast prototyping. Open sourced:)</p>&mdash; 山本りゅういち (@r9y9) <a href="https://twitter.com/r9y9/status/897117170265501696">August 14, 2017</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

ドキュメントの最新版は https://r9y9.github.io/nnmnkwii/latest/ です。以下に、いくつかリンクを貼っておきます。

- [なぜ作ったのか、その背景の説明と設計 (日本語)](https://r9y9.github.io/nnmnkwii/v0.0.1/design_jp.html)
- [クイックガイド](https://r9y9.github.io/nnmnkwii/v0.0.1/nnmnkwii_gallery/notebooks/00-Quick%20start%20guide.html)
- [DNN英語音声合成のチュートリアル](https://r9y9.github.io/nnmnkwii/v0.0.1/nnmnkwii_gallery/notebooks/tts/01-DNN-based%20statistical%20speech%20synthesis%20(en).html)

よろしければご覧ください[^1]。

[^1]: リンク切れが怖いので、v0.0.1のリンクを貼りました。できれば、最新版をご覧ください。 https://r9y9.github.io/nnmnkwii/latest/ こちらからたどれます

ドキュメントは、だいたい英語でお硬い雰囲気で書いたので、この記事では、日本語でカジュアルに背景などを説明しようと思うのと、（ドキュメントには英語音声合成の例しかないので）HTSのデモに同梱のATR503文のデータセットを使って、**DNN日本語音声合成** を実装する例を示したいと思います。結果だけ知りたい方は、音声サンプルが下の方にあるので、適当に読み飛ばしてください。

## なぜ作ったのか

一番大きな理由は、僕が **対話環境（Jupyter, IPython等）** で使えるツールがほしかったからです[^2]。
僕は結構前からREPL (Read-Eval-Print-Loop) 信者で、プログラミングのそれなりの時間をREPLで過ごします。
IDEも好きですし、emacsも好きなのですが、同じくらいJupyterや[Julia](https://github.com/JuliaLang/julia)のREPLが好きです。
用途に応じて使い分けますが、特に何かデータを分析する必要があるような時に、即座にデータを可視化できるJupyter notebookは、僕にとってプログラミングに欠かせないものになっています。

ところが、HTSの後継として生まれたDNN音声合成ツールである [Merlin](https://github.com/CSTR-Edinburgh/merlin) は、コマンドラインツールとして使われる想定のもので、僕の要望を満たしてくれるものではありませんでした。
とはいえ、Merlinは優秀な音声研究者たちの産物であり、当然役に立つ部分も多く、使っていました。しかし、ことプロトタイピングにおいては、やはり対話環境でやりたいなあという思いが強まっていきました。

新しく作るのではなく、Merlinを使い続ける、Merlinを改善する方針も考えました。僕がMerlinを使い始めた頃、Merlinはpython3で動かなかったので、動くように [プルリク](https://github.com/CSTR-Edinburgh/merlin/pull/141) を出したこともあるのですが、まぁレビューに数カ月もかかってしまったので、これは新しいものを作った方がいいな、と思うに至りました。

以上が、僕が新しくツール作ろうと思った理由です。

[^2]: 知っている人にはまたか、と言われそう

## 特徴

さて、Merlinに対する敬意と不満から生まれたツールでありますが、その特徴を簡単にまとめます。

- **対話環境** での使用を前提に、設計されています。コマンドラインツールはありません。ユーザが必要に応じて作ればよい、という考えです。
- DNN音声合成のデモをノートブック形式で提供しています。
- 大規模データでも扱えるように、データセットとデータセットのイテレーション（フレーム毎、発話毎の両方）のユーティリティが提供されています
- **Merlinとは異なり、音響モデルは提供しません**。自分で実装する必要があります（が、今の時代簡単ですよね、lstmでも数行で書けるので
- 任意の深層学習フレームワークと併せて使えるように、設計されています[^4]（[autogradパッケージ](https://r9y9.github.io/nnmnkwii/latest/references/autograd.html)のみ、今のところPyTorch依存です
- 言語特徴量の抽出の部分は、Merlinのコードをリファクタして用いています。そのせいもあって、Merlinのデモと同等のパフォーマンスを簡単に実現できます。

[^4]: 音響モデルの提供をライブラリの範囲外とすることで、間接的に達成されています

## 対象ユーザ

まずはじめに、大雑把にいって、音声合成の研究（or その真似事）をしてみたい人が主な対象です。
自前のデータを元に、ブラックボックスでいいので音声合成エンジンを作りたい、という人には厳しいかもしれません。その前提を元に、少し整理します。

### こんな人におすすめです

- Jupyter notebookが好きな人
- REPLが好きな人
- Pythonで処理を完結させたい人
- オープンソースの文化に寛容な人[^3]
- 音声合成の研究を始めてみたい人

[^3]: バグにエンカウントしたらすぐに使うのをやめてしまう人には、向いていないかもしれません。

### こんな人には向かないかも

- コマンドラインツールこそ至高な人
- パイプライン処理こそ至高な人
- SPTKのコマンドラインツール至高な人
- 信頼のある機関が作ったツールしか使わない人[^5]
- 音声研究者ガチ勢で、自前のツールで満足している人

[^5]: Merlinは、エジンバラ大学の優秀な研究者の方々によって作られています

## DNN日本語音声合成の実装例

さて、前置きはこのくらいにして、日本語音声合成の実装例を示します。シンプルなFeed forwardなネットワークと、Bi-directional LSTM RNNの2パターンを、ノートブック形式で作成しました。

ソースコードは、 https://github.com/r9y9/nnmnkwii_gallery にあります。以下に、現状点での直リンク（gitのコミットハッシュがURLに入っています）を貼っておきます。nbviewerに飛びます。

- [Feed forwardなネットワークを使った音声合成のノートブックへの直リンク](http://nbviewer.jupyter.org/github/r9y9/nnmnkwii_gallery/blob/bd4bd260eb22d0000ac2776b204b3a5afb693c49/notebooks/tts/jp-01-DNN-based%20statistical%20speech%20synthesis.ipynb)
- [Bi-directional LSTM RNNを使った音声合成のノートブックへの直リンク](http://nbviewer.jupyter.org/github/r9y9/nnmnkwii_gallery/blob/bd4bd260eb22d0000ac2776b204b3a5afb693c49/notebooks/tts/jp-02-Bidirectional-LSTM%20based%20RNNs%20for%20speech%20synthesis.ipynb)

興味のある人は、ローカルに落として実行してみてください。CUDA環境があることが前提ですが、通常のFeed forwardのネットワークを用いたデモは、
特徴抽出の時間（初回実行時に必要）を除けば、5分で学習&波形生成が終わります。Bi-directional LSTMのデモは、僕の環境 (i7-7700K, GTX 1080Ti) では、約2時間で終わります。GPUメモリが少ない場合は、バッチサイズを小さくしなければならず、より時間がかかるかもしれません。

### データセット

今回は、HTSのNIT-ATR503のデモデータ ([ライセンス](https://github.com/r9y9/nnmnkwii_gallery/blob/4899437e22528399ca50c34097a2db2bed782f8b/data/NIT-ATR503_COPYING)) を拝借します。ライブラリを使って音声合成を実現するためのデータとして、最低限以下が必要です。

- (state or phone level) フルコンテキストラベル
- Wavファイル
- 質問ファイル（言語特徴量の抽出に必要）

上2つは、今回はHTSのデモスクリプトからまるまるそのまま使います（※HTSのデモスクリプトを回す必要はありません）。質問ファイルは、コンテキストクラスタリングに使われる質問ファイルを元に、質問数を（本当に）適当に減らして、Merlinのデモの質問ファイルからCQSに該当する質問を加えて、作成しました。
フルコンテキストラベルには、phone-levelでアライメントされたものを使いますが、
state-levelでアライメントされたものを使えば、性能は上がると思います。今回は簡単のためにphone-levelのアライメントを使います。

質問の選定には、改善の余地があることがわかっていますが、あくまでデモということで、ご了承ください。

### 音声合成の結果

全体の処理に興味がある場合は別途ノートブックを見てもらうとして、ここでは結果だけ貼っておきます。
HTSのデモからとってきた例文5つに対して、それぞれ

- Feed forward neural networks (MyNetとします) で生成したもの
- Bi-directional LSTM recurrent neural networks (MyRNNとします)で生成したもの
- HTSデモで生成したもの (HTSとします)

の順番に、音声ファイルを添付しておきます。聴きやすいように、soxで正規化しています。それではどうぞ。

1 こんにちは

MyNet

<audio controls="controls" >
<source src="/audio/jp-01-tts/phrase01.wav" type="audio/wav" autoplay/>
Your browser does not support the audio element.
</audio>

MyRNN

<audio controls="controls" >
<source src="/audio/jp-02-tts/phrase01.wav" autoplay/>
Your browser does not support the audio element.
</audio>

HTS

<audio controls="controls" >
<source src="/audio/hts_nit_atr503_2mix/phrase01.wav" autoplay/>
Your browser does not support the audio element.
</audio>

2 それではさようなら

MyNet

<audio controls="controls" >
<source src="/audio/jp-01-tts/phrase02.wav" autoplay/>
Your browser does not support the audio element.
</audio>

MyRNN

<audio controls="controls" >
<source src="/audio/jp-02-tts/phrase02.wav" autoplay/>
Your browser does not support the audio element.
</audio>

HTS

<audio controls="controls" >
<source src="/audio/hts_nit_atr503_2mix/phrase02.wav" autoplay/>
Your browser does not support the audio element.
</audio>

3 はじめまして

MyNet

<audio controls="controls" >
<source src="/audio/jp-01-tts/phrase03.wav" autoplay/>
Your browser does not support the audio element.
</audio>

MyRNN

<audio controls="controls" >
<source src="/audio/jp-02-tts/phrase03.wav" autoplay/>
Your browser does not support the audio element.
</audio>

HTS

<audio controls="controls" >
<source src="/audio/hts_nit_atr503_2mix/phrase03.wav" autoplay/>
Your browser does not support the audio element.
</audio>

4 ようこそ名古屋工業大学へ

MyNet

<audio controls="controls" >
<source src="/audio/jp-01-tts/phrase04.wav" autoplay/>
Your browser does not support the audio element.
</audio>

MyRNN

<audio controls="controls" >
<source src="/audio/jp-02-tts/phrase04.wav" autoplay/>
Your browser does not support the audio element.
</audio>

HTS

<audio controls="controls" >
<source src="/audio/hts_nit_atr503_2mix/phrase04.wav" autoplay/>
Your browser does not support the audio element.
</audio>

5 今夜の名古屋の天気は雨です

MyNet

<audio controls="controls" >
<source src="/audio/jp-01-tts/phrase05.wav" autoplay/>
Your browser does not support the audio element.
</audio>

MyRNN

<audio controls="controls" >
<source src="/audio/jp-02-tts/phrase05.wav" autoplay/>
Your browser does not support the audio element.
</audio>

HTS

<audio controls="controls" >
<source src="/audio/hts_nit_atr503_2mix/phrase05.wav" autoplay/>
Your browser does not support the audio element.
</audio>

一応HTSで生成された音声も貼りましたが、そもそも実験条件が違いすぎる[^6]ので、単純に比較することはできません。
せめて HTS ＋ STRAIGHTと比較したかったところですが、僕はSTRAIGHTを持っていないので、残念ながらできません、悲しみ。

しかし、それなりにまともな音声が出ているような気がします。

[^6]: f0分析、スペクトル包絡抽出、非周期性成分の抽出法がすべてことなる、またポストフィルタの種類も異なる。条件をある程度揃えて比較するのが面倒そうだったので（なにせHTSを使ったモデルの学習は数時間かかるし…）、手を抜きました、すいません

## おわりに

いままでさんざん、汎用性とは程遠いクソコードを書いてきましたが、今回こそは少しはマシなものを作ろうと思って作りました。僕以外の人にも役に立てば幸いです。あと、この記事を書いた目的は、いろんな人に使ってみてほしいのと、使ってみた結果のフィードバックがほしい（バグ見つけた、そもそもエラーで動かん、ここがクソ、等）ということなので、フィードバックをくださると助かります。よろしくお願いします。

ちなみに名前ですが、ななみ or しちみと読んでください。何でもいいのですが、常識的に考えてあぁ確かに読めないなぁと思いました（小並感）。ドキュメントにあるロゴは、昔三次元物体追跡の実験をしていたときに撮ったく某モンのポイントクラウドですが、そのうち七味的な画像に変えようと思っています。適当ですいません
