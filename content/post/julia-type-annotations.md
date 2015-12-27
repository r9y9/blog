---
layout: post
title: "Julia: 値と変数に対する Type Annotation の違い"
date: 2015-12-08
comments: true
categories: Julia Julia-Advent-Calendar-2015
---

## はじめに

[Julia Advent Calendar 2015](http://qiita.com/advent-calendar/2015/julialang) 8日目の記事です。

この記事では、値 (value) と変数 (variable) に対する type annotation の違いを、問題とそれに対する解答を用意する形式で説明しようと思います。そんなの知ってるぜ！という方は、問題だけ解いてみて自分の理解度を試してもらえればと思います。

記事に出てくるJuliaコードは、Julia 0.5-dev, 0.4.0 で動作確認しました。

## 問題

新規REPLセッションを開いて、A、B それぞれを実行したときの挙動はどうなるでしょうか？エラーの発生の有無と、エラーが発生しない場合は返り値の値、型を答えてください。

### A

```jl
function f()
    x = (1.0 + 2.0)::Int
    return x
end

f()
```

### B

```jl
function g()
    x::Int = (1.0 + 2.0)
    return x
end

g()
```

なお、一方ではエラーが起き、もう一方はエラー無く実行されます。一見似たような書き方ですが、二つは異なる意味を持ちます。この記事ではそれぞれを解説しようと思います。

この問題の答えがわからなかった方は、この記事を読むと正解がわかるはずなので、続きをご覧ください。下の方に、簡潔な問題の解答とおまけ問題を書いておきました。


## A: 値に対する type annotation

Aの2行目では、値に対して type annotation をしています。これは typeassert とも呼びます。Aで使った type annotation を日本語で説明してみると、「`(1.0 + 2.0)` という式を評価した値は、Int 型であることを保証する」となります。

`(1.0 + 2.0)` を評価した値は `3.0` であり、 Float64の型を持ちます。したがって `Float64 != Int` であるため、

```
ERROR: TypeError: typeassert: expected Int64, got Float64
```

のような typeassert のエラーが吐かれます。

`(1.0 + 2.0)`を評価した値の型は一見して明らかため、実用的な例ではありませんが、例えば関数の返り値の型は一見してわからないことがあるので、例えば以下のような書き方は有用な場合もあると思います。

```jl
x = f(y)::Int
```


## B: 変数に対する type annotation

Bの2行目では、変数に対して type annotation をしています。同じく日本語で説明すると、「`x`という変数に入る値は、Int 型であることを保証する」となります。また、値に対する annotation とは異なり**スコープ**を持ちます。

前述したとおり、`(1.0 + 2.0)` を評価した値は `3.0` であり、Float64の型を持ちます。一方で、`x` は Int型の値を持つ変数として宣言されているため、この場合、Float64型である `(1.0 + 2.0)` を、Int 型に変換するような処理が**暗黙的に**行われます。したがって、変換可能な場合には（B の例がそうです）、エラーは起きません。暗黙的に処理が行われるというのは、知らないと予期せぬバグに遭遇することになるため、気をつける必要があります。

では、変数に対する type annotation はどのような場合に使うかというと、あるスコープの範囲で、代入によって変数の型が変わってしまうのを防ぐために使います。ある変数の型がスコープの範囲で不変というのはコンパイラにとっては嬉しい事で、パフォーマンスの向上に繋がります。Performance tips にもありますね（参考: [Performance tips / Avoid changing the type of a variable](http://docs.julialang.org/en/release-0.4/manual/performance-tips/#avoid-changing-the-type-of-a-variable)）


## 違いまとめ

ここまでの話から、違いをまとめると、以下のようになります。

 Type annotation の種類      | typeassert error　 | 暗黙的な型変換　 | スコープ　
----------------------------|------------------|----------------|----------
 値に対する type annotation   | あり             | なし           | なし
 変数に対する type annotation 　 | なし             | あり           | あり

<br>

## 最後に

type annotation を使うときは、値と変数に対する annotation の違いを意識して、使い分けましょう


## 問題の解答

- A: typeassert に引っかかり、TypeError が吐かれる
- B: Int 型の 3 が返り値として得られる

## おまけ問題


### 1

```jl
function h()
    x::UInt8 = UInt8(0)
    x = Float64(0.0)
    x
end
```

```jl
# なんと表示されるでしょうか？
println(typeof(h()))
```

### 2

```jl
function s()
    x::Int = Float64(0)
    x = UInt8(0)
    x = Float32(0.5)
    x
end
```

```jl
# なんと表示されるでしょうか？
s()
```

解答は、各自REPLで実行して確認してみてください。長々と読んでくださりありがとうございました。

## 参考

- [公式ドキュメント / Type Declarations](http://docs.julialang.org/en/release-0.4/manual/types/?highlight=typeassert#type-declarations)
