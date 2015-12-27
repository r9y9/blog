---
layout: post
title: "Bashでコマンドの存在チェック"
date: 2013-08-12
comments: true
categories: shell-script
---

素晴らしいまとめ→ [コマンドの存在チェックはwhichよりhashの方が良いかも→いやtypeが最強 - qiita](http://qiita.com/kawaz/items/1b61ee2dd4d1acc7cc94)

いつもwhichを使っていたのだけど、typeの方がよさげ。

今までこう書いてた

```bash
if [ -x which "何かコマンド" ]
then
    コマンドが存在した場合の処理
fi
```

コマンドが実行可能かどうかをwhichを使って判定する。少なくとも自分のubuntu 12.04では期待した通りに動く。だた環境によっては、指定したコマンドがない場合に、

`
/usr/bin/which: no hogehoge
`

みたいに表示されて、おそらくwhichが実行可能なバイナリだから、if文がtrueで通っちゃうことがある。これは困る。で、ググってたらtypeやhashがあることを知って、typeが良さそうということで試したら期待通りの動作になったのでハッピー。bash組み込みらしいね

## 書き方

```
if type "コマンド" > /dev/null 2>&1
then
    コマンドが存在した場合の処理
fi
```

bash組み込みのコマンドを使って存在判定するので、速いらしい（割りとどうでもいいけど）。標準エラー出力は意外とうっとしいということがわかったので、今回書いてたスクリプトでは捨てるようにした。

これからはtype使おう。［］も書かなくても済むしコードもすっきりする
