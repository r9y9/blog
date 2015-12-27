---
layout: post
title: Cxx.jl を使ってみた感想 + OpenCV.jl, Libfreenect2.jl の紹介
date: 2015-12-22
comments: true
categories: Julia Julia-Advent-Calendar-2015
---

<div align="center"><img src="/images/opencvjl_demo.jpg "OpenCV.jl based on Cxx.jl"" class="image"></div>

## はじめに

[Julia Advent Calendar 2015](http://qiita.com/advent-calendar/2015/julialang) 22日目の記事です。


Julia の C++ FFI (Foreign Function Interface) である [Cxx.jl](https://github.com/Keno/Cxx.jl) をしばらく使ってみたので、その感想を書きます。加えて、Cxx.jl を使って作った成果物の話も簡単に書こうと思います（冒頭に貼った画像は、OpenCV.jl でテキトーにカメラから画像をキャプチャしてthresholdingしたやつです）。
Cxx.jl の動作原理については、僕の理解が不十分なため簡単にしか紹介できませんが、そもそも使ったことがある人が稀だと思われるので、感想程度でも役に立てば幸いです。

## Cxx.jl とは

https://github.com/Keno/Cxx.jl

簡単に説明すると、Cxx.jl とは、Julia から C++ を使用する（e.g. 関数呼び出し、メソッド呼び出し、メンバ変数へのアクセス、etc) ための機能を提供するパッケージです。C++のライブラリを活用したい、あるいはパフォーマンスがシビアな箇所で一部 C++ 使いたい（Cインタフェースを作りたくない[^1]）、といった場合に便利です。

[^1]: 例えば template を多用している場合、Cインタフェースを作るのは面倒です

Cxx.jl の原理についてざっくりといえば、clang を用いて C++ から LLVM IR を生成し、llvmcall を用いて（Just in time に）コードを実行する、という方式のようです[^2]

[^2]: ※正確に理解していないため、あまり宛てにしないでください）

Cxx.jl の原理について知りたい場合は、Cxx.jl のソースコード（+コメント）を、Cxx.jl を使うと何ができるのか知りたい場合は、Cxx.jl の README を御覧ください。

以下、過去を思い出しながら感想を書いてみます

## 実際に使う前に

### Pkg.build("Cxx") を成功させることが困難

そもそも使いはじめる前に、ビルドすることが困難でした。Cxx.jl を動作させるためには、

- julia
- llvm
- clang
- lldb

の開発版が必要ですが、ビルドが難しい大きな原因は、動作することが保証された**明確な revision が存在しない**ことにあります。（なんじゃそれ、と思うかもしれませんが、まぁまだ安定版はリリースされていないので、、）

今でこそ、llvm, clang, lldbは、Keno氏の fork の kf/gallium ブランチ使えばいいよと README に書いてありますが、僕が使い始めた二ヶ月ほど前は、開発版のllvmが必要だよ、くらいにしか書いていませんでした（参考: [Cxx.jl/README](https://github.com/Keno/Cxx.jl/blob/3897e8720b683fe35e407f2128d14e41cec8e0dd/README.md)）。何度もllvmをビルドし直すのは、本当に苦行でした…

参考：
<blockquote class="twitter-tweet" lang="en"><p lang="ja" dir="ltr">今日だけでllvmをn回ビルドしてる（ビルドできたとは言ってない</p>&mdash; 山本りゅういち (@r9y9) <a href="https://twitter.com/r9y9/status/655000313112367104">October 16, 2015</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

<br>

思考停止の様子：
<blockquote class="twitter-tweet" lang="en"><p lang="en" dir="ltr">make -C deps clean-llvm &amp; make -j4</p>&mdash; 山本りゅういち (@r9y9) <a href="https://twitter.com/r9y9/status/670571501658251264">November 28, 2015</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

<br>

### Cxx.jl のビルドはどうするのが一番簡単なのか

さて、さらっと書きましたが、今では llvm, clang, lldb　のkf/gallium　ブランチを使えば、比較的簡単に、多少の試行錯誤[^3] で Cxx.jl をビルドして使えます。

[^3]: 多少の試行錯誤、というのは、Julia と Cxx.jl のリビジョンは、経験的には必ずしも（特にJuliaの）masterで動作しないので、Julia と Cxx.jl を master から少し遡って、ビルドできるか試行錯誤する、という意味です

### 開発版 llvm と一緒に Julia をビルドする

Juliaをクローンしたディレクトリで、以下の様な `Make.user` ファイルを作成して make します。

```
override LLDB_VER=master
override LLVM_VER=svn
override LLVM_ASSERTIONS=1
override BUILD_LLVM_CLANG=1
override BUILD_LLDB=1
override USE_LLVM_SHLIB=1
override LLDB_DISABLE_PYTHON=1

override LLVM_GIT_URL_LLVM=https://github.com/JuliaLang/llvm.git
override LLVM_GIT_URL_LLDB=https://github.com/JuliaLang/lldb.git
override LLVM_GIT_URL_CLANG=https://github.com/JuliaLang/clang.git
override LLVM_GIT_VER=kf/gallium
override LLVM_GIT_VER_LLDB=kf/gallium
override LLVM_GIT_VER_CLANG=kf/gallium
```

一部、LLVM_ASSERSONS を有効にするなど、必ずしも必須でないものも含まれていますが、こちらが現状の推奨のようです。この設定で、僕はubuntu 14.04, osx 10.10 でビルドが通ることを確認しました[^4]

[^4]: ビルドが通ったことがある、の方が正確ですが

注意：すでに llvm や clang がローカルにクローン済の場合、`deps/srccache` 以下からクローン済みのソースを消してからビルドすることをおすすめします。すでにクローンされていて、upstream  の変更を取り入れたい場合は、

```bash
make -C deps update-llvm
```

とすると便利です。

### Cxx.jl のインストール

```jl
Pkg.clone("https://github.com/Keno/Cxx.jl.git")
Pkg.build("Cxx")   
```

エラーがでなければ、インストール完了[^5]です。

[^5]: なお、現状のJulia masterとCxx.jl masterでは、エラーが出ると踏んでおります、、、


## 実際に使ってみたあと

さて、ようやくビルドもできて、ここからは使ってしばらくしての感想です。

### Julia 上で C++ の syntax がそのまま使える

まず、簡単に Cxx.jl の機能を挙げると、重要なのは


- `cxx"..."`
- `icxx"..."`
- `@cxx`

の三つです。以下、簡単に例をあげると、`cxx"..."` でC++ syntax を評価して：

```cpp
cxx"#include <iostream>"

cxx"""
namespace test {
void f() {
    std::cout << "Hello C++" << std::endl;
}
}
"""
```

`@cxx` マクロで C++ 関数を呼び出す：

```jl
@cxx test::f()  # Hello C++
```

`cxx"..."`はグローバルスコープで評価されますが、`icxx"..."` を使えば、特定のスコープ内で C++ を使用することもできます。

```jl
for i in 1:10
    icxx"""std::cout << $i << std::endl;"""
end
```

`ccall` のように、返り値、引数の型などを指定して実行するのではなく、C++ のsyntax をそのまま使ってコードが書ける、という点にびっくりしました。

### template も使える

```cpp
cxx"""
template <typename T>
T add(T x, T y) { return x + y; }
"""
```

こんな感じで特殊化も可能

```cpp
cxx"""
template <>
int add<int>(int x, int y) { return x + y; }
"""
```

書いてて気付きましたが、README には template について言及されていませんね。僕は、今のところ問題なく使えています。例には出していませんが、template class ももちろん使えます（例. `std::vector<T>`）。


### その他雑記

- Cxx.jl で使える C++ には制約がある（はず）だが、ここ二ヶ月使用した限りでは、大きな制約に出会ってないし、快適
- 共有ライブラリの呼び出しは、`ccall` と違ってライブラリだけでなくヘッダーファイルも必要
- `using Cxx` にはけっこう時間がかかる。僕の環境では約15秒だった
- たまに llvm error を吐いて落ちる。デバッグするには llvm, clang についてある程度知識がないと難しそう
- C++ REPL 便利

という感じですかね。書き進むに連れて適当になってすいません、、、

## Cxx.jl を使って作った成果物

まとめに入る前に、Cxx.jl を使って遊ぶ過程で作った成果物を、簡単なコメント付きで紹介します。

### OpenCV.jl

<div align="center"><img src="/images/video_thresholding.gif "OpenCV.jl demo"" class="image"></div>

https://github.com/r9y9/OpenCV.jl

Cxx.jl の学習の題材として作りました。途中から cv::Mat 周りを真面目に作り始めたので、それなりに使えると思います。

デザインポリシーとして、

- cv::Mat を `AbstractArray{T,N}` の subtype として Julia ライクに使えること
- cv::Mat と Julia の Array の相互変換をサポートすること

を念頭において作りました。

### LibFreenect2.jl

<div align="center"><img src="/images/depth_streaming_example.gif "LibFreenect2.jl demo"" class="image"></div>

https://github.com/r9y9/LibFreenect2.jl

ちょうど仕事で kinect v2 を触っていたので、遊びがてらやってみました。

## まとめ

- Cxx.jl をビルドするのはけっこう面倒ですが、C++を（主観ですが）ほとんど不自由なくJITライクに使えるので、非常に便利です
- 二つほど C++ ライブラリのラッパーを作ってみましたが、簡単にできるので、みなさんもお試しあれ
- レッツ・トライ Cxx.jl！


## おまけ

現在 Julia community では、llvm 3.3 から llvm 3.7.1 に移行しようとする動きがあるので（ref: [julia/issues/9336](https://github.com/JuliaLang/julia/issues/9336), [julia/pull/14430](https://github.com/JuliaLang/julia/pull/14430)）、移行後は、もう少しビルドが楽になるかもしれません。

実は、この記事を読んでも、きっと今は　Cxx.jl をビルドできないんじゃないかなと思うんですが、もしどうしてもビルドしたい、ということであれば、僕のローカルの llvm, clang, lldb, julia の revision を調べて教えるので、言ってください。

### 2015/12/28 追記

[Cxx.jl を動作させるための julia, llvm, clang, lldb のコミットハッシュ | qiita](http://qiita.com/r9y9/items/37633ed37e22612b5224)
