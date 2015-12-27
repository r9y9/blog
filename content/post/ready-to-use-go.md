---
layout: post
title: Goに関する良記事
date: 2014-02-02
comments: true
categories: Go
---

いくつか見つけたのでメモる

## [Why We Think GoLang Is Ready For Early Stage Startups](http://www.jellolabs.com/blog/why-golang-is-ready-for-early-stage-startups.html)

とあるスタートアップがウェブでGoを使うという意思決定をした理由、その決断に至るまでのプロセスが書かれている。また、その過程でGoを使うことによる利点・欠点が簡潔にまとめられてる。参考になった

## [Go Getter - Performance comparison to C++ business card ray tracer](https://kidoman.com/programming/go-getter.html)

<div align="center"><img src="/images/go-improvements.png" class="image"></div>

GoとC++のパフォーマンスの比較。Ray tracingというCGの手法を用いて比較をしていて、Goでも最適化するとC++並のスピード出ますよ（そしてC++と違ってGCあるしマルチコアにも簡単にできるしGoいいよ）って話。（自分へのメモのため画像を拝借していますが、意味がわからないと思うので元記事を参照してください）

ただoptimized Go vs un-optimized C++なので注意。Goの最適化が主旨の記事です

## [Go Getter Part 2 - Now with C++ optimizations](https://kidoman.com/programming/go-getter-part-2.html)

<div align="center"><img src="/images/go-vs-cpp-after-both-optimized.png" class="image"></div>

さっきの続きで、こちらでは最適化したC++と比較されてる。OpenMP使って並列化してるようだけど、あれ、まだC++の方が遅い・・（正直意外

## [Go Getter Part 3 - Further optimizations and a multi-threaded C++ version](https://kidoman.com/programming/go-getter-part-3.html)

<div align="center"><img src="/images/2048x2048-3.png" class="image"></div>

これで最後。C++（とGo）をめちゃくちゃ最適化した、って奴ですね。C++の方が二倍程度速くなったよう。
ただ、やっぱC++の方が良かった、というよりGoがC++並になるのも時間の問題って感じですね。


## さて

このまとめで何が言いたかったというと

**「Goを使わない選択肢がない」**

まぁ半分冗談（ケースバイケースだし）ですが、僕のようにC++をメインで使っているけど不満ありまくりな人は、一度Go使ってみてもいいんじゃないでしょうか、と思います。C++の百倍書きやすいです
