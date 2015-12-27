---
layout: post
title: "apt-getでコマンドがインストールできるか確認する方法"
date: 2013-08-12
comments: true
categories: package-management
---

apt-cacheを使えばいい、なんてことは誰でも知ってると思うけど、apt-cache search ってすると、コマンド名だけじゃなくコマンドの説明文も一緒に検索されてしまって、都合が悪い場合がある。

そんな時には以下のようにする。

`
apt-cache search --names-only ^emacs24$
`

これで、指定したコマンドがインストールできるかを確認できる。

### ポイント1

`--names-only` オプションを付ける。これで名前のみから検索してくれる。


###  ポイント2

正規表現を使う。これで柔軟性の高い検索ができる。

以上。

ちなみにyumだともうちょっとめんどくさい。yum listかyum searchを使えば似たようなことができる。yum listは、名前のみ検索、yum searchは名前と説明文を検索。

どうでもいいけどyum使いづらい。apt-get最高
