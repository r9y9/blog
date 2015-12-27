---
layout: post
title: "MFCCの計算方法についてメモ"
date: 2013-11-24
comments: true
categories: speech-signal-processing
---


## MFCC とは

Mel-Frequency Cepstral Coefficients (MFCCs) のこと。音声認識でよく使われる、音声の特徴表現の代表的なもの。

### 算出手順

- 音声信号を適当な長さのフレームで切り出し
- 窓がけ
- フーリエ変換して対数振幅スペクトルを求める
- メルフィルタバンクを掛けて、メル周波数スペクトルを求める
- 離散コサイン変換により、MFCCを求める


以上。SPTKのmfccコマンドのソースもだいたいそうなってた。

### さて

#### ここに音声波形があるじゃろ？？

<div align="center"><img src="/images/speech-signal.png "音声信号を適当な長さのフレームで切り出し"" class="image"></div>

#### 音声波形を窓がけして…

<div align="center"><img src="/images/windowed-signal.png "窓がけ"" class="image"></div>

#### さらにフーリエ変換して対数取って…

<div align="center"><img src="/images/log-amplitude.png "フーリエ変換して振幅スペクトルを求める"" class="image"></div>

#### ここでメルフィルタバンクの出番じゃ

<div align="center"><img src="/images/after-mel-filterbank.png "メルフィルタバンクを掛けて、メル周波数スペクトルを求める"" class="image"></div>


#### 最後に離散コサイン変換で完成じゃ
<div align="center"><img src="/images/MFCC.png "離散コサイン変換により、MFCCを求める"" class="image"></div>


## まとめ

- MFCC求めたかったら、普通はHTKかSPTK使えばいいんじゃないですかね。自分で書くと面倒くさいです
- 正規化はどうするのがいいのか、まだよくわかってない。単純にDCT（IIを使った）を最後に掛けると、かなり大きい値になって使いにくい。ので、 http://research.cs.tamu.edu/prism/lectures/sp/l9.pdf にもあるとおり、mel-filterbankの数（今回の場合は64）で割った。
- 間違ってるかもしれないけどご愛嬌

## 参考

- [L9: Cepstral analysis [PDF]](http://research.cs.tamu.edu/prism/lectures/sp/l9.pdf)
- [メル周波数ケプストラム（MFCC） | Miyazawa’s Pukiwiki 公開版](http://shower.human.waseda.ac.jp/~m-kouki/pukiwiki_public/66.html)
- [メル周波数ケプストラム係数（MFCC） | 人工知能に関する断創録](http://aidiary.hatenablog.com/entry/20120225/1330179868)
