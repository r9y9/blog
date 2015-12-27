---
layout: post
title: "FFTを使った連続ウェーブレット変換の高速化"
date: 2013-10-20
comments: true
categories: signal-processing wavelet-transform continuous-wavelet
---

<div align="center"><img src="/images/gabor_wavelet_nnmnkwii.png "An example of Gabor Wavelet spectrogram (the original wav file is generated using Open Jalk)"" class="image"></div>

## そもそもウェーブレット変換って何

[Jump to wikipedia](http://ja.wikipedia.org/wiki/%E3%82%A6%E3%82%A7%E3%83%BC%E3%83%96%E3%83%AC%E3%83%83%E3%83%88%E5%A4%89%E6%8F%9B)

いわゆる時間周波数解析の手法の一つで、音声、音楽、画像の解析に使われる。直感的には、STFTでいう窓関数の幅を周波数に応じて拡大・伸縮させて、時間変化する信号の特徴を上手く捉えようとする手法のこと

## 高速化の仕組み

さて、本題。ウェーブレット変換は、(スケールパラメータを固定すれば)入力信号とマザーウェーブレットのたたみ込みで表されるので、たたみ込み定理よりフーリエ変換を使った計算方法が存在する。

つまり、

- 入力信号とマザーウェーブレットをそれぞれフーリエ変換する
- 掛け算する
- 逆フーリエ変換する

というプロセスでウェーブレット変換を求めることができて、かつフーリエ変換にはFFTという高速なアルゴリズムが存在するので、計算を高速化できるという仕組み。まぁ原理としてはシンプルなんだけど以外と面倒くさい（気のせい？）。

色々調べたので、メモ代わりにまとめておく。解説ではなくリンク集です

## A Practical Guide to Wavelet Analysis [[web]](http://paos.colorado.edu/research/wavelets/) [[PDF]](http://paos.colorado.edu/research/wavelets/bams_79_01_0061.pdf)
結論から言えばここが一番わかりやすかった。

- 実装よりで理論の解説がある
- matlab/fortran のコードがある

がいいところ

基本的にはこれ読めばわかる。数学全然わからん俺でも読めた。特に、離散表現でのウェーブレットについても書かれているのは良い。連続ウェーブレットといっても、デジタル信号処理で扱う上では離散化しないといけないわけなので

さて、僕が参考にしたmatlabコードへの直リンクは以下

- [マザーウェーブレットの周波数応答の計算部分](http://paos.colorado.edu/research/wavelets/wave_matlab/wave_bases.m)
- [連続ウェーブレット変換の本体](http://paos.colorado.edu/research/wavelets/wave_matlab/wavelet.m)
- [連続ウェーブレット変換のテストコード](http://paos.colorado.edu/research/wavelets/wave_matlab/wavetest.m)

その他、fortanコードなどいくつかあるので、それらはウェブサイトからどうぞ

## Matlab
 mathworksさんのwavelet toolboxのドキュメントもよかった。ここから上記のpracticalなんちゃらのリンクもある

- [Continuous Wavelet Transform](http://www.mathworks.co.jp/jp/help/wavelet/gs/continuous-wavelet-transform.html)
- [Continuous wavelet transform using FFT algorithm](http://www.mathworks.co.jp/jp/help/wavelet/ref/cwtft.html)
- [Inverse CWT](http://www.mathworks.co.jp/jp/help/wavelet/ref/icwtft.html)

コードは転がってないですね。まぁ有料なので

## 日本語でわかりやすいもの

- [C/C++言語でガボールウェーブレット変換により時間周波数解析を行うサンプルプログラム](http://hp.vector.co.jp/authors/VA046927/gabor_wavelet/gabor_wavelet.html)
     - ここは本当に素晴らしい。何年か前にも参考にさせて頂きました。
- [連続ウェーブレット変換 (CWT) - FlexPro 7 日本語版サポート情報](http://www.hulinks.co.jp/support/flexpro/v7/dataanalysis_cwt.html)
     - 日本語で丁寧に書かれてる。内容自体は、practicalなんちゃらと似ている
- [東北大学 伊藤先生の講義資料](http://www.makino.ecei.tohoku.ac.jp/~aito/wavelet/)
     - 数少ない日本語でのウェーブレットに関する資料。ただし連続ウェーブレットについてはあんまり解説はない。C言語のサンプル付き

## 書籍

今回は調べてない。数年前にちょいちょい調べたことがあるけど忘れた

## その他

- [tspl Signal Processing Library in C++](https://code.google.com/p/tspl/source/browse/trunk/include/cwt-impl.h?spec=svn2&r=2)
     - 連続ウェーブレット変換/逆変換のC++実装。細部までコードは追えてないけど、それっぽいコードがある（俺が読んだ記事とはマザーウェーブレットのnormalizationが違う気もする…
- [Inverse Continuous Wavelet Transform and matlab - dsp StackExchange](http://dsp.stackexchange.com/questions/10979/inverse-continuous-wavelet-transform-and-matlab)
     - 逆連続ウェーブレット変換教えてーっていう質問。ここでpracticalなんちゃらを知った
- [混合音中の歌声の声質変換手法](http://staff.aist.go.jp/h.fujihara/voice_conversion/)
     - ガチ技術。元産総研の藤原さんが研究開発したもの。[論文(PDF)](http://staff.aist.go.jp/m.goto/PAPER/SIGMUS201007fujihara.pdf)の方に少し説明がある。
     - 声質変換でウェーブレット使うのは僕が知る限りではこれくらい
     - ちなみに結果めっちゃすごい

## さいごに
以上。ウェーブレット変換は難しいことがわかった（こなみ）。ウェーブレットの利点欠点については書かなかったけれど、音声や音楽を解析したい場合に、時間周波数解析によく用いられる短時間フーリエ解析よりもウェーブレット解析の方が望ましい場合は非常によくあると思っているので、ぜひもっと使われてほしいですね。作ってるライブラリには必ず入れます。

## ちなみに
計算コストがそこまでボトルネックにならないなら、畳み込みでウェーブレット計算してもいいんじゃないかと思ってる。FFTを使う方法の場合、あるスケールパラメータに対する時間方向のウェーブレット変換係数を一気に求められても、あるシフトパラメータに対する周波数方向のウェーブレット変換係数（つまりある時間でのスペクトルのようなもの）は一気に求められない気がしている。つまり、STFTみたいな形でインクリメンタルにスペクトルは求めにくいんじゃないかってこと（少なくとも自明には思えない）。畳み込み計算するなら、間違いなくできるけど。このあたり理解がまだあやふやなので、間違ってる可能性大

さらにちなみに、僕が作ってたリアルタイムで動く自動伴奏システムは畳み込みでウェーブレット変換してたよ。ウェーブレットよりもアルゴリズムのほうがボトルネックになっていたので全然気にならなかった。参考まで
