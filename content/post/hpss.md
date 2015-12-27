---
layout: post
title: "調波打楽器音分離（HPSS）を試す"
date: 2013-09-14
comments: true
categories: music-signal-processing source-separation, matrix-factorization
---

## HPSSとは（一行説明）

HPSS（Harmonic/Percussive Sound Separation）というのは、音源中の調波音/打楽器音が、それぞれ時間方向に滑らか/周波数方向に滑らかという異った性質を持つことを利用して、両者を分離する方法のこと。わからんければ論文へ

アイデアはシンプル、実装は簡単、効果は素晴らしい。specmurtに似たものを感じる。ということで少し感動したので結果を載せる


## 実装

調波音のスペクトログラムを$H$、打楽器音のスペクトログラムを$P$、時間indexをt、周波数indexをkとして、以下の数式をそのまま実装して、適当に反復計算すればおｋ

<div>
\begin{align}
|H_{t, k}| = \frac{w_{H}^2 (|H_{t+1,k}| + |H_{t-1,k}|)^2 |W_{t,k}|}{w_{H}^2 (|H_{t+1,k}| + |H_{t-1,k}|)^2 + w_{P}^2(|P_{t,k+1}| + |P_{t,k-1}|)^2}
\end{align}
</div>

<div>
\begin{align}
|P_{t, k}| = \frac{w_{P}^2 (|P_{t,k+1}| + |P_{t,k-1}|)^2 |W_{t,k}|}{w_{H}^2 (|H_{t+1,k}| + |H_{t-1,k}|)^2 + w_{P}^2(|P_{t,k+1}| + |P_{t,k-1}|)^2}
\end{align}
</div>

ただし

<div>
\begin{align}
|W_{t,k}| = |H_{t,k}| + |P_{t,k}|
\end{align}
</div>

絶対値はパワースペクトル。論文中の表記とはけっこう違うので注意。厳密ではないです。$w\_{H}, w\_{P}$は重み係数で、両方共1.0くらいにしとく。

HPSSの論文はたくさんあるけど、日本語でかつ丁寧な ["スペクトルの時間変化に基づく音楽音響信号からの歌声成分の強調と抑圧"](http://ci.nii.ac.jp/naid/110007997346) を参考にした。

H/Pから音源を再合成するときは、位相は元の信号のものを使えばおｋ

一点だけ、HとPの初期値どうすればいいんかなぁと思って悩んだ。まぁ普通に元音源のスペクトログラムを両方の初期値としてやったけど、うまく動いてるっぽい。

## 結果

フリー音源でテストしてみたので、結果を貼っとく。$w\_{H}=1.0, w\_{P}=1.0$、サンプリング周波数44.1kHz、モノラル、フレーム長512、窓関数はhanning。反復推定の回数は30。音源は、[歌もの音楽素材：歌入り素材系のフリー音楽素材一覧](http://maoudamashii.jokersounds.com/archives/song_kyoko_feels_happiness.html) から使わせてもらいました。ありがとうございまっす。元音源だけステレオです。
18秒目くらいからを比較すると効果がわかりやすいです

### 元音源

<iframe frameborder="no" height="166" scrolling="no" src="https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F110367442" width="100%"></iframe>

### Hのみ取り出して再合成した音源

<iframe frameborder="no" height="166" scrolling="no" src="https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F110367534" width="100%"></iframe>

### Pのみ取り出して再合成した音源

<iframe frameborder="no" height="166" scrolling="no" src="https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F110367599" width="100%"></iframe>

それにしても特に泥臭い努力をせずに、このクオリティーが出せるのはすごい。音源に対する事前知識も何もないし。あと、ちょっとノイズが載ってるのはたぶんプログラムミス。つらたーん

コレ以外にも多重HPSSとかもやったけど、いやーおもしろい手法だなーと思いました（こなみ

詳しくは論文へ（僕のじゃないけど

## 参考

- [橘 秀幸, 小野 順貴, 嵯峨山 茂樹, "スペクトルの時間変化に基づく音楽音響信号からの歌声成分の強調と抑圧", 情報処理学会研究報告, vol. 2009-MUS-81(12), pp. 1-6, 2009.](http://ci.nii.ac.jp/naid/110007997346)
