---
layout: post
title: Tokyo.Scipyに参加してきた
date: 2014-08-05
comments: true
categories: python scipy
---

## [Tokyo.SciPy](https://github.com/tokyo-scipy/archive)

ハッシュタグ: [#tokyoscipy](https://twitter.com/search?q=%23tokyoscipy&src=tyah)

> Tokyo.Scipy は科学技術計算で Python を利用するための勉強会です．

とのことです。最近、python/numpy/scipyによくお世話になっているので、参加してみました。雑感をメモしておきます。

## [Tokyo.Scipy 006](https://github.com/tokyo-scipy/archive/tree/master/006)

第6回のようでした。プログラムだけさっとまとめると、

- そこそこ大規模Python並列/パイプライン処理入門 w/o MapReduceレジーム (柏野雄太 @yutakashino) 45分
- 初心者が陥るN個の罠。いざ進めNumpy/Scipyの道 (@nezuq) 15分
- Making computations reproducible (@fuzzysphere) 30分
- IPython Notebookで始めるデータ分析と可視化 (杜世橋 @lucidfrontier45) 30分
- PyMCがあれば，ベイズ推定でもう泣いたりなんかしない (神嶌敏弘 @shima__shima) 45分

という感じ。僕的には、@shima__shima 先生の発表が目当てだった

## 雑感

- 今回（？）はscipyの話はほとんどなかった。pythonを使った科学技術計算に関する幅広いトピックを扱ってる印象。
- ipython はやっぱ便利ですね。僕も良く使います
- @shima__shima 先生の発表がとてもわかりやすかったので、本当に参考にしたい
- 正直もっとコアな話もあっていいのでは、と思った
- 懇親会で気づいたが、意外と音声信号処理やってる（た）人がいてびっくりした
- [scikit-learn](https://github.com/scikit-learn/scikit-learn) を初期の頃に作られてた方 [@cournape](https://twitter.com/cournape) がいてびっくり。開発当初はGMMとSVMくらいしかなくて全然ユーザーがつかなかったなどなど、裏話を色々聞けた
- フランス人の「たぶん大丈夫」は絶対無理の意（わろた
- Rust, juliaがいいと教えてもらった。うちjuliaは今やってみてるがなかなかいい
- 発表でも話題に上がったけど、Pandasがいいという話を聞いたので、試してみたい

運営の方々、発表された方々、ありがとうございました。僕も機会が合えば何か発表したい
