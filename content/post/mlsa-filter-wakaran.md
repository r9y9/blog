---
layout: post
title: "MLSA フィルタの実装"
date: 2013-09-23
comments: true
categories: speech-signal-processing speech-synthesis
---

音声合成に使われるMLSA（Mel-Log Spectrum Approximatation）フィルタを実装したいんだが、なにぶんわからん。SPTKにコードはあるけれど、正直理解できない。デジタル信号処理を小学一年生から勉強しなおしたいレベルだ

と、前置きはさておき、MLSAフィルタの実装を見つけたのでメモ。ここ最近ちょくちょく調べているが、SPTK以外で初めて見つけた。

[Realisation and Simulation of the Mel Log Spectrum Approximation Filter | Simple4All Internship Report](http://simple4all.org/wp-content/uploads/2013/05/Jiunn.pdf)

Simple4Allという音声技術系のコミュニティの、学生さんのインターンの成果らしい。ちらっと調べてたら山岸先生も参加してる（た？）っぽい。

上のreportで引用されているように、MLSA filterの実現方法については、益子さんのD論に詳しく書いてあることがわかった。今井先生の論文と併せて読んでみようと思う。

[T. Masuko, "HMM-Based Speech Synthesis and Its Applications", Ph.D Thesis, 2002.](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.109.3623&rep=rep1&type=pdf)

もう正直わからんしブラックボックスでもいいから既存のツール使うかーと諦めかけていたところで割りと丁寧な実装付き解説を見つけたので、もう一度勉強して実装してみようと思い直した。

機械学習にかまけて信号処理をちゃんと勉強していなかったつけがきている。LMA filterもMLSA filterも、本当にわからなくてツライ……

(実装だけであれば、実はそんなに難しくなかった 2013/09後半)

### 追記 2015/02/25

誤解を生む表現があったので、直しました
