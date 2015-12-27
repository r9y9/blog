---
layout: post
title: NMFで音源分離を試してみる
date: 2014-10-19
comments: true
categories: machine-learning matrix-factorization
---

ずーーっと前に、 [NMFアルゴリズムの導出（ユークリッド距離版） - LESS IS MORE](http://r9y9.github.io/blog/2013/07/27/nmf-euclid/) で実際に実装してみてやってみると書いていたのに、まったくやっていなかったことに気づいたのでやりました。

音楽に対してやってみたのですが、簡単な曲だったら、まぁぼちぼち期待通りに動いたかなぁという印象です。コードとノートを挙げたので、興味のある方はどうぞ。

## Github

https://github.com/r9y9/julia-nmf-ss-toy

## ノート

[NMF-based Music Source Separation Demo.ipynb | nbviewer](http://nbviewer.ipython.org/github/r9y9/julia-nmf-ss-toy/blob/master/NMF-based%20Music%20Source%20Separation%20Demo.ipynb)

## NMFのコード (Julia)

NMFの実装の部分だけ抜き出しておきます。
```julia
function nmf_euc(Y::AbstractMatrix, K::Int=4;
                        maxiter::Int=100)
    H = rand(size(Y, 1), K)
    U = rand(K, size(Y, 2))
    const ϵ = 1.0e-21
    for i=1:maxiter
        H = H .* (Y*U') ./ (H*U*U' + ϵ)
        U = U .* (H'*Y) ./ (H'*H*U + ϵ)
        U = U ./ maximum(U)
    end
    return H, U
end
```

いやー簡単ですねー。[NMFアルゴリズムの導出（ユークリッド距離版） - LESS IS MORE](http://r9y9.github.io/blog/2013/07/27/nmf-euclid/) で導出した更新式ほぼそのままになってます（異なる点としては、ゼロ除算回避をしているのと、Uをイテレーション毎に正規化していることくらい）。

B3, B4くらいの人にとっては参考になるかもしれないと思ってあげてみた。

おわり
