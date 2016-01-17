+++
date = "2016-01-18T00:44:46+09:00"
draft = true
title = "対話環境でPoint Cloud Library (PCL) を使いたい"
tags  = [ "Julia", "PCL"]
+++

遅いですが、新年はじめの記事ということで、あけましておめでとうございます。PCLを対話環境で使いたかったので、お正月の間にPCLのラッパーを作りました。なぜ作ったのか、整理して書いてみようと思います。

## Point Cloud Library (PCL) とは

http://www.pointclouds.org/

## 問題

PCL はboost、Eigenに依存している、かつtemplateを多く使用しているため、PCLを使用したプロジェクトのコンパイル時間は非常に長くなります。twitterで [PCL コンパイル] として検索すると、例えば以下の様なツイートが見つかりますが、完全に同意です。

<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

<blockquote class="twitter-tweet" lang="en"><p lang="ja" dir="ltr">PCLリンクしてるコードのコンパイルに一分半くらいかかる。つらい</p>&mdash; がらえもん(プログラム書く (@garaemon_coder) <a href="https://twitter.com/garaemon_coder/status/632064713816305664">August 14, 2015</a></blockquote>

<blockquote class="twitter-tweet" lang="en"><p lang="ja" dir="ltr">PCLはC++だしコンパイル遅いしで色々めんどくさい</p>&mdash; 動かないで点P (@initial_D_0601) <a href="https://twitter.com/initial_D_0601/status/636013899486105600">August 25, 2015</a></blockquote>

<blockquote class="twitter-tweet" lang="en"><p lang="ja" dir="ltr">PCLを使うプロジェクトのコンパイル時間かかりすぎて辛いわ</p>&mdash; kato tetsuro (@tkato_) <a href="https://twitter.com/tkato_/status/662545461362847744">November 6, 2015</a></blockquote>


boostへの依存関係が必須かどうかについては疑問が残りますが、点群処理ではパフォーマンスが求められることが多いと思われるので、C++で書かれていることは合理的に思います。とはいえ、コンパイル時間が長いのは試行錯誤するにはつらいです。

試行錯誤のサイクルを速く回せるようにすることは僕にとって非常に重要だった & C++で書かなければいけないという制約もなかった（※組み込み用途ではない）ので、僕は動的型付け言語でラッパーを作ることにしました。

## 何で書くか

世の中には色んなプログラミング言語があります。C++ライブラリのラッパー作るぞとなったとき、僕にとって選択肢は、

- Python
- Julia

の二択でした。それぞれ、以下のプロジェクトに頼れば templateを多用したライブラリのラップができそうだと思いました。

- [Cython](http://cython.org/)
- [Cxx.jl](https://github.com/Keno/Cxx.jl)

pythonに関しては、すでに cythonで書かれた [strawlab/python-pcl](https://github.com/strawlab/python-pcl) というラッパーがあります。しかし、

- 現在あまりメンテされていない
- サポートされている機能も多くはない
- templateを多用したライブラリのラップをcythonで十分にできるかどうか自信がなかった [^1]
- juliaは関数や型がパラメータを持てるため、templateを多用したライブラリのラップが簡単にできそうだと思った（i.e. `pcl::PointCloud<T>` は `PointCloud{T}` と書ける[^2]）

[^1]: 公式にサポートはされていますが、過去にcythonではまったことがあるので、懐疑的

[^2]: cythonでも同じようにかけますが、pythonだと`PointCloud(dtype=T)`みたいに書くことになるんですかね

といった理由から、Juliaで書くことにしました。

## 成果物

https://github.com/r9y9/PCL.jl

[StatisticalOutlierRemovalのデモ | nbviewer](http://nbviewer.jupyter.org/gist/r9y9/6ed9a1d0b46993d374f5) こんな感じで、jupyter上で試行錯誤できるようになりましたとさ[^3]。[strawlab/python-pcl](https://github.com/strawlab/python-pcl) よりも多くのことができると思います。

[^3]: PCLVisualizerはGUIで使った方が便利なので、JuliaのREPLから使うことが多いですが

PCLは非常に大きなライブラリのため、全ての機能をラップするつもりはありませんが、今後必要に応じて機能を追加するかもしれません。

## 適当なスクショ

PCL.jl で、少なくとも最低限以下はできますということで。ソースコードは [r9y9/PCL.jl/examples](https://github.com/r9y9/PCL.jl/tree/master/examples) にあります。

### PCLVisualizer

<div align="center"><img src="/images/milk_cartoon_all_small_clorox.gif" /></div>


### 3D Object Recognition based on Correspondence Grouping

<div align="center"><img src="/images/correspondence_grouping.png" /></div>


### Hypothesis Verification for 3D Object Recognition

<div align="center"><img src="/images/global_hypothesis_verification.png" /></div>

### Extracting indices from a PointCloud

<div align="center"><img src="/images/extract_indices.png" /></div>

### Kinect v2と遊ぶ

<div align="center">
<iframe width="560" height="315" src="https://www.youtube.com/embed/rGdsNoK3n9Q" frameborder="0" allowfullscreen></iframe></div>

画質低い & クロップが適当で一部しか見えませんが、fpsは15くらいでしょうか。real-timeで点群を処理するようなアプリケーションを書く場合は、現実的にはC++で書くことになるかと思います。

## 雑記

以下、僕のmacbook proで `tic(); using PCL; toc()` をした結果：


```jl
julia> tic(); using PCL; toc()
INFO: vtk include directory found: /usr/local/include/vtk-6.3
INFO: Loading Cxx.jl...
INFO: dlopen...
INFO: vtk version: 6.3.0
INFO: Including headers from system path: /usr/local/include
INFO: pcl_version: 1.8
INFO: Include pcl top-level headers
  1.053026 seconds (91 allocations: 4.266 KB)
INFO: Include pcl::common headers
  5.433219 seconds (91 allocations: 4.078 KB)
INFO: adding vtk and visualization module headers
INFO: Include pcl::io headers
  0.389614 seconds (195 allocations: 11.034 KB)
INFO: Include pcl::registration headers
  1.428106 seconds (195 allocations: 11.065 KB)
INFO: Include pcl::recognition headers
  1.154518 seconds (136 allocations: 6.141 KB)
INFO: Include pcl::features headers
  0.033937 seconds (181 allocations: 8.094 KB)
INFO: Include pcl::filters headers
  0.070545 seconds (316 allocations: 14.125 KB)
INFO: Include pcl::kdtree headers
  0.022809 seconds (91 allocations: 4.078 KB)
INFO: Include pcl::sample_consensus headers
  0.014600 seconds (91 allocations: 4.141 KB)
INFO: Include pcl::segmentation headers
  0.010710 seconds (46 allocations: 2.094 KB)
INFO: FLANN version: 1.8.4
elapsed time: 39.194405845 seconds
39.194405845
```

[r9y9/PCL.jl/src/PCL.jl#L86-L101](https://github.com/r9y9/PCL.jl/blob/9760565dd3b744e16733c54992551e4e0babc7ee/src/PCL.jl#L86-L101) pcl/pcl_base.h. pcl/common/common_headers.h 当たりのパースに大分時間かかってるなあ、、。まぁ一度ロードしてしまえば、juliaのプロセスをkillしないかぎり問題ないのですが。開発中は、頻繁にreloadする必要があって、辛かったです。

ロード時間が長い問題は、Cxx.jlにプリコンパイル（[Keno/Cxx.jl/issues/181](https://github.com/Keno/Cxx.jl/issues/181)）がサポートされれば、改善するかもしれません。


## さいごに

PCLを対話環境で使えるようになりました。快適です。また今回のラッピングを通して、[Cxx.jl](https://github.com/Keno/Cxx.jl) でできないことはほぼないという所感を持ちました。C++ の対話環境（REPL）も付いているので、最強すぎますね。Cythonでもできるぞってことであれば、教えて下さい。僕もpythonから使えるのであれば使いたいです（でも面倒過ぎる気がするので手を出せない）。

僕にとって快適な環境はできましたが、[Cxx.jl](ttps://github.com/Keno/Cxx.jl) のビルドはかなり面倒なので（Juliaの開発版も必要ですし…）、きっと誰も使わないんだろうなー、、、
