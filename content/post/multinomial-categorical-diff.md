---
layout: post
title: "Multinomial distributionとCategorical distributionの違い"
date: 2013-07-31
comments: true
categories: probability
---

些細な違いなんだけど調べたのでメモ。Multinomial distributionは多項分布のこと。Categorical distributionは、一般的な日本語表現が見つからなかった（なのでタイトルは英語）。打つのが大変なので、以下カテゴリカル分布と書く。

結論としては、多項分布のn=1の特殊な場合がカテゴリカル分布ですよってこと。以下少しまとめる。

分布を仮定する離散変数をカテゴリと呼ぶとして、

- 多項分布は、n回試行したときに各カテゴリが何回出るかを表す確率分布
- 多項分布は、二項分布を多カテゴリに一般化したもの
- カテゴリカル分布は、多項分布のn=1の場合に相当する
- カテゴリカル分布は、ベルヌーイ分布を多カテゴリに一般化したもの

以上

nokunoさんによるこの記事→ [多項分布の最尤推定](http://d.hatena.ne.jp/nokuno/20111006/1317853653) は、多項分布というよりカテゴリカル分布の話。本文には書いてあるけどね。あと最尤推定の結果はどちらにしろ同じなんだけどね

## 導出メモ

一応最尤推定をやってみる。前回のナイーブベイズのメモの時は省略したので。入力の変数を $ Y = \{y\_n\}_{n=1}^{N} $ とする。

### カテゴリカル分布

<div>
\begin{align}
p(l) = \pi_{l}, \hspace{2mm} \sum_{l=1}^{L}\pi_{l} = 1
\end{align}
</div>

ここで、$\pi_{l}$がパラメータ、lはカテゴリの番号

### 最尤推定

尤度関数を立てて、最大化することでパラメータを求める。各データは独立に生起すると仮定すると、尤度関数は以下のようになる。

<div>
\begin{align}
L(Y; \theta) = \prod_{n=1}^{N} \pi_{y_{n}}
\end{align}
</div>

$\theta$はパラメータの集合ということで。

ラベルlの出現回数を$N\_{l} = \sum\_{n=1}^{N} \delta (y\_{n} = l)$とすると、次のように書き直せる。

<div>
\begin{align}
L(Y; \theta) = \prod_{l=1}^{L}\pi_{l}^{N_{l}}
\end{align}
</div>

よって、対数尤度は以下のようになる。

<div>
\begin{align}
\log L(Y; \theta) = \sum_{l=1}^{L} N_{l}\log \pi_{l}
\end{align}
</div>

### ラグランジュの未定乗数法で解く

nokunoさんの記事の通りだけど、一応手でも解いたのでメモ

<div>
\begin{align}
G = \sum_{l=1}^{L} N_{l}\log \pi_{l} + \lambda \Bigl[ \sum_{l=1}^{L} \pi_{l} -1) \Bigr]
\end{align}
</div>
として、

<div>
\begin{align}
\frac{\partial G}{\partial \pi_{l}} = \frac{N_{l}}{\pi_{l}} + \lambda  =0
\end{align}
</div>

よって、

<div>
\begin{align}
\pi_{l} = -\frac{N_{l}}{\lambda}
\end{align}
</div>

ここで、以下の制約条件に代入すると、

<div>
\begin{align}
\sum_{l=1}^{L} \pi_{l} = 1
\end{align}
</div>

$\lambda = -N$となることがわかるので、求めたかったパラメータは以下のようになる

<div>
\begin{align}
\pi_{l} = \frac{N_{l}}{N}
\end{align}
</div>

カテゴリの頻度を計算するだけ、カンタン！！


## 参考

- [Categorical distribution - Wikipedia](http://en.wikipedia.org/wiki/Categorical_distribution)
- [Multinomial distribution - Wikipedia](http://en.wikipedia.org/wiki/Multinomial_distribution)
- [多項分布の最尤推定 - nokunoの日記](http://d.hatena.ne.jp/nokuno/20111006/1317853653)
- [多項分布の最尤推定とMAP推定 - 睡眠時間？](http://d.hatena.ne.jp/sleepy_yoshi/20111107/p1)
- [Categorical distribution - Researcher's Eye](http://lef-t.blogspot.jp/2013/02/categorical-distribution-wikipedia-free.html)
