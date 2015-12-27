---
layout: post
title: "Goで信号処理"
date: 2014-01-27
comments: true
categories: go
---

最近Go言語を触っていて、これがなかなかいい感じ。そこそこ速いので、信号処理や機械学習も行けると思う

## Goの良い所

- デフォでたくさん便利なパッケージがある。http, json, os, ...
- パッケージのインストールはとても簡単。go getするだけ
- デフォでテストの枠組みがある
- gofmtでコードのformattingしてくれるので書き方で迷わなくて良い
- 使わないパッケージをimportするとコンパイルエラーになるし自然と疎結合なコードを書くようになる
- 並列処理を言語レベルでサポート
- GCあるのでメモリ管理なんてしなくていい
- 全般的にC++より書きやすい（ここ重要）
- そこそこ速い（C++よりは遅いけど）

ホントはPythonでさくっと書きたいけどパフォーマンスもほしいからC++で書くかー（嫌だけど）。と思ってた自分にはちょうどいい

## Goの悪い所（主にC++と比べて）

- ちょっと遅い。さっと試したウェーブレット変換は、1.5倍くらい遅かった気がする（うろ覚え）
- C++やpythonに比べるとライブラリは少ない
- 言語仕様とかそのへんが優れてるかどうかは判断つきませんごめんなさい

# Go-msptools

2014/07/22 追記：  
Go-msptoolsはGOSSPに吸収されました。（[GOSSP - Go言語で音声信号処理 - LESS IS MORE](http://r9y9.github.io/blog/2014/06/08/gossp-speech-signal-processing-for-go/)を参照）

## おまけ：音の信号処理に役立ちそうなライブラリ

- [go-dsp](https://github.com/mjibson/go-dsp/)
- [portaudio-go](https://code.google.com/p/portaudio-go/)
