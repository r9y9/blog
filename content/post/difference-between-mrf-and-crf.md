---
layout: post
title: "マルコフ確率場 (MRF) と条件付き確率場 (CRF) の違い"
date: 2014-03-01
comments: true
categories: Graphical-Model
---

一番の違いは、生成モデルか識別モデルか、ということ。それぞれ、

- Markov Random Fields (MRF) は生成モデル
- Conditional Random Fields (CRF) は識別モデル

です。

- [What is exactly the difference between MRF and CRF](http://metaoptimize.com/qa/questions/4021/what-is-exactly-the-difference-between-mrf-and-crf)

ここを見ると割とすっきりする。

ただ、少しスムーズに納得できないことがありまして…それは、MRFもCRFもグラフィカルモデルで書くと無向グラフとなること。識別モデルは無向グラフで生成モデルは有向グラフなんじゃ…？と思ってしまう人もいるんじゃないかと思う（いなかったらごめんなさい）。

## グラフィカルモデルとしての表現

一般に、生成モデルは有向グラフの形で記述され、識別モデルは無向グラフとして記述される。例えば、隠れマルコフモデル (HMM) は有向グラフで、条件付き確率場 (CRF) は無向グラフで表される。図を貼っておく

<div align="center"><img src="/images/HMM_and_CRF.png" class="image"></div>

その道の人には、馴染みのある図だと思う（ｼｭｳﾛﾝから引っ張ってきた）。グレーの○が観測変数、白い○が隠れ変数です

ここで重要なのは、例外もあるということ。具体的には、タイトルにあるMRFは生成モデルだけど無向グラフで書かれる。MRFというと、例えばRestricted Boltzmann Machine とかね！

単純なことだけど、これを知らないとMRFについて学習するときにつっかかってしまうので注意

[An Introduction to Conditional Random Fields](http://homepages.inf.ed.ac.uk/csutton/publications/crftut-fnt.pdf) の2.2 Generative versus Discriminative Models から引用すると、

> Because a generative model takes the form p(y,x) = p(y)p(x|y), it is often natural to represent a generative model by a directed graph in which in outputs y topologically precede the inputs. Similarly, we will see that it is often natural to represent a discriminative model by a undirected graph. However, this need not always be the case, and both undirected generative models, such as the Markov random ﬁeld (2.32), and directed discriminative models, such as the MEMM (6.2), are sometimes used. It can also be useful to depict discriminative models by directed graphs in which the x precede the y.

らしいです

## 結論

- 生成モデル＝有向グラフ、識別モデル＝無向グラフで**表されるとは限らない**
- ことMRFに関して言えば生成モデルだけど無向グラフで表されるよ

ということです

さらに言えば、MRFとCRFはグラフィカルモデルでは同じように書けてしまうけれど、両者には明確な違いがあることに気をつけましょう、ということです（ちょっと自信ない）

間違っていたら教えて下さい

## 参考

- [What is exactly the difference between MRF and CRF](http://metaoptimize.com/qa/questions/4021/what-is-exactly-the-difference-between-mrf-and-crf)
- [An Introduction to Conditional Random Fields (PDF)](http://homepages.inf.ed.ac.uk/csutton/publications/crftut-fnt.pdf)
- [More about Undirected Graphical Models](http://www.cs.helsinki.fi/group/cosco/Teaching/Probability/2010/lecture5_MRF2.pdf)
