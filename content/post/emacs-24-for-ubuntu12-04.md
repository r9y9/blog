---
layout: post
title: "emacs24をUbuntu12.04 にインストールする方法"
date: 2013-08-11
comments: true
categories: emacs
---

## コマンド

```bash
sudo add-apt-repository ppa:cassou/emacs
sudo apt-get update
sudo apt-get install emacs24
```

ググればすぐ解決するんだけど、過去何回も調べててアホみたいなので自分でもスクリプト書いたよ。といってもレポジトリ追加してapt-getするだけだけど。

https://github.com/r9y9/install/blob/master/install_emacs.sh

emacsがサーバに入ってないとしにたみることが判明したので、もうサーバにもemacs入れておくようにしたい。

ちなみに24以降だと、パッケージ管理システムがデフォでちゃんとしてたり、color-themeがデフォであったりするので、24以降の方がいい


## 参考

[emacs24 - Ubuntu的日常](http://d.hatena.ne.jp/going-around/20130120/1358693301)
