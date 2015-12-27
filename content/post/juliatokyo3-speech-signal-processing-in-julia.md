---
layout: post
title: "JuliaTokyo #3 Speech Signal Processing in Julia"
date: 2015-04-26
comments: true
categories: Julia Speech-Signal-Processing Machine-Learning
---

[JuliaTokyo #3](http://juliatokyo.connpass.com/event/13218/)でLT発表してきました。前回の[JuliaTokyo #2](http://juliatokyo.connpass.com/event/8010/)でも発表したので、二回目でした。

##  スライド

<div align="center">
<iframe src="//www.slideshare.net/slideshow/embed_code/key/h4geMoK1msYqdY" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/ryuichiy/juliatokyo-3-speech-signal-processing-in-julia-47403938" title="JuliaTokyo #3 Speech Signal Processing in Julia" target="_blank">JuliaTokyo #3 Speech Signal Processing in Julia</a> </strong> from <strong><a href="//www.slideshare.net/ryuichiy" target="_blank">Ryuichi YAMAMOTO</a></strong> </div>
</div>

## コード

https://github.com/r9y9/JuliaTokyo3

## 三行まとめ

発表の内容を三行でまとめると、

- 音声ファイルの読み込み（or 書き込み）は[WAV.jl]((https://github.com/dancasimiro/WAV.jl)を使おう
- 基本的なデジタル信号処理は [JuliaDSP/DSP.jl](https://github.com/JuliaDSP/DSP.jl) をチェック（※JuliaDSPにはウェーブレットとかもあるよ）
- 音声に特化した信号処理は、[r9y9/WORLD.jl](https://github.com/r9y9/WORLD.jl) がオススメです

という感じです。

応用例として、歌声を分離する話（[デモコード](https://github.com/r9y9/RobustPCA.jl)）、統計的声質変換（[統計的声質変換クッソムズすぎワロタ（チュートリアル編） - LESS IS MORE](http://r9y9.github.io/blog/2014/11/12/statistical-voice-conversion-code/)）、画像をスペクトログラムに足しこむ話とか、さっと紹介しました。

## 補足

僕が使う/作ったパッケージを、あとで見返せるように最後のスライドにまとめておいたのですが、改めてここで整理しておきます。

- [dancasimiro/WAV](https://github.com/dancasimiro/WAV.jl) WAVファイルの読み込み
- [JuliaDSP/DSP](https://github.com/JuliaDSP/DSP.jl) 窓関数、スペクトログラム、デジタルフィルタ
- [r9y9/WORLD](https://github.com/r9y9/WORLD.jl) 音声分析・合成フレームワーク
- [r9y9/MelGeneralizedCepstrums](https://github.com/r9y9/MelGeneralizedCepstrums.jl) メル一般化ケプストラム分析
- [r9y9/SynthesisFilters](https://github.com/r9y9/SynthesisFilters.jl) メル一般化ケプストラムからの波形合成
- [r9y9/SPTK](https://github.com/r9y9/SPTK.jl) 音声信号処理ツールキット
- [r9y9/RobustPCA](https://github.com/r9y9/RobustPCA.jl) ロバスト主成分分析(歌声分離へ応用)
- [r9y9/REAPER](https://github.com/r9y9/REAPER.jl) 基本周波数推定
- [r9y9/VoiceConversion](https://github.com/r9y9/VoiceConversion.jl) 統計的声質変換

上から順に、~~汎用的かなーと思います~~[^1]。僕が書いたパッケージの中では、**WORLDのみ**公式パッケージにしています。理由は単純で、その他のパッケージはあまりユーザがいないだろうなーと思ったからです。かなりマニアックであったり、今後の方針が決まってなかったり（ごめんなさい）、応用的過ぎて全然汎用的でなかったり。WORLDは自信を持ってオススメできますので、Juliaで音声信号処理をやってみようかなと思った方は、ぜひお試しください。

[^1]: とスライドに書いたけど、考えなおすと、僕が思う品質の高さ順、の方が正確です、失礼しました。MelGeneneralizedCepstrumsは一番気合入れて書いたけど、ユーザーがいるかといったらいないし、RobustPCAはさっと書いただけだけど、アルゴリズムとしては汎用的だし。またRobustPCAだけ毛色が違いますが、応用例で紹介したのでリストに入れておきました。

## ざっくり感想

- ＃Juliaわからん 本当に素晴らしいと思うので、僕も積極的に #Juliaわからん とつぶやいていこうと思います（詳しくは [@chezou](https://twitter.com/chezou) さんの記事をどうぞ [#JuliaTokyo で #juliaわからん という雑なレポジトリを立てた話をしたら julia.tokyo ができてた  - once upon a time,](http://chezou.hatenablog.com/entry/2015/04/26/222518)）。僕は、Julia に Theano が欲しいです。`T.grad` 強力すぎる
- `ccall` かんたんとか言いましたが、ミスった書き方をしたときのエラーメッセージはあまり親切ではないので、つまずきやすいかも。僕は気合で何とかしています。
- Julia遅いんだけど？？？と言われたら、[@bicycle1885](https://twitter.com/bicycle1885) さんの [What's wrong with this Julia?](http://www.slideshare.net/KentaSato/whats-wrong-47403774) を投げつけようと思います。
- かなり聴衆が限定的になってしまう話をしてしまったので、次発表するならJulia 言語自体の話をしようかなと思いました

## 最後に

[@sorami](https://twitter.com/sorami)さんを筆頭とする運営の方々、本当にありがとうございました！楽しかったです。
