---
layout: post
title: "PythonによるニューラルネットのToyコード"
date: 2014-05-11
comments: true
categories: Python, Neural-Networks, Machine-Larning
---

1000番煎じだけど、知り合いにニューラルネットを教えていて、その過程で書いたコード。わかりやすさ重視。

このために、誤差伝播法をn回導出しました（意訳：何回もメモなくしました）

```python
#!/usr/bin/python
# coding: utf-8

# ニューラルネットワーク(Feed-Forward Neural Networks)の学習、認識の
# デモコードです。
# 誤差伝搬法によってニューラルネットを学習します。
# XORの学習、テストの簡単なデモコードもついています
# 2014/05/10 Ryuichi Yamamoto

import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def dsigmoid(y):
    return y * (1.0 - y)

class NeuralNet:
    def __init__(self, num_input, num_hidden, num_output):
        """
        パラメータの初期化
        """
        # 入力層から隠れ層への重み行列
        self.W1 = np.random.uniform(-1.0, 1.0, (num_input, num_hidden))
        self.hidden_bias = np.ones(num_hidden, dtype=float)
        # 隠れ層から出力層への重み行列
        self.W2 = np.random.uniform(-1.0, 1.0, (num_hidden, num_output))
        self.output_bias = np.ones(num_output, dtype=float)

    def forward(self, x):
        """
        前向き伝搬の計算
        """
        h = sigmoid(np.dot(self.W1.T, x) + self.hidden_bias)
        return sigmoid(np.dot(self.W2.T, h) + self.output_bias)

    def cost(self, data, target):
        """
        最小化したい誤差関数
        """
        N = data.shape[0]
        E = 0.0
        for i in range(N):
            y, t = self.forward(data[i]), target[i]
            E += np.sum((y - t) * (y - t))
        return 0.5 * E / float(N)

    def train(self, data, target, epoches=30000, learning_rate=0.1,\
              monitor_period=None):
        """
        Stochastic Gradient Decent (SGD) による学習
        """
        for epoch in range(epoches):
            # 学習データから1サンプルをランダムに選ぶ
            index = np.random.randint(0, data.shape[0])
            x, t = data[index], target[index]

            # 入力から出力まで前向きに信号を伝搬
            h = sigmoid(np.dot(self.W1.T, x) + self.hidden_bias)
            y = sigmoid(np.dot(self.W2.T, h) + self.output_bias)

            # 隠れ層->出力層の重みの修正量を計算
            output_delta = (y - t) * dsigmoid(y)
            grad_W2 = np.dot(np.atleast_2d(h).T, np.atleast_2d(output_delta))

            # 隠れ層->出力層の重みを更新
            self.W2 -= learning_rate * grad_W2
            self.output_bias -= learning_rate * output_delta

            # 入力層->隠れ層の重みの修正量を計算
            hidden_delta = np.dot(self.W2, output_delta) * dsigmoid(h)
            grad_W1 = np.dot(np.atleast_2d(x).T, np.atleast_2d(hidden_delta))
            
            # 入力層->隠れ層の重みを更新
            self.W1 -= learning_rate * grad_W1
            self.hidden_bias -= learning_rate * hidden_delta

            # 現在の目的関数の値を出力
            if monitor_period != None and epoch % monitor_period == 0:
                print "Epoch %d, Cost %f" % (epoch, self.cost(data, target))

        print "Training finished."

    def predict(self, x):
        """
        出力層の最も反応するニューロンの番号を返します
        """
        return np.argmax(self.forward(x))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Specify options")
    parser.add_argument("--epoches", dest="epoches", type=int, required=True)
    parser.add_argument("--learning_rate", dest="learning_rate",\
                        type=float, default=0.1)
    parser.add_argument("--hidden", dest="hidden", type=int, default=20)
    args = parser.parse_args()

    nn = NeuralNet(2, args.hidden, 1)

    data = np.array([[0, 0], [0 ,1], [1, 0], [1, 1]])
    target = np.array([0, 1, 1, 0])

    nn.train(data, target, args.epoches, args.learning_rate,\
             monitor_period=1000)

    for x in data:
        print "%s : predicted %s" % (x, nn.forward(x))
```

```python
#!/usr/bin/python
# coding: utf-8

# MNISTを用いたニューラルネットによる手書き数字認識のデモコードです
# 学習方法やパラメータによりますが、だいたい 90 ~ 97% くらいの精度出ます。
# 使い方は、コードを読むか、
# python mnist_net.py -h
# としてください
# 参考までに、
# python mnist_net.py --epoches 50000 --learning_rate 0.1 --hidden 100
# とすると、テストセットに対して、93.2%の正解率です
# 僕の環境では、学習、認識合わせて（だいたい）5分くらいかかりました。
# 2014/05/10 Ryuichi Yamamoto

import numpy as np
from sklearn.externals import joblib
import cPickle
import gzip
import os

# 作成したニューラルネットのパッケージ
import net

def load_mnist_dataset(dataset):
    """
    MNISTのデータセットをダウンロードします
    """
    # Download the MNIST dataset if it is not present
    data_dir, data_file = os.path.split(dataset)
    if (not os.path.isfile(dataset)) and data_file == 'mnist.pkl.gz':
        import urllib
        origin = 'http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz'
        print 'Downloading data from %s' % origin
        urllib.urlretrieve(origin, dataset)

    f = gzip.open(dataset, 'rb')
    train_set, valid_set, test_set = cPickle.load(f)
    f.close()

    return train_set, valid_set, test_set

def augument_labels(labels, order):
    """
    1次元のラベルデータを、ラベルの種類数(order)次元に拡張します
    """
    new_labels = []
    for i in range(labels.shape[0]):
        v = np.zeros(order)
        v[labels[i]] = 1
        new_labels.append(v)
    
    return np.array(new_labels).reshape((labels.shape[0], order))        

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MNIST手書き数字認識のデモ")
    parser.add_argument("--epoches", dest="epoches", type=int, required=True)
    parser.add_argument("--learning_rate", dest="learning_rate",\
                        type=float, default=0.1)
    parser.add_argument("--hidden", dest="hidden", type=int, default=100)
    args = parser.parse_args()

    train_set, valid_set, test_set = load_mnist_dataset("mnist.pkl.gz")
    n_labels = 10 # 0,1,2,3,4,5,6,7,9
    n_features = 28*28

    # モデルを新しく作る
    nn = net.NeuralNet(n_features, args.hidden, n_labels)

    # モデルを読み込む
    # nn = joblib.load("./nn_mnist.pkl")

    nn.train(train_set[0], augument_labels(train_set[1], n_labels),\
             args.epoches, args.learning_rate, monitor_period=2000)

    ## テスト
    test_data, labels = test_set
    results = np.arange(len(test_data), dtype=np.int)
    for n in range(len(test_data)):
        results[n] = nn.predict(test_data[n])
        # print "%d : predicted %s, expected %s" % (n, results[n], labels[n])
    print "recognition rate: ", (results == labels).mean()
    
    # モデルを保存
    model_filename = "nn_mnist.pkl"
    joblib.dump(nn, model_filename, compress=9)
    print "The model parameters are dumped to " + model_filename
```

https://github.com/r9y9/python-neural-net-toy-codes

以下のようなコマンドを叩いて、正解率が97%くらいになるまで学習してから入力層から隠れ層への重みを可視化してみた

```bash
# python mnist_net.py --epoches 50000 --learning_rate 0.1 --hidden 100 # epochesは適当に
```

<div align="center"><img src="/images/nn_mnist_W1_100.png "Input to Hidden weight filters after traingned on MNIST."" class="image"></div>

興味深いことに、RBMと違って重み行列の解釈はしにくい。生成モデルの尤度を最大化することと、誤差を最小化することはこんなにも違うんだなぁというこなみな感想

RBMについては、以下へ

[Restricted Boltzmann Machines with MNIST - LESS IS MORE](http://r9y9.github.io/blog/2014/03/06/restricted-boltzmann-machines-mnist/)

おわり
