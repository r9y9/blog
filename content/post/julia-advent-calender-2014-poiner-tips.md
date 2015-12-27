---
layout: post
title: ccallにおけるポインタ周りのハマりどころとその解決法
date: 2014-12-09
comments: true
categories: julia
---

[Julia Advent Calendar 2014](http://qiita.com/advent-calendar/2014/julialang) 9日目の記事です。

## はじめに

CやFortranの関数をJuliaから呼ぶために使用する`ccall`において、ポインタに関係するハマりどころとその解決法を紹介します。純粋なJuliaを使っている場合にはポインタを意識することはめったにないと思うので、`ccall` を使う人（計算が重いボトルネック部分をCで書いてJuliaから呼びたい人、Cのライブラリのラッパーを書きたい/書いてる人）を主な読者と想定して記事を書きました（限定的でごめんなさい）。

困った時は、公式ドキュメントの [Calling C and Fortran Code](http://docs.julialang.org/en/latest/manual/calling-c-and-fortran-code/) を参考にしましょう。

**注意**: 最新版の公式ドキュメントをいくつか引用していますが、ドキュメントは日々更新されていますので、この記事を読んで頂いた時点とは異なる可能性があることにご注意ください。

## こんなとき

`ccall` を使う際に、ポインタに関する以下のような疑問を持つことがあります。

- ポインタを引数に持つ（例. `double*`）関数のラッピングはどうすればいいのか？
- 構造体のポインタを引数に持つ関数のラッピングはどうすれば？
- ポインタのポインタを引数に持つ（例. `double**`）関数のラッピングは？

一つ目は非常に簡単で、`Array`（Cの関数が`double*`を取るならば`Array{Float64,1}`）をそのまま渡せばよいだけです。ドキュメントの[Array Conversions](http://docs.julialang.org/en/latest/manual/calling-c-and-fortran-code/#array-conversions)にも書かれています。が、残りの二つに関してはハマりどころがあります。順に説明します。

## 構造体のポインタを引数に持つ関数のラッピングはどうすれば？

現状のドキュメントは少し不親切なので、引用した上で、整理します。

[Calling C and Fortran Code](http://docs.julialang.org/en/latest/manual/calling-c-and-fortran-code/) より引用:
> Currently, it is not possible to pass structs and other non-primitive types from Julia to C libraries. However, C functions that generate and use opaque struct types by passing pointers to them can return such values to Julia as Ptr{Void}, which can then be passed to other C functions as Ptr{Void}. Memory allocation and deallocation of such objects must be handled by calls to the appropriate cleanup routines in the libraries being used, just like in any C program.

冒頭に it is not possible とあります。が、決して不可能なわけではありません。上記文章の要点をまとめると、

- opaqueな構造体はCからJuliaへポインタとして渡すことができる
- そのポインタは `Ptr{Void}` としてCの関数に渡すことができる

と書かれています。つまり、一般には構造体は渡せないけどポインタ渡しはできるよ、ということです。

じゃあnon-opaqueな構造体についてはどうなんだ？Juliaの型を渡せないのか？という疑問が出てきます。結論からいえば、non-opaqueな構造体についてもポインタ渡しは可能です。つまり、Cの構造体に相当するimmutableな型[^1]をjuliaで宣言してあげれば、juliaの型をCに渡すことが可能です（値渡しはできません）

[^1]: immutableでなければいけない理由はまだよくわかっていないのですが、少なくとも [#8948](https://github.com/JuliaLang/julia/pull/8948) にはそう書いてあります


例を示します。

### Cコード

```c
typedef struct {
   double a;
   int b;
} Foo;

# 構造体のポインタを引数にとる関数1
void print(Foo* foo) {
    printf("a=%lf\n", foo->a);
    printf("b=%d\n", foo->b);
}

# 構造体のポインタを引数にとる関数2
void reset(Foo* foo) {
    foo->a = 0.0;
    foo->b = 0;
}
```

### Juliaコード

```julia
# Cの構造体 Foo に相当する型を宣言します
immutable Foo
    a::Float64
    b::Int32 # cのintはjuliaのInt32に対応します
end

foo = Foo(10.0, 2)

# Cの関数に、ポインタとしてJuliaの型を渡すことができます
ccall(:print, "libfoo", Void, (Ptr{Foo},), &foo)

# ポインタで渡す場合、Cで変更した結果はJuliaにも反映されます
ccall(:reset, "libfoo", Void, (Ptr{Foo},), &foo)

# foo(0.0, 0) と表示される
println(foo)
```

ちなみにJuliaからCへ値渡しをしてもエラーにならないので、お気をつけください（ハマりました）。

公式ドキュメントは不親切と言いましたが、 プルリクエスト [update documentation for passing struct pointers to C #8948](https://github.com/JuliaLang/julia/pull/8948)（まだマージはされていない）で改善されているので、もしかするとこの記事が読まれる頃には改善されているかもしれません。

また、値渡しを可能にしようとする動きもあります（[RFC: Make struct passing work properly #3466](https://github.com/JuliaLang/julia/pull/3466), [WIP: types as C-structs #2818](https://github.com/JuliaLang/julia/pull/2818) マージ待ち）。

### 構造体渡しのまとめ

- Cの構造体に相当するJuliaの型を定義して、ポインタで渡せばOK
- 値渡しは現状できない
- ポインタを受けることはできる（Ptr{Void}として受ける）

## ポインタのポインタを引数に持つ（例. `double**`）関数のラッピングは？

さて、これはドキュメントにまったく書かれておらず、かつハマりやすいと僕は思っています。例を交えつつ解説します。以下のような関数のラッピングを考えます。

```c
void fooo(double** input, int w, int h, double** output);
```

`input`は入力の行列、`output`は計算結果が格納される行列、行列のサイズは共に 列数`w`、行数`h` だと思ってください。Juliaからは `input::Array{Float64,2}` を入力として、`output::Array{Float64,2}` を得たいとします。

`double*`を引数にとる場合は`Array{Float64,1}`を渡せばよかったのに対して、`double**`を引数に取る関数に `Array{Float64,2}`や`Array{Array{Float64,1},1}`を単純に渡すだけでは、残念ながらコンパイルエラーになります。はい、すでに若干面倒ですね。。さて、どうすればいいかですが、

- どんな型で渡せばいいか
- どのように型を変換するか
- 変換した型をどのように元に戻すか

という三点に分けて説明します。

### 1. どんな型で渡せばいいか

`Array{Ptr{Float64}}` で渡せばよいです。外側のArrayは、`ccall` がポインタに変換してくれるので、Juliaの型でいえば`Ptr{Ptr{Float64}}`、Cの型で言えば`double**`になるわけです。

### 2. どのように型を変換するか

ここがハマりどころです。今回の例では、`Array{Float64,2}` を `Array{Ptr{Float64},1}` に変換すればよいので、例えば以下のような実装が思いつきます。

```julia
# Array{T,2} -> Array{Ptr{T}}
function ptrarray2d{T<:Real}(src::Array{T,2})
    dst = Array{Ptr{T}, size(src, 2))
    for i=1:size(src, 2)
        dst[i] = pointer(src[:,i], 1) # 先頭要素のポインタを取り出す
    end
    dst
end
```

実はこの実装はバグを含んでいます。バグがあるとしたら一行しか該当する部分はないですが、

```julia
dst[i] = pointer(src[:,i], 1)
```

ここが間違っています。何が間違っているかというと、`pointer(src[:,i], 1)`は一見`src`の`i`列目の先頭要素のポインタを指しているような気がしますが、`src[:,1]`で `getindex`という関数が走って内部データのコピーを行っているので、そのコピーに対するポインタを指している（元データの`i`列目のポインタを指していない）点が間違っています[^2]。これは、JuliaのArray実装ついて多少知らないとわからないと思うので、ハマりどころと書きました。

[^2]: たちの悪いことに、この実装でもだいたい上手く動くんですよね…。数値型がimmutableだからコピーしてもそうそうアドレスが変わらないとかそういう理由だろうかと考えていますが、ちょっとよくわかっていないです

Array `A`に対する syntax `X = A[I_1, I_2, ..., I_n]` は `X = getindex(A, I_1, I_2, ..., I_n)` と等価です。詳細は、[Multi-dimensional Arrays](http://docs.julialang.org/en/latest/manual/arrays/)や[標準ライブラリのドキュメント](http://docs.julialang.org/en/latest/stdlib/base/?highlight=getindex#Base.getindex) を参考にしてください

さて、正解を示します。

```julia
# Array{T,2} -> Array{Ptr{T}}
function ptrarray2d{T<:Real}(src::Array{T,2})
    dst = Array{Ptr{T}, size(src, 2))
    for i=1:size(src, 2)
         dst[i] = pointer(sub(src, 1:size(src,1), i), 1)
    end
    dst
end
```

違いは `SubArray`を使うようになった点です。`SubArray`は、indexingを行うときにコピーを作らないので、期待した通りに`i`列目の先頭要素のポインタを取得することができます。`SubArray`について、以下引用しておきます[^3]。

[^3]: ArrayとSubArrayの使い分けはどうすればいいのか、それぞれどういう目的で作られたのか等、僕も勉強中で理解が曖昧なため説明できません、すみません。

> SubArray is a specialization of AbstractArray that performs indexing by reference rather than by copying. A SubArray is created with the sub() function, which is called the same way as getindex() (with an array and a series of index arguments). The result of sub() looks the same as the result of getindex(), except the data is left in place. sub() stores the input index vectors in a SubArray object, which can later be used to index the original array indirectly.

引用元: [Multi-dimensional Arrays](http://docs.julialang.org/en/latest/manual/arrays/#implementation)

### 3. 変換した型をどのように元に戻すか

Juliaで計算結果（上の例でいう `double** output`）を受け取りたい場合、ポインタに変換した値をJuliaのArrayに戻す必要があります（必ずしもそうではないですが、まぁほぼそうでしょう）。つまり、`Array(Ptr{Float64},1)`を`Array{Float64,2}`したいわけです。幸いにも、これは`pointer_to_array`を使うと簡単にできます。コードを以下に示します。

```julia
# ccallを実行した後の計算結果が coutput に格納されているとします
coutput::Array{Ptr{Float64},1}

# Cに渡した型 Array{Ptr{Float64},1} から Array{Float64,2}に変換
for i=1:length(coutput)
    output[:,i] = pointer_to_array(coutput[i], size(output, 1))
end
```

`pointer_to_array` は、その名前の通りの関数ですね。pointerをArrayに変換してくれます。

### 1, 2, 3 をまとめる

最後に、1, 2, 3の内容をまとめて、ポインタのポインタを引数にもつ関数のラッパー例を書いておきます。

```julia
function fooo(input::Array{Float64,2})
    h, w = size(intput)
    output = Array(Float64, h, w)
    
    # C関数に渡す用の変数
    cinput::Array{Ptr{Float64}} = ptrarray2d(input)
    coutput::Array{Ptr{Float64}} = ptrarray2d(output)
    
    ccall(:fooo, "libfooo", Void,
    		 (Ptr{Ptr{Float64}}, Int, Int, Ptr{Ptr{Float64}}), 
    		 cinput, w, h, coutput)

    # coutputをJuliaのArrayに変換
    for i=1:length(coutput)
        output[i,:] = pointer_to_array(coutput[i], h)
    end

    output
end
```

### ポインタのポインタまとめ

- `Array`のindexingはコピーを作るのである要素のポインタがほしい時は注意
- 行/列の先頭のポインタがほしいときは `SubArray` を使いましょう


## おわりに

ポインタにまつわるハマりどころとその解決法を紹介しました。今回紹介したものはすべて [WORLD.jl](https://github.com/r9y9/WORLD.jl) という [音声分析変換合成システムWORLD](http://ml.cs.yamanashi.ac.jp/world/) のラッパーを書いていたときに得た知見です。やっと`WORLD.jl`が安定して動くようになってきて公式パッケージにしようかなぁと考えているところですので、興味のある方はぜひ触ってみてください。
