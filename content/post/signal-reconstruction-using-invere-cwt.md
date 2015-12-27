---
layout: post
title: "逆連続ウェーブレット変換による信号の再構成"
date: 2013-10-21
comments: true
categories: inverse-continous-wavelet-transform wavelet-transform signal-reconstruction signal-processing
---

やったのでメモ。おそらく正しくできたと思う。結果貼っとく。ウェーブレットの参考は以下の文献

[Torrence, C. and G.P. Compo "A Practical Guide to Wavelet Analysis", Bull. Am. Meteorol. Soc., 79, 61–78, 1998.](http://paos.colorado.edu/research/wavelets/bams_79_01_0061.pdf) 

## ウェーブレットの条件
マザーウェーブレットはmorletを使う

<div>
\begin{align}
\psi_{0}(\eta) = \pi^{-1/4}e^{i\omega_{0}\eta}e^{-\eta^{2}/2}
\end{align}
</div> 

文献に従って$\omega_{0} = 6.0$とした。

以下にいっぱい図を張る。軸は適当

## 元の信号

<div align="center"><img src="/images/wavelet/original_signal.png "The original signal"" class="image"></div>

## ウェーブレットスペクトログラム

<div align="center"><img src="/images/wavelet/morlet_wavelet_spectrogram.png "Morlet wavelet spectrogram"" class="image"></div>

Gaborではなく、Morletで求めたもの。スケールは、min=55hzで、25cent毎に8オクターブ分取った。一サンプル毎にウェーブレット変換を求めてるので、前回の記事でガボールウェーブレットで求めた奴よりよっぽど解像度高いっすね（前のは10ms毎だった、書いてなかったけど）。見てて綺麗（こなみ

計算はFFT使ってるので速い

http://hp.vector.co.jp/authors/VA046927/gabor_wavelet/gabor_wavelet.html
スケールのとり方はここを参考にするといい

## 再構成した信号

<div align="center"><img src="/images/wavelet/recostructed_signal.png "The recostructed signal"" class="image"></div>


連続ウェーブレットの逆変換は、フーリエ変換と違ってそんなシンプルじゃないんだけど、結果から言えばウェーブレット変換の実数部を足しあわせて適当にスケールすれば元の信号が再構成できるみたい。ほんまかと思って実際にやってみたけど、できた

が、実は少し誤差がある

## 重ねてプロット

<div align="center"><img src="/images/wavelet/double_0.png "The original signal and recostructed signal"" class="image"></div>

## あっぷ

<div align="center"><img src="/images/wavelet/double_1.png "The original signal and recostructed signal with zoom 1"" class="image"></div>

<div align="center"><img src="/images/wavelet/double_2.png "The original signal and recostructed signal with zoom 2"" class="image"></div>

<div align="center"><img src="/images/wavelet/double_3.png "The original signal and recostructed signal with zoom 3"" class="image"></div>

<div align="center"><img src="/images/wavelet/double_4.png "The original signal and recostructed signal with zoom 4"" class="image"></div>

<div align="center"><img src="/images/wavelet/double_5.png "The original signal and recostructed signal with zoom 5"" class="image"></div>


んー、まぁだいたいあってんじゃないですかね

## 誤差

平均誤差を計算すると、図の縦軸の量で考えて55.3994だった。16bitのwavが-32768〜32767なので、どうだろう、大きいのか小さいのかわからん

ただ、再合成した音声を聞いた所それほど違和感はなかった。これはつまり、スペクトルいじる系の分析にSTFTがではなくウェーブレット使ってもいいんではないか？という考えが生まれますね。果たして、ウェーブレットが音声/音楽の分析にフーリエ変換ほど使われないのはなぜなのか、突き詰めたい

## 使った音声
あなたが一番聞きたいと思った声が流れます、どうぞ

<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/116227502"></iframe>

スペクトログラム表示するのにサンプルが多いと大変なので、48kから10kにサンプリング周波数を落としたもの

## 再構成した音声

<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/116227539"></iframe>

僕の耳では違いはわからない。サンプリング周波数によって誤差が大小する可能性はあるが、そこまで調査してない


## メモ

http://paos.colorado.edu/research/wavelets/wavelet3.html
ここの最後に書かれている以下の文章、

> One problem with performing the wavelet transform in Fourier space is that this assumes the time series is periodic. The result is that signals in the wavelet transform at one end of the time series will get wrapped around to the other end. 

FFT使うウェーブレット変換の問題は、信号を周期関数として仮定してしまうことにある、と。まあ、ですよねー。信号がめちゃくちゃ長くてこの仮定が破綻してしまう場合、どうするのがいいんだろう。

あと、FFT使うウェーブレットの問題として、メモリ食うってのがあるんよな。ウェーブレット変換を計算する前に、マザーウェーブレットのフーリエ変換を持っとかないといけないし、サンプル毎に計算しないといけないし。44.1kの数分の音声とかなると、もう無理っすね。

それぞれ、解決方法は思いつかないでもないけど、まだまとまってないので、解決したらまとめる、かもしれない。

## さらにめも

- practicalなんちゃらの、マザーウェーブレットを正規化する部分のmatlabコード、文献中の数式と若干違ってトリッキー。展開すれば一緒なんだけど、文献中の数式をそのまま書いたようになってないので、注意。ちょっと戸惑った
- 逆ウェーブレットを行う際のスケールにかかる係数（文献中でいう$C_{\delta}$）は、マザーウェーブレットが決まれば値が定まる（らしい）。例えばMorletの$\omega_0 = 6$なら0.776とわかってるので、積分して計算する必要はない
- ウェーブレット変換と戯れてたら週末終わった
