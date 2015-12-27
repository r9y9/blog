---
layout: post
title: "pysptk: SPTKのpythonラッパーを作った (part 2)"
date: 2015-09-06
comments: true
categories: speech-signal-processing python
---

2015/09/05:

<div align="center">
<blockquote class="twitter-tweet" lang="en"><p lang="ja" dir="ltr"><a href="https://t.co/WFBmYEIVce">https://t.co/WFBmYEIVce</a> SPTKのpythonラッパー（マシなやつ）完成&#10;ドキュメント <a href="http://t.co/jYhw1y3Bzg">http://t.co/jYhw1y3Bzg</a>&#10;pip install pysptk でインストールできるようになりました。pypi童貞捨てれた</p>&mdash; 山本りゅういち (@r9y9) <a href="https://twitter.com/r9y9/status/639848868075560960">September 4, 2015</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
</div>


ずいぶん前に、swig遊びをしがてらpythonのラッパーを書いていたんですが、cythonを使って新しく作りなおしました。かなりパワーアップしました。

```
pip install pysptk
```

でインストールできるので、よろしければどうぞ

## なぜ作ったのか

- cythonとsphinxで遊んでたらできた

## 使い方

以下のデモを参考にどうぞ

- [Introduction to pysptk](http://nbviewer.ipython.org/github/r9y9/pysptk/blob/51c103e5a7e9746c96cd78043df4e48fe2d6a3a8/examples/pysptk%20introduction.ipynb): メル一般化ケプストラム分析とか
- [Speech analysis and re-synthesis](http://nbviewer.ipython.org/github/r9y9/pysptk/blob/51c103e5a7e9746c96cd78043df4e48fe2d6a3a8/examples/Speech%20analysis%20and%20re-synthesis.ipynb): 音声の分析・再合成のデモ。合成音声はnotebook上で再生できます


## ドキュメント

http://pysptk.readthedocs.org

## ぼやき

SPTKの関数、変な値入れるとexitしたりセグフォったりするので、ちゃんとテスト書いてほしいなあ


## 関連

- [SPTKのPythonラッパーを書いた - LESS IS MORE](http://r9y9.github.io/blog/2014/08/10/sptk-from-python/)
