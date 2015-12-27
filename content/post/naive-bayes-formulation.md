---
layout: post
title: "Naive Bayesの復習（導出編）"
date: 2013-07-28
comments: true
categories: machine-learning
---

すぐ忘れるのでメモ。ナイーブベイズの学習アルゴリズムの導出とか、そもそもナイーブベイズが定番過ぎて意外とやったことなかった気もするので、復習がてらやってみた。

ちょっと修正 2013/07/30

- ナイーブベイズについて整理
- 学習アルゴリズムの導出


## Naive bayes （ナイーブベイズ）

スパムフィルタで使われたことで有名な確率モデルで、シンプルだけどそこそこ実用的なのが良い所。Naive bayesという名前は、特徴ベクトル間に条件付き独立性を仮定してることにある（実際は相関あることが多いけど、まぁ簡単のためって感じ）。具体的に例を挙げて言うと、例えば文書分類タスクの場合、各単語は独立に生起するという仮定を置くことに相当する。

まずはモデルを書き下す。入力データを$\mathbf{x}$（D次元）、ラベルを$y$（離散値）とすると、ナイーブベイズでは以下のように同時確率をモデル化する。

<div>
\begin{align}
p(\mathbf{x}, y) &= p(y)p(\mathbf{x}|y)\\
&= p(y)p(x_{1}, x_{2}, \dots, x_{D}|y)\\
&= p(y)\prod_{d=1}^{D} p(x_{d}|y)
\end{align}
</div>

カンタン。基本的にdは次元に対するインデックス、nはデータに対するインデックスとして書く。

ポイントは特徴ベクトル間に条件付き独立性の仮定を置いていること（二度目）で、それによってパラメータの数が少なくて済む。

## 分類

一番確率の高いラベルを選べばいい。数式で書くと以下のようになる。

<div>
\begin{align}
\hat{y} &= \argmax_{y} [p(y|\mathbf{x})]\\
 &= \argmax_{y} [p(\mathbf{x}, y)]\\
 &= \argmax_{y} \Bigl[ p(y)\prod_{d=1}^{D} p(x_{d}|y)\Bigr]
\end{align}
</div>

argmaxを取る上では、$y$に依存しない項は無視していいので、事後確率の最大化は、同時確率の最大化に等しくなる。

## 学習アルゴリズムの導出

ここからが本番。学習データを$X = \{\mathbf{x}\_{n}\}\_{n=1}^{N}$、対応する正解ラベルを$Y = \{y_n\}\_{n=1}^{N} $として、最尤推定により学習アルゴリズムを導出する。実際はMAP推定をすることが多いけど、今回は省略。拡張は簡単。

### 尤度関数

各サンプルが独立に生起したと仮定すると、尤度関数は以下のように書ける。

<div>
\begin{align}
L(X,Y; \mathbf{\theta}) &= \prod_{n=1}^{N}p(y_{n})p(\mathbf{x_{n}}|y_{n})\\
&= \prod_{n=1}^{N} \Bigl[ p(y_{n})\prod_{d=1}^{D}p(x_{nd}|y_{n})\Bigr]
\end{align}
</div>

対数を取って、

<div>
\begin{align}
\log L(X,Y; \mathbf{\theta}) =  \sum_{n=1}^{N}\Bigl[\log p(y_{n}) + \sum_{d=1}^{D}\log p(x_{nd}|y_{n})\Bigr]
\end{align}
</div>

学習アルゴリズムは、この関数の最大化として導くことができる。

### ところで

特徴ベクトルにどのような分布を仮定するかでアルゴリズムが少し変わるので、今回は以下の二つをやってみる。

- ベルヌーイ分布
- 正規分布

前者は、binary featureを使う場合で、後者は、continuous featureを使う場合を想定してる。画像のピクセル値とか連続値を扱いたい場合は、正規分布が無難。その他、多項分布を使うこともあるけど、ベルヌーイ分布の場合とほとんど一緒なので今回は省略

ラベルに対する事前分布は、ラベルが離散値なので多項分布（間違ってた）categorical distributionとする。日本語でなんて言えばいいのか…[wikipedia](http://en.wikipedia.org/wiki/Categorical_distribution) 参考

## Bernoulli naive bayes

特徴ベクトルにベルヌーイ分布を仮定する場合。0 or 1のbinary featureを使う場合にはこれでおｋ．ベルヌーイ分布は以下

<div>
\begin{align}
p(x;q) = q^{x}(1-q)^{1-x}
\end{align}
</div>

特徴ベクトルに対するパラメータは、ラベル数×特徴ベクトルの次元数（L×D）個ある。対数尤度関数（Gとする）は、以下のように書ける。

<div>
\begin{align}
G &=  \sum_{n=1}^{N}\Bigl[ \log \pi_{y_{n}} \notag \\
 &+ \sum_{d=1}^{D} \bigl[ x_{nd} \log q_{y_{n}d} + (1-x_{nd}) \log (1-q_{y_{n}d}) \bigr] \Bigr]
\end{align}
</div>

ここで、$\pi\_{y\_{n}}$ はcategorical distributionのパラメータ。

### 微分方程式を解く

あとは微分してゼロ。ラベルに対するインデックスをl 、学習データ中のラベルlが出現する回数を$N\_{l} = \sum\_{n=1}^{N} \delta(y\_{n}= l)$、さらにその中で$x\_{nd}=1 $となる回数を$N\_{ld} = \sum\_{n=1}^{N} \delta(y\_{n}= l) \cdot x\_{nd} $とすると、

<div>
\begin{align}
\frac{\partial G}{\partial q_{ld}} &= \frac{N_{ld}}{q_{ld}} - \frac{N_{l} - N_{ld}}{1-q_{ld}}  = 0
\end{align}
</div>

よって、

<div>
\begin{align}
q_{ld} = \frac{N_{ld}}{N_{l}} \label{eq:naive1}
\end{align}
</div>

できました。厳密に数式で書こうとするとめんどくさい。日本語で書くと、

<div>
\begin{align}
パラメータ = \frac{特徴ベクトルの出現回数}{ラベルの出現回数}
\end{align}
</div>

って感じでしょうか。

categoricalのパラメータについては、めんどくさくなってきたのでやらないけど、もう直感的に以下。ラグランジュの未定定数法でおｋ

<div>
\begin{align}
\pi_{l} = \frac{N_{l}}{N} \label{eq:naive2}
\end{align}
</div>

学習は、式 ($\ref{eq:naive1}$)、($\ref{eq:naive2}$) を計算すればおｋ．やっと終わった。。。長かった。

## Gaussian naive bayes

次。$x$が連続変数で、その分布に正規分布（Gaussian）を仮定する場合。まず、正規分布は以下のとおり。

<div>
\begin{align}
p(x; \mu, \sigma^{2}) = \frac{1}{\sqrt{2\pi\sigma^{2}}}\exp\Bigl\{-\frac{(x-\mu)^{2}}{2\sigma^{2}}\Bigr\}
\end{align}
</div>

正規分布を使う場合、特徴ベクトルに対するパラメータは、ラベル数×特徴ベクトルの次元数×2個ある。×2となっているのは、平均と分散の分。対数尤度関数は、以下のようになる

<div>
\begin{align}
G &=  \sum_{n=1}^{N}\Bigl[ \log \pi_{y_{n}} \notag \\
 &+ \sum_{d=1}^{D} \bigl[ -\frac{1}{2}\log 2\pi - \log\sigma_{y_{n}d} -  \frac{(x_{nd}-\mu_{y_{n}d})^2}{2\sigma_{y_{n}d}} \bigr] \Bigr]
\end{align}
</div>

### 微分方程式を解く

計算は省略するけど、偏微分してゼロと置けば、結果は以下のようになる。式が若干煩雑だけど、基本的には正規分布の最尤推定をしてるだけ。

<div>
\begin{align}
\mu_{ld} = \frac{1}{N_{l}} \sum_{n=1}^{N} x_{nd} \cdot \delta(y_{n} =l) = \frac{N_{ld}}{N_{l}} \label{eq:naive3}
\end{align}
</div>

<div>
\begin{align}
\sigma_{ld} = \frac{1}{N_{l}} \sum_{n=1}^{N} (x_{nd}-\mu_{ld})^{2} \cdot \delta (y_{n}= l) \label{eq:naive4}
\end{align}
</div>

学習では、式 ($\ref{eq:naive2}$)、($\ref{eq:naive3}$)、($\ref{eq:naive4}$)を計算すればおｋ．式 ($\ref{eq:naive3}$)は式 ($\ref{eq:naive1}$)と一緒なんだけど、正規分布の場合はxが連続値なので注意。分散が特徴ベクトルの次元によらず一定とすれば、パラメータの数をぐっと減らすこともできる。

## おわりに

これで終わり。予想以上に書くのに時間かかった…。今日logistic regressionを見直してて、ふとnaive bayesやったことないなーと思って、まぁ試すだけならscipy使えば一瞬なんだろうけどちょっと導出までやってみようと思った。

実装編→[Naive Bayesの復習（実装編）: MNISTを使って手書き数字認識](http://r9y9.github.io/blog/2013/08/06/naive-bayes-mnist/)

## 参考

- [scikit.learn手法徹底比較！ ナイーブベイズ編Add Star - Risky Dune](http://d.hatena.ne.jp/saket/20130212/1360678478)
- [Gaussian Naïve Bayes, andLogistic Regression](http://www.cs.cmu.edu/~epxing/Class/10701-10s/Lecture/lecture5.pdf)
- [ナイーブベイズを用いたテキスト分類 - 人工知能に関する断創録](http://aidiary.hatenablog.com/entry/20100613/1276389337)
