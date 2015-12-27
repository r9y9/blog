---
layout: post
title: 最近の音声信号処理遊びの進捗
date: 2015-08-23
comments: true
categories: speech-signal-processing julia
---

## hello

遡ればもう約一年まえになるでしょうか、統計的声質遊びをしたいと思い、理論の勉強を始めたり、（特にJuliaで）コードを色々書いていました（お前ほんといろんな言語で遊んでるな、というツッコミはさておき）。[統計的声質変換クッソムズすぎワロタ（チュートリアル編） - LESS IS MORE](http://r9y9.github.io/blog/2014/11/12/statistical-voice-conversion-code/) を書いていた当初は、当然自分のためだけに書いていて、まぁアレな出来でしたが、最近気を取り直して多少マシに仕上げましたので、何となくブログに書いてみようかなーと思った次第です。というわけで、最近公式に登録したいくつかのパッケージを、まとめて簡単に紹介します。

主な改善点は、windowsもちゃんとサポートするようにしたこと（誰得？）と、テストをきちんと書いたことと、julia的なインタフェースを意識するようにしたことですかね。3つ目はかなり曖昧ですが、まぁ気持ち使いやすくなったと思います。

## パッケージ

- [MelGeneralizedCepstrums.jl](https://github.com/r9y9/MelGeneralizedCepstrums.jl): メル一般化ケプストラム分析
- [SynthesisFilters.jl](https://github.com/r9y9/SynthesisFilters.jl): メル一般化ケプストラムからの音声波形合成
- [SPTK.jl](https://github.com/r9y9/SPTK.jl): [SPTK](http://sp-tk.sourceforge.net/)のラッパー

車輪の再発明はできるだけしたくなかったので、最初のほうはCライブラリのラッパーを書くことが多く、windowsとかめんどくさいしunix環境でしか動作確認してませんでしたが、[WindowsのJuliaから呼べるようなCライブラリの共有ライブラリ（DLL）を作る | qiita](http://qiita.com/r9y9/items/e0567e2a21a5e3c36e51) 重い腰を上げてwindowsでも動くように頑張ったことがあり（めんどくさいとか言って手を動かさないのホント良くないですね）、登録したパッケージはすべてwindowsでも動くようになりました。めでたし。[WORLD.jl](https://github.com/r9y9/WORLD.jl) もwindowsで動くようにしました。

## MelGeneralizedCepstrums.jl

メルケプストラムの推定とか。いくつか例を載せておきます

<img src="https://raw.githubusercontent.com/r9y9/MelGeneralizedCepstrums.jl/v0.0.1/examples/cepstrum.png" alt="cepstrum based envelope." class="image">

<img src="https://raw.githubusercontent.com/r9y9/MelGeneralizedCepstrums.jl/v0.0.1/examples/mel-cepstrum.png" alt="mel-cepstrum based envelope." class="image">

<img src="https://raw.githubusercontent.com/r9y9/MelGeneralizedCepstrums.jl/v0.0.1/examples/mel-generalized-cepstrum.png" alt="mel-generalized-cepstrum based envelope." class="image">

<img src="https://raw.githubusercontent.com/r9y9/MelGeneralizedCepstrums.jl/v0.0.1/examples/lpc-cepstrum.png" alt="lpc-cepstrum based envelope." class="image">

詳細はこちらの[ノートブック](http://nbviewer.ipython.org/github/r9y9/MelGeneralizedCepstrums.jl/blob/v0.0.1/examples/Introduction%20to%20MelGeneralizedCeptrums.jl.ipynb)へ

メルケプストラム分析、メル一般化ケプストラム分析に関しては、SPTKの実装をjuliaで再実装してみました。結果、速度は1.0 ~ 1.5倍程度でおさまって、かつ数値的な安定性は増しています（メモリ使用量はお察し）。まぁ僕が頑張ったからというわけでなく、単にJuliaの線形方程式ソルバーがSPTKのものより安定しているというのが理由です。

## SynthesisFilters.jl

メルケプストラムからの波形合成とか。

詳細はこちらの[ノートブック](http://nbviewer.ipython.org/github/r9y9/SynthesisFilters.jl/blob/v0.0.1/examples/Introduction%20to%20SynthesisFilters.jl.ipynb)へ。いくつかの音声合成フィルタの合成音をノートブック上で比較することができます。

[mixed excitation（っぽいの）を使ったバージョンのノートブック](http://nbviewer.ipython.org/github/r9y9/SynthesisFilters.jl/blob/mix-excitation/examples/Introduction%20to%20SynthesisFilters.jl.ipynb): 実装に自信がないので、そのうち消すかも。聴覚的にはこっちのほうが良いです。

## SPTK.jl

公式のSPTKではなく、僕が少しいじったSPTK（windowsで動くようにしたり、APIとして使いやすいように関数内でexitしてた部分を適切なreturn code返すようにしたり、swipeというF0抽出のインタフェースをexposeしたり、など）をベースにしています。

[デモ用のノートブック](http://nbviewer.ipython.org/github/r9y9/SPTK.jl/blob/v0.0.1/examples/Introduction%20to%20SPTK.jl.ipynb)

MelGeneralizedCepstrums.jl と SynthesiFilters.jl は、ほとんどSPTK.jlで成り立っています。本質的に SPTK.jl にできて MelGeneralizedCepstrums.jl と SynthesiFilters.jlにできないことは基本的にないのですが、後者の方が、より簡単な、Julia的なインタフェースになっています。

例えば、メルケプストラム、ケプストラム、LPCなど、スペクトルパラメータの型に応じて、適切なフィルタ係数に変換する、合成フィルタを選択するなど、multiple dispatchを有効に活用して、よりシンプルなインタフェースを提供するようにしました（というか自分がミスりたくなかったからそうしました）。

## おわり

かなり適当に書きましたが、最近の進捗は、Juliaで書いていたパッケージ多少改善して、公式に登録したくらいでした。進捗まじ少なめ。あと些細なことですが、ipython（ijulia）に音埋め込むのクッソ簡単にできてびっくりしました（なんで今までやらなかったんだろう）。[@jfsantos](https://github.com/jfsantos) に感謝
