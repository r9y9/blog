+++
date = "2016-01-24T22:32:08+09:00"
draft = false
title = "Cxx.jlを用いてJulia expression/value をC++に埋め込む実験"
tags  = [ "Julia"]
categories = ["Julia"]
+++

Keno氏によるJuliaCon 2015 の発表 [Keno Fischer: Shaving the Yak](https://www.youtube.com/watch?v=OB8BclL_Tmo) でタイトルの内容が一部紹介されていて、便利そうだなと思い、色々試してみました。

<div align="center">
<iframe width="560" height="315" src="https://www.youtube.com/embed/OB8BclL_Tmo" frameborder="0" allowfullscreen></iframe>
</div>
<br/>

発表の内容は大まかに、Keno氏がなぜ[Cxx.jl](https://github.com/Keno/Cxx.jl)を作ったのか、なぜJuliaを始めたのか、といったモチベーションの話から、Cxx.jlでできることについてlive programmingを交えての紹介、といった話になっています。50分とけっこう長いですが、面白いので興味のある方はどうぞ。この記事は、上の動画を見たあと、Cxx.jlと戯れた結果をまとめたものです。

以下、この記事の目次です。

- 前置き：C++をJulia上で使う
- **本編：JuliaのexpressionやvalueをC++に埋め込む**

 前置きが若干長いので、タイトルの内容が知りたい方は、飛ばして下さい。

## 前置き：C++をJulia上で使う

Cxx.jlを使えば、C++をJulia上で非常にスムーズに扱えうことができます。例えば、C++の`std::vector<T>`を使いたい、さらにはJuliaの`filter`関数を`std::vector<T>`に対して使えるようにしたい、といった場合は、以下に示すように、ほんのすこしのコードを書くだけでできます。


準備：

```
using Cxx
import CxxStd: StdVector
```

`filter`関数：

```jl
function Base.filter{T}(f, v::StdVector{T})
    r = icxx"std::vector<$T>();"
    for i in 0:length(v)-1
        if f(T(v[i]))
            push!(r, v[i])
        end
    end
    r
end
```

なお、`filter`関数に出てくる、`length`, `getindex`, `push!` は、Cxx..jlにそれぞれ以下のように定義されています。

```jl
Base.getindex(it::StdVector,i) = icxx"($(it))[$i];"
Base.length(it::StdVector) = icxx"$(it).size();"
Base.push!(v::StdVector,i) = icxx"$v.push_back($i);"
```

計算結果を見やすくするために、`show` 関数も定義しておきます。

```
function Base.show{T}(io::IO, v::StdVector{T})
    println(io, "$(length(v))-element StdVector{$T}:")
    for i = 0:length(v)-1
        println(io, T(v[i]))
    end
end
```

実行結果：

```jlcon
julia> v = icxx"std::vector<double>{1,2,3,4,5,6,7,8,9,10};"
10-element StdVector{Float64}:
1.0
2.0
3.0
4.0
5.0
6.0
7.0
8.0
9.0
10.0

julia> filter(x -> x > 5, v)
5-element StdVector{Float64}:
6.0
7.0
8.0
9.0
10.0
```

簡単にできました。とても強力です。

さて、以降本編に入りたいと思いますが、Julia上でC++を使うのは簡単かつ、Cxx.jlの主な用途だとは思うのですが（少なくとも自分がそうでした）、逆はどうなのでしょうか？実は、limitationはあるものの、かなり面白いことができます。

## JuliaのexpressionやvalueをC++に埋め込む

まず簡単に、基本的な使い方を整理します。

### valueを埋める

`$(some_value)` という書き方をします

```jlcon

julia> cxx"""
       int getRandom() {
           return $(rand(1:10));
       }
       """
true
julia> @cxx getRandom()
2
julia> @cxx getRandom()
2
julia> @cxx getRandom()
2
```

rand関数を評価したvalueを埋め込んでいるので、何度`getRandom`を呼び出しても結果は同じになります。

### expressionを埋める

`$:(some_expression)` という書き方をします。

```jlcon
julia> cxx"""
       int getReallyRandom() {
           return $:(rand(1:10));
       }
       """
true
julia> @cxx getReallyRandom()
1
julia> @cxx getReallyRandom()
9
julia> @cxx getReallyRandom()
2
```

期待した通りの動作になっていますね。

## 発展例

さて、以下、もう少し発展的な例です。

### C++ expressionの中にJuila expressionを埋めて、さらにその中にC++ expressionを埋める (1)

言葉にするとややこしいですが、例を見ればすぐにわかると思います。

```jlcon
julia> cxx"""
       void test4(int N) {
           for (int i = 0; i < N; ++i) {
               $:(println(icxx"return i;"); nothing);
           }
       }
       """
true

julia> @cxx test4(10)
0
1
2
3
4
5
6
7
8
9
```

簡単に説明すると、C++のfor分の中で、Juliaのprintln関数を読んでいて、さらにprintlnの引数に、C++ expressionが渡されています。`icxx"return i;"`という部分が重要で、これは C++ lambda`[&](){return i;)}` に相当しています。中々キモい表記ですが、こんなこともできるようです。

### C++ expressionの中にJuila expressionを埋めて、さらにその中にC++ expressionを埋める (2)

もう少し実用的な例です。C++関数の中で、Juliaのプログレスバーを使ってみます。

```jlcon
julia> using ProgressMeter
```

```jlcon
julia> cxx"""
       #include <iostream>
       #include <cmath>

       double FooBar(size_t N) {
           double result = 0.0;
           $:(global progress_meter = Progress(icxx"return N;", 1); nothing);
           for (size_t i = 0; i < N; ++i) {
               result = log(1+i) + log(2+i);
               $:(next!(progress_meter); nothing);
           }
           return result;
       }
       """
true

julia> @cxx FooBar(100000000)
Progress: 100% Time: 0:00:18
36.84136149790473
```

プログレスバーについては、[Juliaでプログレスバーの表示をする | qiitq](http://qiita.com/bicycle1885/items/6c7cd3d853e00ddfc250) を参考にどうぞ。このコードもなかなかきもいですが、期待した通りに、プログレスバーが表示されます。

さて、この例からは、Cxx.jlの（現在の）limitationが垣間見えるのですが、

- Juliaのexpressionで定義したローカル変数は、C++的には同じ関数スコープであっても、Julia expressionからはアクセス不可（上記例では、`progress_meter`をglobalにしないと、for文内のjulia expressionからは`progress_meter` にアクセスできません）
- 随所にある`nothing`にお気づきの人もいると思うのですが、C++ expression内のJulia expressionにさらにC++ expressionを埋め込む場合（※そういったexpressionのことを、**nested expressions** と呼ぶんだと思います）、返り値は`Void`型しか受け付けられません（`nothing` をJulia expressionの末尾に置くことで、Julia expressionの返り値を`Void`にしています）

後者について、簡単に例をあげておきます。

#### ネストしていないからOK

```jlcon
julia> cxx"""
       int getRandom2() {
           int r = $:(rand(1:10));
           return r;
       }
       """
true

julia> @cxx getRandom2()
2
```

### ネストしているからダメ

```jlcon

julia> cxx"""
       int getRandom3(int hi) {
           int r = $:(rand(1:icxx"return hi;"));
           return r;
       }
       """
In file included from :1:
__cxxjl_10.cpp:2:9: error: cannot initialize a variable of type 'int' with an rvalue of type 'void'
    int r = __julia::call2([&](){ return hi; });
        ^   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ERROR: Currently only `Void` is supported for nested expressions
 in InstantiateSpecializations at /Users/ryuyamamoto/.julia/v0.5/Cxx/src/cxxstr.jl:268
 [inlined code] from /Users/ryuyamamoto/.julia/v0.5/Cxx/src/cxxstr.jl:723
 in anonymous at /Users/ryuyamamoto/.julia/v0.5/Cxx/src/cxxstr.jl:759
 in eval at ./boot.jl:265
 ```

 nested expressionsで、返り値が`Void`以外も取れるようになると、嬉しいなーと思います。

### C++ lambda に Julia expressionを埋める

これは現在、間接的にしかできませんでした。以下に例をあげます。

```jlcon
ulia> for f in ["iostream", "thread"] cxxinclude(f) end

julia> cxx"""
       int getRandom() { return $:(rand(1:10)); }
       """
true

julia> th = icxx"""
           std::thread([]{
               for (size_t i = 0; i < 10; ++i) {
                   std::cout << getRandom() << std::endl;
               }
            });
       """
6
10
5
6
5
3
7
2
6
9
(class std::__1::thread) {
}

julia> @cxx th->join()
```

threadである必要はない例ですが、lambdaの例ということで。間接的にというのは、一度Julia関数をC++関数に埋め込んで、そのC++関数をlambdaの中で呼び出す、という意味です。

以下のようにJulia expressionを直接埋めようとすると、assertion failureで落ちるてしまうので、注意

```jlcon
julia> th = icxx"""
           std::thread([]{
               for (size_t i = 0; i < 10; ++i) {
                   std::cout << $:(rand(1:10)) << std::endl;
               }
            });
       """

In file included from :1:
:4:36: error: variable '__juliavar1' cannot be implicitly captured in a lambda with no capture-default specified
            std::cout << jl_apply0(__juliavar1) << std::endl;
                                   ^
:1:1: note: '__juliavar1' declared here
^
:2:17: note: lambda expression begins here
    std::thread([]{
                ^
Assertion failed: (V && "DeclRefExpr not entered in LocalDeclMap?"), function EmitDeclRefLValue, file /Users/ryuyamamoto/julia/deps/srccache/llvm-3.7.1/tools/clang/lib/CodeGen/CGExpr.cpp, line 2000.
zsh: abort      julia-master
```

例はこれで以上です。

## まとめ

C++にJuliaを埋め込むといったことは今までほとんどしなかったのですが、今回色々試してみて、いくつかlimitationはあるものの非常に強力だと思いました。興味のある人は、C++にJuliaを埋め込む例は、[Keno/Gallium.jl](https://github.com/Keno/Gallium.jl) にいくつか見つかるので、参考になるかもしれません。

Keno氏の発表、とてもおもしろかったです。先週半ば頃、午前2時半くらいから見始めたのですが、面白くて一気に見てしまいました。いまllvm/clangについて勉強しているので、limitationの部分は、できれば自分でも解決可能かどうか、挑戦してみたいなと思っています。おしまい

## 参考

- Cxx.jlの著者 [Keno](https://github.com/Keno)
- [Cxx.jl](https://github.com/Keno/Cxx.jl)
- [Keno Fischer: Shaving the Yak](https://www.youtube.com/watch?v=OB8BclL_Tmo)
