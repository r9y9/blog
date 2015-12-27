---
layout: post
title: Pylearn2, theanoをEC2 g2.x2large で動かす方法
date: 2014-07-20
comments: true
categories: machine-learning ec2 gpu
---

<div align="center"><img src="/images/dbm_learned_from_mnist.png "Weight visualization of Restricted bolztomann machine trained on MNIST dataset."" class="image"></div>

## モチベーション

- 手元のへぼマシンでニューラルネットの学習を回わす
- 半日たっても終わらない
- 最近だとGPU使って計算を高速化するのが流行りだが、手元にGPUはない

[Deep Learning in Python with Pylearn2 and Amazon EC2](http://www.kurtsp.com/deep-learning-in-python-with-pylearn2-and-amazon-ec2.html)

手元にGPUがない…？大丈夫！Amazon EC2を使えば良さそう！！！

というわけで、めんどくさいと言わずにec2にお手軽計算環境を整えます。ec2でGPUが乗ったものだと、g2.2xlargeがよさそうですね。

ちなみに↑の図、pylearn2のtutorialのRestricted Bolzmann MachinesをMNISTで学習した結果なんですが、手元のマシンだとだいたい6時間くらい？（忘れた）だったのがg2.2xlargeだと30分もかかってない（ごめんなさい時間図るの忘れた）。$0.65/hourと安いんだし（他のインスタンスに比べればそりゃ高いけど）、もう手元のマシンで計算するの時間の無駄だしやめようと思います。

さてさて、今回環境構築に少しはまったので、もうはまらないように簡単にまとめておきます。

## 結論

[Amazon Linux AMI with NVIDIA GRID GPU Driver on AWS Marketplace ](https://aws.amazon.com/marketplace/pp/B00FYCDDTE)

すでにNVIDIAのドライバとCUDA（5.5）が入ったインスタンスをベースに使いましょう。

[EC2(g2.2xlarge)でOpenGLを使う方法](http://xanxys.hatenablog.jp/entry/2014/05/17/135932) で挙げられているように普通のlinuxを使う方法もありますが、ハマる可能性大です。僕はubuntuが使いたかったので最初はubuntu 14.04 server でドライバ、cuda (5.5 or 6.0) のインストールを試しましたが同じように失敗しました。

イケイケと噂の音声認識ライブラリKaldiの[ドキュメントらしきもの](https://220-135-252-130.hinet-ip.hinet.net/speechwiki/index.php/Kaldi#installing_and_testing_CUDA-6.0_in_Ubuntu_14.04)を見ると、Ubuntu 14.04でもcuda 6.0インストールできるっぽいんですけどね…だめでした。頑張ればできるかもしれませんが、よほど強いメリットがない場合は、おとなしくpre-installされたインスタンスを使うのが吉だと思います。

## セットアップ

↑で上げたインスタンスにはGPUドライバやCUDAは入っていますが、theanoもpylearn2もnumpyもscipyも入っていません。よって、それらは手動でインストールする必要があります。

というわけで、インストールするシェルをメモって置きます。試行錯誤したあとに適当にまとめたshellなので、なんか抜けてたらごめんなさい。

https://gist.github.com/r9y9/50f13ba28b5b158c25ae

```bash
#!/bin/bash

# Pylearn2 setup script for Amazon Linux AMI with NVIDIA GRID GPU Driver.
# http://goo.gl/3KeXXW

sudo yum update -y
sudo yum install -y emacs tmux python-pip
sudo yum install -y python-devel git blas-devel lapack-devel

# numpy, scipy, matplotlib, etc.
sudo pip install numpy
sudo pip install scipy
sudo pip install cython
sudo pip install ipython nose

# matplotlib
sudo yum install -y libpng-devel freetype-devel
sudo pip install matplotlib

# Scikit-learn
sudo pip install scikit-learn

# Theano
sudo pip install --upgrade git+git://github.com/Theano/Theano.git

# Enable GPU for theano
echo '[global]
floatX = float32
device = gpu0

[nvcc]
fastmath = True' > .theanorc

# pylearn2
git clone git://github.com/lisa-lab/pylearn2.git
cd pylearn2
sudo python setup.py develop
cd ..

echo "export PYLEARN2_DATA_PATH=/home/ec2-user/data" >> .bashrc

# MNIST dataset
mkdir -p data/mnist/
cd data/mnist/
wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
gunzip train-images-idx3-ubyte.gz
wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
gunzip train-labels-idx1-ubyte.gz
wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
gunzip t10k-images-idx3-ubyte.gz
wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
gunzip t10k-labels-idx1-ubyte.gz
cd ../..
```

簡単ですね

また、上記のような手順を踏まなくても、Community AMIs でpylearn2で検索するとすでにpylearn2が入ったAMIが出てくるので、それを使うのもありかもです（僕は試してません）。

僕がAMIを公開してもいいんですが、今のところする予定はありません

# まとめ

そこそこ良い計算環境がさくっとできました、まる。ラーメン食べたい

## 参考

- [インスタンスタイプ - Amazon EC2 (クラウド上の仮想サーバー Amazon Elastic Compute Cloud) | アマゾン ウェブ サービス（AWS 日本語）](http://aws.amazon.com/jp/ec2/instance-types/)
- [Deep Learning in Python with Pylearn2 and Amazon EC2](http://www.kurtsp.com/deep-learning-in-python-with-pylearn2-and-amazon-ec2.html)
- [EC2(g2.2xlarge)でOpenGLを使う方法](http://xanxys.hatenablog.jp/entry/2014/05/17/135932)
