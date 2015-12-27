---
layout: post
title: "JuliaTokyo #2でBinDeps.jl についてLTしてきた"
date: 2014-09-30
comments: true
categories: Julia JuliaTokyo BinDeps
---

[JuliaTokyo #2 - connpass](juliatokyo.connpass.com/event/8010/)
	    
<script async class="speakerdeck-embed" data-id="21106ae0285e01327810268beacd0cf3" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>

## 発表概要

C/C++ライブラリのラッパー（C++は現状のJuliaでは難しいけど）を作るときに、どうやってライブラリの依存関係を管理するか？という話です。結論としては、方法はいくつかありますが　BinDeps.jl というパッケージを使うのが楽で良いですよ、ということです。Githubのいろんなリポジトリをあさった僕の経験上、BinDeps.jl はバイナリの依存関係管理におけるデファクトスタンダードな気がしています。BinDeps.jl の使い方は、既存のパッケージのコードを読みまくって学ぶのがおすすめです。

さて、途中で書くのに疲れてしまったのですが、[自作のJuliaパッケージで、Cライブラリとの依存性を記述する - Qiita](http://qiita.com/r9y9/items/73806e3ce7f3a372d0b3) に以前似たような内容をまとめたので、併せてどうぞ。qiitaにも書きましたが、最適化関係のプロジェクトを集めた [JuliaOpt](http://www.juliaopt.org/) コミュニティでは、バイナリの依存関係管理にBinDeps.jlを使用することを推奨しています。

## 雑感

- 勉強会にはデータ分析界隈の人が多い印象。音声系の人はとても少なかった。
- R人気だった
- Go使ってる！って人と合わなかった（つらい）
- @show マクロ最高
- unicode最高
- 懇親会では、なぜか途中から深層学習やベイズの話をしていた…
- いい忘れたけど僕もnightly build勢でした。毎日あたたかみのある手動pull & make をしています。
- Julia の話ができて楽しかったので、また参加したいなー

LTで [MeCab.jl](https://github.com/chezou/MeCab.jl) について話をしてくれたchezouさんが、ちょうどBinDeps.jl に興味を持たれているようだったので、勉強会のあとに BinDeps.jl を使ってバイナリの管理を実装して、[プルリク](https://github.com/chezou/MeCab.jl/pull/2)をしてみました。参考になればうれしいなーと思います。

おしまい。
