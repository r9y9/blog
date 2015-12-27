---
layout: post
title: "Bloggerカスタマイズメモ"
date: 2013-07-27
comments: true
categories: blogger
---

## まとめ
とりあえず、行ったのは以下の通り。変更の度にこの投稿に追加するかも

- [Mathjaxの導入](http://r9y9.github.io/blog/2013/08/03/mathjax-blogger/)
- syntax highlighterの導入
- google-code-prettyyの導入
- CSSの修正
- ソーシャルリンクの追加

## Mathjax

別記事にまとめた→ [Mathjaxを使ってBloggerで数式を書く](http://r9y9.github.io/blog/2013/08/03/mathjax-blogger/)

## Syntax Highlighter

結局syntax highlighterを使うことにした（2013/08/03）。
google-code-prettyだとデフォに不満が若干あるし、カスタマイズしててもめんどくさかったので。
デフォで綺麗なのがいい

### 導入方法

http://www.way2blogging.org/widget-generators/syntax-highlighter-scripts-generator

ここでgenerateされたコードを埋め込むだけ。

### 使い方

```html
<pre class="brush: html">
   write html code here
</pre>
```

### カスタマイズ

http://8bitsize.blogspot.jp/2012/10/syntax-highlighter-config.html

ここを参考に、toolbarを表示しないようにした。

`SyntaxHighlighter.defaults['toolbar'] = false;`

とgenerateされたスクリプトに追加するだけ

## google-code-pretty

結局syntax highlighterを使うことにした（2013/08/03）。
google-code-prettyだとデフォに不満が若干あるし、カスタマイズしててもめんどくさかったので。

### 導入方法

以下のリンクから、add to bloggerボタンを押すと一瞬で導入できる

http://www.kuribo.info/2008/04/code-prettify.html

## CSS

cssの修正は、とりあえず最低限以下のようにした。
全体のフォントをよさげな奴に指定
タイトルのフォントやらをよさげな奴に指定
headingのフォーマット変更

気に入らないところはその都度調整すると思うので、gistで管理することにする。
https://gist.github.com/r9y9/6094627

## ソーシャルリンク

### Follow me ボタン

http://www.go2web20.net/twitterFollowBadge/
ここで作って、html/javascriptガジェットにコードを貼り付けるだけ。

### いいねボタン

あとで付けたい


継ぎ足し継ぎ足しカスタマイズしていく
