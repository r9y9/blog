+++
date = "2017-12-21T00:00:00+09:00"
draft = false
title = "Interactive C++: Jupyter上で対話的にC++を使う方法の紹介 [Jupyter Advent Calendar 2017]"
tags  = ["Jupyter", "C++", "Julia", "cling"]
categories = ["C++", "Jupyter", "Julia"]
+++

![](/images/jupyter-cxx/jupyter-cxx-demo.gif)

[Jupyter Advent Calendar 2017](https://qiita.com/advent-calendar/2017/jupyter) 21日目の記事です。

C++をJupyterで使う方法はいくつかあります。この記事では、僕が試したことのある以下の4つの方法について、比較しつつ紹介したいと思います。

1. [root/cling](https://github.com/root-project/cling) 付属のカーネル
2. [root/root](https://github.com/root-project/cling) 付属のカーネル
3. [xeus-cling](https://github.com/QuantStack/xeus-cling)
4. [Keno/Cxx.jl](https://github.com/Keno/Cxx.jl) をIJuliaで使う

まとめとして、簡単に特徴などを表にまとめておきますので、選ぶ際の参考にしてください。詳細な説明は後に続きます。

|                  | [cling](https://github.com/root-project/cling)                                | [ROOT](https://github.com/root-project/root)                                                | [xeus-cling](https://github.com/QuantStack/xeus-cling)                                                                    | [Cxx.jl]((https://github.com/Keno/Cxx.jl)) + [IJulia](https://github.com/JuliaLang/IJulia.jl) |
|------------------|--------------------------------------|-----------------------------------------------------|--------------------------------------------------------------------------------|-----------------|
|C++インタプリタ実装 | C++ | C++ | C++ | Julia + C++ |
| (Tab) Code completion | ○                                    | ○                                                   | ○                                                                              | x               |
| Cインタプリタ    | △[^1]                                    | △                                                   | △                                                                    | ○               |
| %magics    | x                                    | %%cpp, %%jsroot, その他                                           | x                                                                    | △[^6]              |
| 他言語との連携   | x                                    | Python, R [^3]                                              | x                                                                              | Julia           |
| バイナリ配布     | [公式リンク](https://root.cern.ch/download/cling/) | [公式リンク](https://root.cern.ch/downloading-root) (python2系向け）                                  | condaで提供                     |         △[^2]        |
| オンラインデモ   | x                                    | [rootdemo](https://swanserver.web.cern.ch/swanserver/rootdemo/) | [binderリンク](https://mybinder.org/v2/gh/QuantStack/xeus-cling/0.0.7-binder?filepath=notebooks%2Fxcpp.ipynb) |x      |

[^1]: clangをベースにしているので原理的には可能だと思いますが、少なくともjupyterカーネルとしてはありません
[^2]: linux向け
[^3]: [公式ホームページ](https://root.cern.ch/) より引用: It is mainly written in C++ but integrated with other languages such as Python and R.
[^6]: Juliaのmacroを使えばよい、というスタンスで、提供していません。 [参考リンク](https://github.com/JuliaLang/IJulia.jl/blob/42d103eaa89d8cf1ab3bc0a8ee0e298bb9a91f80/src/magics.jl#L1)


**共通事項**

すべて、clang/llvmをC++インタプリタのベースにしています。Cxx.jl以外は、C++インタプリタであるclingをベースに、さらにその上にjupyterカーネルを実装しています。

## 1. cling

clingは、いわずとしれた（？）C++インタプリタ実装です。後述するROOTという data analysis framework の一部として、CERNによって開発されています。(20年くらい前の) 古くからあったCINTというC++インタプリタ実装が、clangを使って書き直された、という歴史があります。clingプロジェクトの一環としてJupyterカーネルが開発されています。

**良いところ**

- clingの起動が速いのでストレスが少ない [^4]

[^4]: Cxx.jlだと、パッケージのコンパイルに10秒かかる、とか過去にありました。最近は改善されていますが

**イマイチなところ**

- IPythonだと使える `%time` のようなマジックはない
- cling本体で良いのでは？感が否めない。cling本体のREPLを使えば、Ctrl+Rによるヒストリ検索も使えるし…

**使ってみた感想まとめ**

個人的には、Jupyterは可視化と組み合わせてこそ良さがあると思っているのもありますが、あえてJupyterで使う必要性を僕は感じませんでした。cling自体はとても素晴らしいのと、ノートブックとして実行結果ごとコードを保存したい、といった目的でjupyterを使う場合には、良いと思いました。

**注意**

`#include <iostream>` のあとにcode completionをしようとするとclingが落ちる、というバグがあります。Jupyterの場合はカーネルがリスタートします。

- https://github.com/vgvassilev/cling/issues/152

**参考リンク**

- 公式web: https://cdn.rawgit.com/root-project/cling/master/www/index.html
- Github: https://github.com/root-project/cling
- 紹介スライド: [LLVM Developers' Meeting, "Creating cling, an interactive interpreter interface for clang", Axel Naumann, Philippe Canal, Paul Russo, Vassil Vassilev, 04.11.2010, San Jose, CA, United States](http://llvm.org/devmtg/2010-11/Naumann-Cling.pdf)

## 2. ROOT

ROOTの説明を公式ページから引用します：

> A modular scientific software framework. It provides all the functionalities needed to deal with big data processing, statistical analysis, visualisation and storage. It is mainly written in C++ but integrated with other languages such as Python and R.

日本語の情報が少ない印象ですが、[ROOT 講習会 2017 | 高エネルギー宇宙物理学のための ROOT 入門 – ROOT for High-Energy Astrophysics (RHEA)](https://github.com/akira-okumura/RHEA/wiki/ROOT-%E8%AC%9B%E7%BF%92%E4%BC%9A-2017) によると、実験系素粒子物理学では標準的なデータ解析ソフトウェア・ライブラリ群のようです。

ROOTプロジェクト自体にclingを含みますが、clingが提供するjupyterカーネルとは別で、[JupyROOT](https://github.com/root-project/root/tree/master/bindings/pyroot/JupyROOT) というカーネルが開発されています。

**良いところ**

- PythonとC++をミックスできる。`%%cpp` magicでC++関数を定義して、ホスト（python) 側から呼び出せる
- `%%jsroot` magic により、グラフをインタラクティブに動かせる
- IPythonで使えるmagicが使える（`%timeit`, `%time`, `%load_ext`等）

**イマイチなところ**

- Numpyやmatplotlibなど、Pythonを用いた数値計算ではデファクトに近いツールとの連携は微妙に思いました [^5]。cythonのように、手軽にnumpy arrayをC++に渡す、といった方法はなさそう・・・？（あったら教えてください）
- ROOTの（でかい）APIを覚えないと使えなさそうで、ハードルが高い
- 公式のbinderのデモノートブック、ちょいちょいカーネルが落ちる…

[^5]: https://github.com/rootpy/rootpy ライブラリはありますが、結局このライブラリのAPIを覚えないといけないという…はい…

**使ってみた感想まとめ**

Jupyterカーネルはclingのものよりも良いと思いました。PythonとC++をミックスできるのが特に良いと思います。個人的には、ROOTが機能もりもりのデカイソフトウェアなことがあまり好きになれず、使い込んでいないのですが、ROOTのAPIに慣れた人、あるいは好きになれる人には、良いと思います。

clingだと `#include <iostream>`のあとにcode completionで落ちる、というバグがありまたが、ROOT付属のcling (`ROOT 6.10/08` をソースからビルドして使いました) ではそのバグはありませんでした。

**参考リンク**

- 公式ページ: https://root.cern.ch/
- Github: https://github.com/root-project/root
- オンラインデモ: https://swanserver.web.cern.ch/swanserver/rootdemo/

## 3. xeus-cling

先月 11月30日に、[Jupyter blog で紹介](https://blog.jupyter.org/interactive-workflows-for-c-with-jupyter-fe9b54227d92) されたカーネルです。名前の通りclingをベースにしています。C++インタプリタとしては機能的にcling付属カーネルと同じですが、[xeus](https://github.com/QuantStack/xeus) というJupyter kernel protocolのC++実装をベースにしている点が異なります。

**良いところ**

- condaでパッケージとして提供されているので、インストールが楽。clang/clingも併せてインストールしてくれます
- 同じ開発元が、[xplot](https://github.com/QuantStack/xplot) という可視化ライブラリを提供している（ただしalphaバージョン）
- 標準ライブラリのヘルプが `?` コマンドで確認できます (例. `?std::vector`)

**イマイチなところ**

- 外部ライブラリをロードしようとしたら動きませんでした（なので [プルリク](https://github.com/QuantStack/xeus-cling/pull/94) 投げました（が、いい方法ではなかったようでcloseされました
- ``%timeit`` の実装があったので試してみましたが、エラーが出て動きませんでした

**使ってみた感想まとめ**

少しalphaバージョンの印象を受けました。xplotなど周辺ツールへの期待がありますが、個人的にはmatplotlib等pythonの可視化ツールでいいのでは…という気持ちになりました。

**参考リンク**

- Github: https://github.com/QuantStack/xeus-cling
- 紹介記事: https://blog.jupyter.org/interactive-workflows-for-c-with-jupyter-fe9b54227d92

## 4. Cxx.jl + IJulia.jl

Cxx.jlは、clangをベースにしたJuliaのC++インタフェースです。JuliaにはIJuliaというJupyterカーネルの実装があるので、IJuliaとCxx.jlを使えば、Jupyter上でC++を使うことができます。過去にCxx.jlに関する記事をいくつか書きましたので、そのリンクを貼っておきます。

- [Cxx.jlを用いてJulia expression/value をC++に埋め込む実験 | LESS IS MORE](/blog/2016/01/24/passing-julia-expressions-to-cxx/)
- [Cxx.jl を使ってみた感想 + OpenCV.jl, Libfreenect2.jl の紹介 | LESS IS MORE](/blog/2015/12/22/cxx-jl/)

**良いところ**

- JuliaとC++をミックスできます。過去記事に書きましたが、例えばC++関数内でJuliaのプログレスバーを使ったりできます
- C++インタプリタとCインタプリタを切り替えられます
- `icxx` と `cxx` マクロで、それぞれローカル/グローバルスコープを切り替えられます。
- Juliaの配列をC++に渡すのは非常に簡単にできます。例を以下に示します

```jl
C++ > #include <iostream>
true

julia> cxx"""
       template <class T>
       void f(T x, int n) {
           for (int i = 0; i < n; ++i) {
               std::cout << x[i] << std::endl;
           }
       }""";

julia> x = rand(5)
10-element Array{Float64,1}:
 0.593086
 0.736548
 0.344246
 0.390799
 0.226175

julia> icxx"f($(pointer(x)), $(length(x)));"
0.593086
0.736548
0.344246
0.390799
0.226175
```

**イマイチなところ**

- Cxxパッケージを読み込むのに多少時間がかかります。僕の環境では（プリコンパイルされた状態で）2.5秒程度でした
- (Tab) Code completionは実装されていません [#61](https://github.com/Keno/Cxx.jl/issues/61)
- `icxx` or `cxx` で囲まないといけず、syntax highlightはされません

**使ってみた感想まとめ**

僕は一年以上Cxx.jlを使っているので、バイアスも入っていると思いますが、かなり使いやすいと思います。パッケージのロードに時間がかかるのは、何度もカーネルやjuliaを再起動したりしなければ、まったく気になりません。[IJuliaの設計上の理由](https://github.com/JuliaLang/IJulia.jl/blob/42d103eaa89d8cf1ab3bc0a8ee0e298bb9a91f80/src/magics.jl#L1) により、magicはありませんが、例えば `%time` は `@time` マクロで十分であり、不便に感じません。

**参考リンク**

- IJulia: https://github.com/JuliaLang/IJulia.jl
- Cxx : https://github.com/Keno/Cxx.jl

## まとめ

- C++と他言語のやりとりのスムースさの観点から、やはり僕は対話環境でC++を使うならCxx.jlが最高だと思いました。Cxx + JuliaのREPLも便利ですが、Cxx + IJuliaも良いと思います。
- ただし、C++単体でしか使わない、ということであれば、cling or xeus-clingが良いと思います。ただし xeus-clingは、前述の通り外部ライブラリを読みこもうとするとエラーになる問題があったので、外部ライブラリを読み込んで使用したい場合はパッチ ([xeus-cling/#94](https://github.com/QuantStack/xeus-cling/pull/94)) を当てた方がよいかもしれません
- xeus-clingには、Jupyterブログにのっていたのでどんなものかと思って試してみましたが、周辺ツール含め思ってたよりalpha版のようでした。また、他と比べての機能的な優位性はあまり感じませんでした。ただし、condaパッケージとして提供されているので、敷居が一番低いのは嬉しいですね
- ROOTのjupyter kernelは、C++とpythonをミックスできるのが特に良く、素晴らしいと思いました。また `%%cpp` magicの他にも、ipythonで使える `%timeit` などのmagicも使えるのは、ユーザにとっては嬉しいです。Cxx.jlを除けば、ROOTのカーネルが一番良いと思いました。

## 参考

- [Interactive Workflows for C++ with Jupyter – Jupyter Blog](https://blog.jupyter.org/interactive-workflows-for-c-with-jupyter-fe9b54227d92)
- [C++11/14/17インタプリタ環境 Jupyter-Cling - Qiita](https://qiita.com/mugwort_rc/items/b8087d1b6f9498b037d5)
- [JupyterにC++のノートのためのclingカーネルを追加する [Mac] - Qiita](https://qiita.com/sasaki77/items/f6253e1d6638fba0e744)
- [高エネルギー宇宙物理学のための ROOT 入門 – ROOT for High-Energy Astrophysics (RHEA)](https://github.com/akira-okumura/RHEA)
