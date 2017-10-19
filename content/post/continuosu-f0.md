+++
date = "2017-10-04T15:04:17+09:00"
draft = true
title = "統計的音声合成おけるContinous F0 modelingにおけるF0の補完方法"

+++


統計的音声合成において、Continuous F0の補完方法について、いくつか論文を調べたものの、F0を連続に補完しましたとは書いてあっても、具体的にどのように補完したのかはあまり書いておらず、自分で何がよいのか調べてみました。

ここでF0（基本周波数）は、有声区間では非ゼロの値、無声区間では0をとるものとします[^1]。音響モデルを考える際に、不連続なF0の系列をモデル化するのには、大きく2種類の方法があります。

- 1. Multi-space probabiltiy distribution HMM (MSDHMM) のように、連続かどうかを表す離散変数と、有声区間のF0の値を表す連続変数の2つ変数でモデル化する。
- 2. 無声区間のF0を連続な値で補完して、単一の連続変数でモデル化する

HMM音声合成では、（僕の肌感ではありますが、よく耳にしていたという意味で）前者がよく使われていた気がしますが、DNN音声合成の研究が盛んになって以来、モデルのシンプルさ、実装のシンプルさもあってか、後者が多くなっているような気がします。
で、今回の記事を書くにおいて調べたことは、冒頭にも書きましたが、どのような補完方法がよいのか？という点です。

## Merlinの実装

Merlinでは、とてもシンプルに、F0を線形に補完しています[^2]

https://github.com/CSTR-Edinburgh/merlin/blob/8688aa75cc5440522aca88a3d4d5fa7033a85a21/src/frontend/acoustic_normalisation.py#L75-L108

[^1]: そうでない定義は全然ありそうですが、便宜上この前提で進めます
[^2]: なおこの実装はとても効率が悪いです。numbaで大幅に高速化できます。でもscipyを使えば十分だと気づいたのでので、自前ライブラリでは、より汎用的にscipyで[実装](https://r9y9.github.io/nnmnkwii/latest/references/generated/nnmnkwii.preprocessing.f0.interp1d.html#nnmnkwii.preprocessing.f0.interp1d)しました。
