---
layout: post
title: "NMFアルゴリズムの導出（ユークリッド距離版）"
date: 2013-07-27
comments: true
categories: machine-learning matrix-factorization
---

## はじめに

シングルトラックにミックスダウンされた音楽から、その構成する要素（例えば、楽器とか）を分離したいと思うことがある。
音源分離と言えば、最近はNon-negative Matrix Factorization (非負値行列因子分解; NMF) が有名。
実装は非常に簡単だけど、実際にやってみるとどの程度の音源分離性能が出るのか気になったので、やってみる。

と思ったけど、まずNMFについて整理してたら長くなったので、実装は今度にして、まずアルゴリズムを導出してみる。

## 2014/10/19 追記

実装しました

https://github.com/r9y9/julia-nmf-ss-toy

## NMFの問題設定

NMFとは、与えられた行列を非負という制約の元で因子分解する方法のこと。
音楽の場合、対象はスペクトログラムで、式で書くとわかりやすい。
スペクトログラムを $\mathbf{Y}: [\Omega \times T] $
    とすると、

<div>
\begin{align}
\mathbf{Y} \simeq \mathbf{H} \mathbf{U}
\end{align}
</div>

となる、$\mathbf{H}: [\Omega \times K]、\mathbf{U}: [K \times T]$ を求めるのがNMFの問題。
ここで、Hが基底、Uがアクティビティ行列に相当する。
NMFは、元の行列Yと分解後の行列の距離の最小化問題として定式化できる。

<div>
\begin{align}
\mathbf{H}, \mathbf{U} = \mathop{\rm arg~min}\limits_{\mathbf{H}, \mathbf{U}} D (\mathbf{Y}|\mathbf{H}\mathbf{U}), \hspace{3mm} {\rm subect\ to} \hspace{3mm} H_{\omega,k}, U_{k, t} > 0
\end{align}
</div>

すごくシンプル。Dは距離関数で色んなものがある。ユークリッド距離、KLダイバージェンス、板倉斎藤距離、βダイバージェンスとか。

## ユークリッド距離の最小化

ここではユークリッド距離（Frobeniusノルムともいう）として、二乗誤差最小化問題を解くことにする。
一番簡単なので。最小化すべき目的関数は次のようになる。

<div>
\begin{align}
D (\mathbf{Y}|\mathbf{H}\mathbf{U}) =& || \mathbf{Y}-\mathbf{HU}||_{F} \\
=& \sum_{\omega, k}|Y_{\omega,t} - \sum_{k}H_{\omega, k}U_{k, t}|^{2}
\end{align}
</div>

行列同士の二乗誤差の最小化は、要素毎の二乗誤差の和の最小化ということですね。展開すると、次のようになる。

<div>
\begin{align}
\sum_{\omega, k}|Y_{\omega,t} - \sum_{k}H_{\omega, k}U_{k, t}|^{2}
= \sum_{\omega, t}(|Y_{\omega, t}|^2 -2Y_{\omega, t} \sum_{k}H_{\omega, k}U_{k, t} + |\sum_{k}H_{\omega, k}U_{k, t}|^2)
\end{align}
</div>

微分してゼロ！としたいところだけど、3つ目の項を見ると、絶対値の中に和が入っているので、そうはいかない。
なので、補助関数法を使う。
基本的なアイデアは、目的関数の直接の最適化が難しい場合には、上界関数を立てることで間接的に最小化するということ。

3項目に対してイェンセンの不等式を適応すると、

<div>
\begin{align}
|\sum_{k}H_{\omega,k}U_{k,t}|^{2} \le \sum_{k} \frac{H_{\omega,k}^{2}U_{k, t}^{2}}{\lambda_{k, \omega, t}}
\end{align}
</div>

これで、右辺は $ H\_{\omega,k}, U\_{k, t} $ について二次関数になったので、微分できてはっぴー。
上の不等式を使えば、実際に最小化する目的関数は、次のようになる。

<div>
\begin{align}
G := \sum_{\omega, t}(|Y_{\omega, t}|^2 -2Y_{\omega, t} \sum_{k}H_{\omega, k}U_{k, t} + \sum_{k} \frac{H_{\omega,k}^{2}U_{k, t}^{2}}{\lambda_{k, \omega, t}})
\end{align}
</div>

Gを最小化すれば、間接的に元の目的関数も小さくなる。

## 更新式の導出

あとは更新式を導出するだけ。
まず、目的関数を上から押さえるイメージで、イェンセンの不等式の等号条件から補助変数の更新式を求める。
この場合、kに関して和が1になることに注意して、

<div>
\begin{align}
\lambda_{k,\omega,t} = \frac{H_{\omega, k}U_{k, t}}{\sum_{k'}H_{\omega, k'}U_{k', t}}
\end{align}
</div>

次に、目的関数Gを $H\_{\omega,k}, U\_{k,t} $で偏微分する。

<div>
\begin{align}
\frac{\partial G}{\partial H_{\omega,k}} &= \sum_{t} (-2 Y_{\omega,t}U_{k,t} + 2 \frac{H_{\omega, k}U_{k, t}^2}{\lambda_{k,\omega,t}}) &= 0\\
\frac{\partial G}{\partial U_{k, t}} &= \sum_{\omega} (-2 Y_{\omega,t}H_{\omega,k} + 2 \frac{H_{\omega, k}^2U_{k, t}}{\lambda_{k,\omega,t}}) &= 0
\end{align}
</div>

少し変形すれば、以下の式を得る。

<div>
\begin{align}
H_{\omega,k} = \frac{\sum_{t}Y_{\omega,t}U_{k,t}}{\sum_{t}\frac{U_{k, t}^2}{\lambda_{k,\omega,t}}}, \hspace{3mm}
U_{k,t} = \frac{\sum_{\omega}Y_{\omega,t}H_{\omega,k}}{\sum_{\omega}\frac{H_{\omega, k}^2}{\lambda_{k,\omega,t}}}
\end{align}
</div>

補助変数を代入すれば、出来上がり。

<div>
\begin{align}
H_{\omega,k} = H_{\omega,k} \frac{\sum_{t}Y_{\omega,t}U_{k,t}}{\sum_{t}U_{k, t}\sum_{k'}H_{\omega, k'}U_{k', t}}, \hspace{3mm}
U_{k,t} = U_{k,t}\frac{\sum_{\omega}Y_{\omega,t}H_{\omega,k}}{\sum_{\omega}H_{\omega, k}\sum_{k'}H_{\omega, k'}U_{k', t}}
\end{align}
</div>

## 行列表記で

これで終わり…ではなく、もう少しスマートに書きたい。
ここで、少し実装を意識して行列表記を使って書きなおす。
行列の積は、AB（A: [m x n] 行列、B: [n x l] 行列）のようにAの列数とBの行数が等しくなることに注意して、
ほんの少し変形すれば最終的には次のように書ける。

<div>
\begin{align}
H_{\omega,k} &= H_{\omega,k} \frac{[\mathbf{Y}\mathbf{U}^{\mathrm{T}}]_{\omega,k}}{[\mathbf{H}\mathbf{U}\mathbf{U}^{\mathrm{T}}]_{\omega,k}}, \\
U_{k,t} &= U_{k,t}\frac{[\mathbf{H}^{\mathrm{T}}\mathbf{Y}]_{k, t}}{[\mathbf{H}^{\mathrm{T}}\mathbf{H}\mathbf{U}]_{k,t}}
\end{align}
</div>

乗法更新式というやつですね。
元々の行列の要素が非負なら、掛けても非負のままですよってこと。
NMFのアルゴリズムは、この更新式を目的関数が収束するまで計算するだけ、簡単。Pythonなら数行で書ける。

## メモ

自分で導出していて思ったことをメモっておこうと思う。

- 更新式は、行列の要素毎に独立して求められるんだなぁということ。
    - まぁ要素毎に偏微分して等式立ててるからそうなんだけど。更新の順番によって、収束する値、速度が変わるといったことはないんだろうか。
- 行列演算とスカラー演算が同じ式に同時に含まれていることがあるので注意。例えば、最終的な更新式の割り算は、要素毎のスカラー演算で、行列演算ではない。
- 何かいっぱいシグマがあるけど、めげない。計算ミスしやすい、つらい。
- NMFという名前から行列操作を意識してしまうけど、更新式の導出の過程に行列の微分とか出てこない。更新式の導出は、行列の要素個々に対して行うイメージ。

NMFなんて簡単、と言われますが（要出典）、実際にやってみると結構めんどくさいなー、と思いました（小並感
