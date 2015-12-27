---
layout: post
title: "SPTKをC++から使えるようにする"
date: 2013-12-01
comments: true
categories: speech-signal-processing
---

[音声信号処理ツールキットSPTK](http://sp-tk.sourceforge.net/)をC++から使おうと思ったら意外とハマってしまったので、

* C++から使えるようにC++コンパイラでコンパイルできるようにした
* 使いやすいようにwafを組み込みんだ

リポジトリ: https://github.com/r9y9/SPTK

というわけで、使い方について簡単に書いておく

# SPTK について

* SPTKを使うと何ができるか: [SPTKの使い方 (1) インストール・波形描画・音声再生 | 人工知能に関する断創録](http://aidiary.hatenablog.com/entry/20120701/1341126474)
* SPTKとは: [Speech Signal Processing Toolkit (SPTK)]([http://sp-tk.sourceforge.net/])

# SPTK with waf

[SPTK with waf](https://github.com/r9y9/SPTK)は、SPTKをwafでビルド管理できるようにしたものです。

* SPTKを共有ライブラリとしてインストールできます。
* C、C++の好きな方でコンパイルできます。
* wafが使えます（速い、出力がキレイ）
* 自分のC、C++コードからSPTKのメソッドを呼べます。
* コマンドラインツールはインストールされません。

コマンドラインツールを使いたい人は、元のconfigure scriptを使えば十分です。

# 環境

* Unix系

Ubuntu 12.04 LTS 64 bitとMac OS X 10.9では確認済み

# SPTKのインストール

リポジトリをクローンしたあと、

## Build

     ./waf configure && ./waf

## Build with clang++

     CXX=clang++ ./waf configure && ./waf

## Build with gcc

     git checkout c
     ./waf configure && ./waf

## Build with clang

     git checkout c
     CC=clang ./waf configure && ./waf

## Install 

     sudo ./waf install

* Include files: `/usr/local/include/SPTK`
* Library: `/usr/local/lib/SPTK`
* Pkg-config: `/usr/local/lib/pkgconfig`

オリジナルのSPTKとはインストール場所が異なります（オリジナルは、`/usr/local/SPTK`）

# SPTKを使ってコードを書く

`<SPTK/SPTK.h>` をインクルードして、好きな関数を呼ぶ

コンパイルは、例えば以下のようにする

     g++ test.cpp `pkg-config SPTK --cflags --libs`

面倒なので、example/ 内のコードを修正して使う（wafを使おう）のがおすすめです。


<br/>

# きっかけ

* SPTKはコマンドラインツールだと思ってたけど、どうやらSPTK.hをインクルードすれば一通りのツールを使えるらしい
* SPTK.hをインクルードして使う方法のマニュアルが見つからない…
* SPTKはC言語で書かれてるし、C++から使うの地味にめんどくさい

# C++から簡単に使いたかった

* gccやclangだけじゃなくg++やclang++でコンパイルできるようにしよう
* 自分のコードのビルド管理にはwafを使ってるし、wafで管理できるようにしてしまおう
* waf素晴らしいしな （参考: [waf チュートリアル | 純粋関数型雑記帳 ](http://d.hatena.ne.jp/tanakh/20100212)）

# 最後に

SPTKもwafも素晴らしいので積極的に使おう＾＾
