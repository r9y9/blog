---
layout: post
title: "Naive Bayesの復習（実装編）: MNISTを使って手書き数字認識"
date: 2013-08-06
comments: true
categories: machine-learning digit-recognition
---

前回は学習アルゴリズムを導出したので、今回はそれを実装する。Gaussian Naive Bayesのみやった。例によって、アルゴリズムを書く時間よりも言語の使い方等を調べてる時間などの方が圧倒的に多いという残念感だったけど、とりあえずメモる。python, numpy, scipy, matplotlibすべて忘れてた。どれも便利だから覚えよう…

そもそもナイーブベイズやろうとしてたのも、MNISTのdigit recognitionがやりたかったからなので、実際にやってみた。

コードはgithubに置いた https://github.com/r9y9/naive_bayes

結果だけ知りたい人へ：正解率  76 %くらいでした。まぁこんなもんですね

## 手書き数字認識

手書き数字の画像データから、何が書かれているのか当てる。こういうタスクを手書き数字認識と言う。郵便番号の自動認識が有名ですね。

今回は、MNISTという手書き数字のデータセットを使って、0〜9の数字認識をやる。MNISTについて詳しくは本家へ→[THE MNIST DATABASE of handwritten digits](http://yann.lecun.com/exdb/mnist/)
ただし、MNISTのデータセットは直接使わず、Deep Learningのチュートリアルで紹介されていた（[ここ](http://deeplearning.net/tutorial/gettingstarted.html#gettingstarted)）、pythonのcPickleから読める形式に変換されているデータを使った。感謝

## とりあえずやってみる

```bash
$ git clone https://github.com/r9y9/naive_bayes
$ cd naive_bayes
$ python mnist_digit_recognition.py
```

プログラムの中身は以下のようになってる。

- MNISTデータセットのダウンロード
- モデルの学習
- テスト

実行すると、学習されたGaussianの平均が表示されて、最後に認識結果が表示される。今回は、単純に画像のピクセル毎に独立なGaussianを作ってるので、尤度の計算にめちゃくちゃ時間かかる。実装のせいもあるけど。なので、デフォでは50サンプルのみテストするようにした。


## 学習されたGaussianの平均

<div align="center"><img src="/images/mnist_mean_of_gaussian.png "gaussian means"" class="image"></div>

学習されたGaussianの平均をプロットしたもの。上のコードを実行すると表示される。

それっぽい。学習データは50000サンプル


## 認識結果

時間がかかるけど、テストデータ10000個に対してやってみると、結果は以下のようになった。

`0.7634 (7634/10000)`

まぁナイーブベイズなんてこんなもん。もちろん、改善のしようはいくらでもあるけれども。ちなみにDeep learningのチュートリアルで使われてたDBN.pyだと0.987くらいだった。

## 感想

相関が強い特徴だと上手くいかんのは当たり前で、ピクセル毎にGaussianなんて作らずに（ピクセル間の相関を無視せずに）、少しまともな特徴抽出をかませば、8割りは超えるんじゃないかなぁと思う。

あとこれ、実装してても機械学習的な面白さがまったくない（上がれ目的関数ｩｩーー！的な）ので、あまりおすすめしません。おわり。

[導出編→Naive Bayesの復習（導出編）](http://r9y9.github.io/blog/2013/07/28/naive-bayes-formulation/)


## 参考

- [機械学習のPythonとの出会い（１）：単純ベイズ基礎編 - slideshare](http://www.slideshare.net/shima__shima/python-13349162)
