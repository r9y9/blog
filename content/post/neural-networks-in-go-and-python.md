---
layout: post
title: Goでニューラルネットいくつか書いたけどやっぱPythonが楽でいいですね
date: 2014-07-29
comments: true
categories: go python machine-learning 
---

いまいち成果出ないので気分転換にブログをだらだら書いてみるテストです。

## まえがき

半年くらい前に、某深層学習に興味を持ってやってみようかなーと思っていた時期があって、その時にGoでいくつかニューラルネットを書きました（参考：[Restricted Boltzmann Machines with MNIST - LESS IS MORE](http://r9y9.github.io/blog/2014/03/06/restricted-boltzmann-machines-mnist/)、[githubに上げたコード](https://github.com/r9y9/nnet)）。なぜGoだったかというと、僕がGoに興味を持ち始めていたからというのが大きいです。Goを知る前は、たくさん計算するようなコードを書くときはC++だったけれど、C++は色々つらいものがあるし、GoはC++には速度面で劣るもののそこそこ速く、かつスクリプト的な書きやすさもあります。C++のデバッグやメンテに費やす膨大な時間に比べれば、計算時間が1.5~2倍に増えるくらい気にしないというスタンスで、僕はC++のかわりGoを使おうとしていました（※今でも間違っているとは思いませんが、とはいえ、厳しいパフォーマンスを求められる場合や既存の資産を有効活用したい場合など、必要な場面ではC++を書いています）。

## Goで機械学習

僕は機械学習がけっこう好きなので、Goでコード書くかーと思っていたのですが、結果としてまったく捗りませんでした。ニューラルネットをてきとーに書いたくらいです。

検索するとわかりますが、現状、他の主流な言語に比べて圧倒的に数値計算のライブラリが少ないです。特に、線形代数、行列演算のデファクト的なライブラリがないのはつらいです。いくつか代表的なものをあげます。

- [skelterjohn/go.matrix](https://github.com/skelterjohn/go.matrix) - もうまったくメンテされていないし、たぶんするつもりはないと思います。使い勝手は、僕にとってはそんなに悪くなかった（試しに[NMF](https://gist.github.com/r9y9/9030922)を書いてみた）ですが、実装は純粋なGoで書かれていて、GPUを使って計算するのが流行りな時代では、例えば大きなニューラルネットをパラメータを変えながら何度も学習するのにはしんどいと思いました。
- [gonum/matrix](https://github.com/gonum/matrix) - 比較的最近出てきたライブラリで、[biogo](https://code.google.com/p/biogo/) から行列演算に関する部分を切り出して作られたもののようです。行列演算の内部でblasを使っていて、かつ将来的にはcublasにも対応したい、みたいな投稿をGoogle Groupsで見たのもあって、半年くらい前にはgoで行列演算を行うならこのライブラリを使うべきだと判断しました（以前けっこう調べました：[gonum/matrix のデザインコンセプトに関するメモ - Qiita](http://qiita.com/r9y9/items/7f93a89e3a88bb4ed263)）。しかし、それほど頻繁にアップデートされていませんし、機能もまだ少ないです。

自分で作るかー、という考えも生まれなかったことはないですが、端的に言えばそれを行うだけのやる気がありませんでした。まぁ本当に必要だったら多少難しくてもやるのですが、ほら、僕達にはpythonがあるじゃないですか…

## Pythonで機械学習

[python 機械学習 - Google 検索](https://www.google.co.jp/search?q=python+%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92&oq=python+%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92) 約 119,000 件（2014/07/29現在）

もうみんなやってますよね。

[Golang 機械学習 - Google 検索](https://www.google.co.jp/search?q=Golang+%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92&oq=Golang+%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92) 約 9,130 件（2014/07/29現在）

いつかpythonのように増えるんでしょうか。正直に言って、わかりません（正確には、あんま考えていませんごめんなさい）

さて、僕もよくpython使います。機械学習のコードを書くときは、だいたいpythonを使うようになりました（昔はC++で書いていました）。なぜかって、numpy, scipyのおかげで、とても簡潔に、かつ上手く書けばそこそこ速く書けるからです。加えて、ライブラリがとても豊富なんですよね、機械学習にかかわらず。numpy, scipyに加えて、matplotlibという優秀な描画ライブラリがあるのが、僕がpythonを使う大きな理由になっています。

pythonの機械学習ライブラリは、[scikit-learn](http://scikit-learn.org/stable/) が特に有名でしょうか。僕もちょいちょい使います。使っていて最近おどろいたのは、scipy.mixtureには通常のGMMだけでなく変分GMM、無限混合GMMも入っていることですよね。自分で実装しようとしたら、たぶんとても大変です。昔変分GMMの更新式を導出したことがありますが、何度も心が折れそうになりました。いやー、いい時代になったもんですよ…（遠い目

## Pythonでニューラルネット（pylearn2を使おう）

Deep何とかを含め流行りのニューラルネットが使える機械学習のライブラリでは、僕は [pylearn2](https://github.com/lisa-lab/pylearn2) がよさ気だなーと思っています。理由は、高速かつ拡張性が高いからです。pylearn2は、数学的な記号表現からGPUコード（GPUがなければCPU向けのコード）を生成するmathコンパイラ [Theano](https://github.com/Theano/Theano) で書かれているためpythonでありながら高速で、かつ機械学習に置いて重要なコンポーネントであるデータ、モデル、アルゴリズムが上手く分離されて設計されているのがいいところかなと思います（全部ごっちゃに書いていませんか？僕はそうですごめんなさい。データはともかくモデルと学習を上手く切り分けるの難しい）。A Machine Learning library based on Theanoとのことですが、Deep learningで有名な [lisa lab](http://lisa.iro.umontreal.ca/index_en.html) 発ということもあり、ニューラルネットのライブラリという印象が少し強いですね。

一つ重要なこととして、このライブラリはかなり研究者向けです。ブラックボックスとして使うのではなく、中身を読んで必要に応じて自分で拡張を書きたい人に向いているかと思います。

[Ian J. Goodfellow, David Warde-Farley, Pascal Lamblin, Vincent Dumoulin, Mehdi Mirza, Razvan Pascanu, James Bergstra, Frédéric Bastien, and Yoshua Bengio. “Pylearn2: a machine learning research library”. arXiv preprint arXiv:1308.4214](http://arxiv.org/pdf/1308.4214v1.pdf)

↑の論文のIntroductionの部分に、その旨は明記されています。と、論文のリンクを貼っておいてなんですが、[Ian Goodfellow](http://www-etud.iro.umontreal.ca/~goodfeli/) のホームページにもっと簡潔に書いてありました。以下、引用します。

> I wrote most of Pylearn2, a python library designed to make machine learning research convenient. Its mission is to provide a toolbox of interchangeable parts that provide a lot of flexibility for setting up machine learning experiments, providing enough extensibility that pretty much any research idea is feasible within the context of the library. This is in contrast to other machine learning libraries such as scikits-learn that are designed to be black boxes that just work. Think of pylearn2 as user friendly for machine learning researchers and scikits-learn as user friendly for developers that want to apply machine learning.

pylearn2では、Multi-layer Perceptron (MLP)、Deep Bolztmann Machines (DBM)、新しいものでMaxout Network等、手軽に試すことができます（まぁゆうて計算はめっちゃ時間かかるけど）。先述の通りmathコンパイラの [Theano](https://github.com/Theano/Theano) を使って実装されているので、GPUがある場合はGPUを使って計算してくれます。環境構築に関しては、今はAWSという便利なサービスがあるので、GPUを持っていなくてもウェブ上でポチポチしてるだけで簡単にGPU環境を構築できます（参考：[Pylearn2, theanoをEC2 g2.x2large で動かす方法 - LESS IS MORE](http://r9y9.github.io/blog/2014/07/20/pylearn2-on-ec2-g2-2xlarge/)）。本当にいい時代になったものですね（二回目

pylearn2、コードやドキュメント、活発なgithubでの開発、議論を見ていて、素晴らしいなーと思いました（まだ使い始めたばかりの僕の意見にあまり信憑性はないのですが…）。僕もこれくらい汎用性、拡張性のあるコードを書きたい人生でした…（自分の書いたニューラルネットのコードを見ながら）

## Pylearn2は遅いって？

本当に速さを求めるなら [cuda-convnet2](https://code.google.com/p/cuda-convnet2/) や [Cafee](http://caffe.berkeleyvision.org/)、もしくは直でcudaのAPIをだな…と言いたいところですが、確かにpylearn2は他の深層学習のライブラリに比べて遅いようです。最近、Convolutional Neural Network (CNN) に関するベンチマークがGithubで公開されていました。

[soumith/convnet-benchmarks](https://github.com/soumith/convnet-benchmarks)

現時点でまだ work in progressと書いてありますが、参考になると思います。優劣の問題ではなく、必要に応じて使い分ければいいと僕は思っています。

さてさて、本当はここから僕が書いたGoのニューラルネットのコードがいかにクソかという話を書こうかと思ったのですが、長くなったのでまた今度にします。

## まとめ

- Goでニューラルネットとか機械学習をやるのは現状しんどいし（[golearn](https://github.com/sjwhitworth/golearn)とかあるけど、まだまだearly stage）、おとなしくpython使うのが無難
- pythonはやっぱり楽。ライブラリ豊富だし。ニューラルネットならpylearn2がおすすめ。ただし自分で拡張まで書きたい人向けです。

散々pythonいいよゆうてますが、どちらかといえば僕はGoの方が好きです。機械学習には現状pythonを使うのがいいんじゃないかなーと思って、Goでニューラルネットを書いていた時を思い出しながらつらつらと書いてみました。

おわり。
