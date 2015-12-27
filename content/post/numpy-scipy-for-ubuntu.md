---
layout: post
title: "UbuntuでNumpy, Scipyをソースからインストール"
date: 2013-08-12
comments: true
categories: python ubuntu
---

<div align="center"><img src="/images/numpy_scipy_version_terminal.png" class="image"></div>

apt-getを使う場合→[ubuntuにnumpy, scipy, matplotlib環境を構築 - sat0yuの日記](http://d.hatena.ne.jp/sat0yu/20130302/1362172589
)
ただやっぱり最新版を使いたいということがある。というわけでメモ。
Ubuntu 12.04 desktopを想定する（他でもほぼ同様の手順でインストールできると思う）。

## 準備

```bash
sudo apt-get install python python-dev gcc gfortran g++
```

## Numpyのインストール

```bash
git clone https://github.com/numpy/numpy
cd numpy
python setup.py build
sudo python setup.py install
```

かんたん


## Scipyのインストール

これがちょっとめんどい。numpyのようには行かなかった。2013/08/12

### 前準備

以下をインストール

- numpy （上の通りでおｋ）
- blas/lapack
- cython

## cythonのインストール

これ、apt-get install cython でも入るんだけど、バージョンが古いって怒られた。なので、cythonもソースからいれる

```
git clone https://github.com/cython/cython
cd cython
python setup.py build
sudo python setup.py install
```

かんたん

## blas/lapackのインストール

これはapt-getから入れればおｋ

```bash
sudo apt-get install libblas-dev liblapack-dev
```

scipyのINSTALL.txt （リンク）を見るに、libatlas3-base-devをインストールすれば良さそうだけど、ubuntu 12.04じゃ見つからんかった（2013/08/12時点で）。で、何となく試してたら、libblas-devとliblapack-devで行けた。

## Scipyのインストール！

これでやっとインストールできる

```
git clone https://github.com/scipy/scipy
cd scipy
python setup.py build
sudo python setup.py install
```

終わり。
