---
layout: post
title: SPTKのPythonラッパーを書いた
date: 2014-08-10
comments: true
categories: speech-signal-processing python
---

## 2015/09/06 追記

ましなpythonラッパーを新しく作りました: [Pysptk: SPTKのpythonラッパーを作った (Part 2) - LESS IS MORE](http://r9y9.github.io/blog/2015/09/06/pysptk/)


## 2014/08/10 追記

ipython notebookによる簡単なチュートリアルを貼っておきます

[SPTK を Pythonから呼ぶ | nbviewer](http://nbviewer.ipython.org/github/r9y9/SPTK/blob/master/notebook/SPTK%20calling%20from%20python.ipynb)

## 2014/11/09

タイポ修正しました…

scipy.mixture -> sklearn.mixture

SPTKの中で最も価値がある（と僕が思っている）メルケプストラム分析、メルケプストラムからの波形合成（MLSA filter）がpythonから可能になります。

ご自由にどうぞ

[Speech Signal Processing Toolkit (SPTK) for API use with python | Github](https://github.com/r9y9/SPTK)

注意ですが、`SPTK.h`にある関数を全部ラップしているわけではないです。僕が必要なものしか、現状はラップしていません（例えば、GMMとかラップする必要ないですよね？sklearn.mixture使えばいいし）。ただ、大方有用なものはラップしたと思います。

## 参考

- [Goで音声信号処理をしたいのでSPTKのGoラッパーを書く - LESS IS MORE](http://r9y9.github.io/blog/2014/02/10/sptk-go-wrapper/)

Goでも書いたのにPythonでも書いてしまった。


一年くらい前に元指導教員の先生と「Pythonから使えたらいいですよね」と話をしていました。先生、ようやく書きました。
