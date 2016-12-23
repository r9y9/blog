+++
date = "2016-12-23T18:06:08+09:00"
draft = false
title = "Juliaをソースからビルドする"
tags  = ["Julia"]
categories = ["Julia"]
+++

[Julia advent calendar 2016](http://qiita.com/advent-calendar/2016/julialang) 23日目の記事です。

## はじめに

Juilaを最も簡単にインストールする方法は、[公式のダウンロードページ](http://julialang.org/downloads/)からバイナリ or インストーラを使用することだと思います。多くの人は、処理系をソースからビルドして使用することはめったにないと思いますが[^1]、自分好みにビルドをカスタマイズしてJuliaを使いたいというコアな方向けに、僕がよく使うビルド時のオプションや便利そうなオプション、ビルド時のTipsなどを紹介しようと思います。

僕がソースからビルドすることになった主な理由は、ソースからビルドしないと使えないパッケージがあったからです[^2]。

[^1]: 大変ですよね
[^2]: https://github.com/Keno/Cxx.jl です

## 下準備

```bash
git clone https://github.com/JuliaLang/julia && cd julia
```

## ビルドのカスタマイズ方法

Juliaのビルドシステムでは、Make.userというファイルで、ユーザがいくらかカスタマイズすることを許可しています。プロジェクトトップにMake.userを作成し、そこに `override LLVM_VER=3.7.1` のような書き方で記述することで、カスタマイズ可能です（詳細は[公式の説明](https://github.com/JuliaLang/julia#source-download-and-compilation)をご覧ください）。例えば僕の場合、主な開発環境であるmacOSではMake.userを以下のように記述しています（項目の説明は後ほどします）。

```
override LLVM_VER=3.7.1
override LLVM_ASSERTIONS=1
override BUILD_LLVM_CLANG=1
override USE_LLVM_SHLIB=1
```

あとは、通常通りmakeコマンドを走らせることで、ビルドを行います。

```bash
make -j4
```

コア数は適当に指定します。llvm, openblasあたりのビルドが結構重いので、並列ビルドがオススメです。

## 僕がよく使うオプション

ここから、僕がよく使うオプションをいくつか解説します。

### LLVM_VER

llvmのバージョンを表します。Julia上でC++を使いたいというcrazyな人に激推しの [Keno/Cxx.jl](https://github.com/Keno/Cxx.jl) というパッケージがあるのですが、このパッケージはclangとllvmの3.7.1以上を必要とします（Cxx.jlについては、過去に何度か記事を書いたので、例えば [Cxx.jlを用いてJulia expression/value をC++に埋め込む実験](http://r9y9.github.io/blog/2016/01/24/passing-julia-expressions-to-cxx/) をご覧ください）。llvm 3.3がデフォルトだったJulia v0.4時代では、明示的に3.7.1と指定する必要がありました。いまは、

- Julia v0.5の公式配布バイナリでも、`Pkg.add("Cxx")`でインストールできるとされている（[Keno/Cxx.jl/#287](https://github.com/Keno/Cxx.jl/issues/287)）
- かつ現状のデフォルトバージョンが3.7.1 (もうすぐ3.9.1になりそうですが [JuliaLang/julia/#19768](https://github.com/JuliaLang/julia/pull/19678/files))

なので、僕の場合は明示的にLLVM_VERを指定する必要はなくなってきましたが、例えば、LLVMのNVPTX backendを使ってJuliaでCUDAカーネルを書けるようにする [JuliaGPU/CUDAnative.jl](https://github.com/JuliaGPU/CUDAnative.jl) （要 llvm 3.9）のような、experimentalなパッケージを試したい場合など、LLVM_VERを指定したくなる場合もあるかと思います。

### LLVM_ASSERTIONS

LLVMをassert付きでビルドするかどうかを表します。ONにするとビルドかかる時間が長くなり、LLVMのパフォーマンスが若干落ちますが、デバッグには便利です。Juliaのコード生成周りでエラーを起こしやすいようなコードを書くときには、ONにしておくと便利です。

### BUILD_LLVM_CLANG

llvmとあわせて、clangをビルドするかどうか、というオプションです。Cxx.jlに必要なので、僕はそのためにONにしています。その他必要なケースとしては、clangのaddress/memory sanitizerを使いたい場合が考えられます。詳細は[devdocs/sanitizers](http://docs.julialang.org/en/stable/devdocs/sanitizers/) をご覧ください。

## CC, CXX

コンパイラの指定です。僕の場合 ubuntu 14.04では、（Cxx.jlのために）以下のように設定しています。

```
override CC=gcc-6
override CXX=g++-6
```

参考: https://github.com/r9y9/julia-cxx

macOS では特に設定していませんが、Julia以外のプロジェクトをビルドするときに、たまに

```
CXX=usr/local/bin/clang++ cmake ${path_to_project}
```

のように、xcode付属のclangではなく、自前でビルドしたclangを使いたい場合などに、CC, CXXを指定したりします。

### USE_CLANG

clangを使ってビルドするかどうかを表します。gccを使いたくない、というときにオンにします。

### USE_LLVM_SHLIB

llvmを共有ライブラリとしてビルドするかどうかを表します。v0.4ではデフォルトがオフで、v0.5からはオンになっています。llvmの共有ライブラリをdlopenして色々いじりたい場合（何度もアレですが、Cxx.jlを使いたい場合とか）は、オンにする必要があります。

### USE\_SYSTEM\_${LIB_NAME}

Juliaでは、デフォルトで依存ライブラリをソースからビルドします。システムにインストールされたライブラリを使用したい場合、USE_SYSTEM_XXX （e.g. `USE_SYSTEM_BLAS`）をオンにします。ビルド時間を短縮することが可能です。

USE_SYSTEM_xxx にどのようなものがあるのかは、[Make.inc](https://github.com/JuliaLang/julia/blob/d8ecebe1a47fd401ef63a80250c096a21843a82d/Make.inc#L25-L47) をご覧ください。

## 便利そうなオプション

### USE_INTEL_MKL

MKLを使うかどうかを表します。MKLを持っている場合にオンにすれば、一部パフォーマンスが向上しそうですね。

### USE_GPL_LIBS

GPLのライブラリ（FFTWなど）を使用するかどうかを表します。使ったことはありませんが、Juliaを組み込みで使用したい場合に、便利かもしれません。

## ビルド時のTips

Juliaは依存関係が多く、cloneした直後の状態からのビルドには一時間以上かかることもあります[^3]。また、masterを追いかけている場合は、途中でビルドにこけてしまうことも珍しくありません。個人的な経験で言えば、

[^3]: 環境によります

- llvm
- openblas
- libgit2
- mbettls
- libunwind

あたりの依存関係のビルドで、何度も失敗しています。僕がソースビルドをし始めたころ、よく調べずに `make clean && make` をして、案の定駄目で、よくわからずに `make distcleannall` してしまうこともありました（`distcleanall`が必要なケースは稀であり、そうでない場合は非常に時間を無駄にします）[^4]。過去の失敗から、僕が学んできたTipsを紹介します。

[^4]: 僕があほなだけの可能性が大いにあります

### プロジェクトトップMakefileのcleanコマンドを適切に使い分ける

cleanコマンドにはさまざまなものがあります。ビルドのし直しが不要なものまでcleanして、無駄に時間を消費しないように、正しく使い分けましょう。以下、基本的なcleanコマンドを簡単にまとめます。

| コマンド     | 説明                            |
|--------------|---------------------------------|
| clean        | Julia本体のclean                |
| cleanall     | Julia本体、flisp、libuvのclean |
| distclean    | binary配布用の成果物をclean     |
| distcleanall | deps以下の依存関係をすべてclean           |

よほどのことがない限り、 `make distcleanall` を使わないようにしましょう。`make distclean` はほとんど使う必要はないと思います。

コマンドの詳細、その他コマンドについては、[julia/Makefile](https://github.com/JuliaLang/julia/blob/d8ecebe1a47fd401ef63a80250c096a21843a82d/Makefile) をご覧ください

### サブディレクトリのMakefileを使いわける

- **deps**: 依存関係
- **src**: コンパイラ (C, C++, flisp)
- **base**: 標準ライブラリ (Julia)
- **doc**: ドキュメント

など（一部です）、Makefileは復数のサブディレクトリにわかれています。依存関係のビルドに失敗した場合には、depsディレクトリ以下のMakefileが使えます。

depsディレクトリ以下、依存関係のcleanコマンドには、大きく以下の二種類があります。

| コマンド     | 説明                            |
|--------------|---------------------------------|
| clean-xxx        | xxx の clean                |
| distclean-xxx     | xxx の clean と `rm -rf ビルドディレクトリ`|

例えばlibgit2のバージョンが変わってエラーが出たからといって、すべてをビルドし直す必要は基本的にはありません。まずは、

```
make -C deps clean-libgit2 && make
```

としてビルドし直し、それでも駄目な場合は、

```
make -C deps distclean-libgit2 && make
```

といった具合に、軽いcleanコマンドから順に試しましょう。

## まとめ

- Make.user をプロジェクトトップに配置することで、ビルドをカスタマイズできます
- ビルドに失敗したとき、良く考えずに `make distcleanall` するのをやめましょう（自戒
- サブディレクトリの Makefile を使い分けて、rebuildは最小限にしましょう
