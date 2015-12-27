---
layout: post
title: "Mathjaxを使ってBloggerで数式を書く"
date: 2013-08-03
comments: true
categories: mathjax blogger
---

Bloggerカスタマイズメモから、Mathjaxの部分を切り出して補足。ちょっとカスタマイズして書くことも増えたので。bloggerでの作業記録だけど、wordpressでもoctopressでもだいたい一緒

## Mathjax

Latex形式の数式をレンダリングしてくれるエンジン。レンダリングに少し時間がかかるけど、それでも数式は綺麗だし画像じゃないから普通にコピーできるし、個人的にオススメ

### 使い方

```latex
\begin{align}
\sum_{i=1}^{n}i = \frac{1}{2}n(n+1)
\end{align}
```

と書くと、以下のように表示される

<div>
\begin{align}
\sum_{i=1}^{n}i = \frac{1}{2}n(n+1)
\end{align}
</div>

他にもLaTeXの記法はまぁだいたい使えると思う。$$でインラインで書いてももちろんおｋ

### 導入方法

bloggerのレイアウト編集画面で、html/javascriptのガジェットを追加して、そこにmathjaxを使うためのスクリプトを書くだけ。もしくは、htmlを編集して、`<head></head>`の中に直接書く。
以下をコピペすればおｋ．

```html
<script src="http://cdn.mathjax.org/mathjax/latest/MathJax.js" type="text/javascript">    
    MathJax.Hub.Config({
        HTML: ["input/TeX","output/HTML-CSS"],
        TeX: {
               Macros: {
                        bm: ["\\boldsymbol{#1}", 1],
                        argmax: ["\\mathop{\\rm arg\\,max}\\limits"],
                        argmin: ["\\mathop{\\rm arg\\,min}\\limits"]},
               extensions: ["AMSmath.js","AMSsymbols.js"],
               equationNumbers: { autoNumber: "AMS" } },
        extensions: ["tex2jax.js"],
        jax: ["input/TeX","output/HTML-CSS"],
        tex2jax: { inlineMath: [ ['$','$'], ["\\(","\\)"] ],
                   displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
                   processEscapes: true },
        "HTML-CSS": { availableFonts: ["TeX"],
                      linebreaks: { automatic: true } }
    });
</script>
```

これでlatexの文法で数式が書ける。らくちん。wordpressとかでももちろん使える


### マクロの追加

基本的にはここ→ [MathJax in Blogger (II)](http://irrep.blogspot.jp/2011/07/mathjax-in-blogger-ii.html) に書いてあるとおりにやったけど、デフォではargmaxとかargminが使えないので、マクロを追加した。

Mathjaxを呼び出すスクリプトに、以下のような感じで追加（正確には上のスクリプト参考）

```javascript
bm: ["\\boldsymbol{#1}", 1]
argmax: ["\\mathop{\\rm arg\\,max}\\limits"]
argmin: ["\\mathop{\\rm arg\\,min}\\limits"]
```

bmはおまけ。これで以下のような数式が書ける。

```latex
\begin{align}
y = \argmax_y p(y|x)
\end{align}
```

次のように表示される

<div>
\begin{align}
y = \argmax_y p(y|x)
\end{align}
</div>

マクロ参考: http://d.hatena.ne.jp/a_bicky/20130216/1361098344


数式綺麗でイイネ！重いけどね
