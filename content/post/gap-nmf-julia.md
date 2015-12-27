---
layout: post
title: Gamma Process Non-negative Matrix Factorization (GaP-NMF) in Julia
date: 2014-08-20
comments: true
categories: Julia Machine-Learning
---

最近 [Julia](julialang.org) で遊んでいて、その過程で非負値行列因子分解（NMF）のノンパラ版の一つであるGamma Process Non-negative Matrix Factorization (GaP-NMF) を書いてみました。（まぁmatlabコードの写経なんですが）

https://github.com/r9y9/BNMF.jl

元論文:
 [Bayesian Nonparametric Matrix Factorization for Recorded Music](http://soundlab.cs.princeton.edu/publications/2010_icml_gapnmf.pdf)
by Matthew D. Hoffman et al. in ICML 2010.

## デモ

http://nbviewer.ipython.org/github/r9y9/BNMF.jl/blob/master/notebook/GaP-NMF.ipynb

適当な音声（音楽じゃなくてごめんなさい）に対して、GaP-NMFをfittingしてみた結果のメモです。$K=100$ で始めて、100回ほどイテレーションを回すと適度な数（12くらい）にtruncateしているのがわかると思います。予めモデルの複雑度を指定しなくても、データから適当な数を自動決定してくれる、ノンパラベイズの良いところですね。

## ハマったところ

- GIGの期待値を求めるのに必要な第二種変形ベッセル関数は、exponentially scaled versionを使いましょう。じゃないとInf地獄を見ることになると思います（つらい）。Juliaで言うなら [besselkx](https://julia.readthedocs.org/en/latest/stdlib/base/?highlight=besselkx#Base.besselkx) で、scipyで言うなら [scipy.special.kve](http://students.mimuw.edu.pl/~pbechler/scipy_doc/generated/scipy.special.kve.html#scipy.special.kve) です。

## 雑感

- MatlabのコードをJuliaに書き直すのは簡単。ところどころ作法が違うけど（例えば配列の要素へのアクセスはmatlabはA(i,j)でJuliaはA[i,j]）、だいたい一緒
- というかJuliaがMatlabに似すぎ？
- Gamma分布に従う乱数は、[Distributions,jl](https://github.com/JuliaStats/Distributions.jl) を使えばめっちゃ簡単に生成できた。素晴らしすぎる
- 行列演算がシンプルにかけてホント楽。pythonでもmatlabでもそうだけど（Goだとこれができないんですよ…）
- 第二種変形ベッセル関数とか、scipy.special にあるような特殊関数が標準である。素晴らしい。

## Python版と速度比較

[bp_nmf/code/gap_nmf](https://github.com/dawenl/bp_nmf/tree/master/code/gap_nmf) と比較します。matlabはもってないので比較対象からはずします、ごめんなさい

Gistにベンチマークに使ったスクリプトと実行結果のメモを置いときました
https://gist.github.com/r9y9/3d0c6a90dd155801c4c1

結果だけ書いておくと、あらゆる現実を（ry の音声にGaP-NMFをepochs=100でfittingするのにかかった時間は、

```
Julia: Mean elapsed time: 21.92968243 [sec]
Python: Mean elapsed time: 18.3550617 [sec]
```

という結果になりました。つまりJuliaのほうが1.2倍くらい遅かった（僕の実装が悪い可能性は十分ありますが）。どこがボトルネックになっているのか調べていないので、気が向いたら調べます。Juliaの方が速くなったらいいなー

## おわりに

GaP-NMFの実装チャレンジは二回目でした。（たぶん）一昨年、年末に実家に帰るときに、何を思ったのか急に実装したくなって、電車の中で論文を読んで家に着くなり実装するというエクストリームわけわからんことをしていましたが、その時はNaN and Inf地獄に負けてしまいました。Pythonで書いていましたが、今見るとそのコードマジクソでした。

そして二回目である今回、最初はmatlabコードを見ずに自力で書いていたんですが、またもやInf地獄に合いもうだめだと思って、matlabコードを写経しました。あんま成長していないようです（つらい）

Julia歴二週間くらいですが、良い感じなので使い続けて見ようと思います。
