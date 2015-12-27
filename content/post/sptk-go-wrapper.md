---
layout: post
title: Goで音声信号処理をしたいのでSPTKのGoラッパーを書く
date: 2014-02-10
comments: true
categories: Go Speech-Signal-Processing
---

2014/07/22 追記：  
パッケージの一部として書きました（[GOSSP - Go言語で音声信号処理 - LESS IS MORE](http://r9y9.github.io/blog/2014/06/08/gossp-speech-signal-processing-for-go/)を参照）。
SPTKのラップも含め、いくつかGoで信号処理アルゴリズムを実装したので、お求めの方はどうぞ

-- 

Goが最近オススメです（n度目

Goで音声信号処理をしたいけど、全部一から書くのは大変だし、既存の資産は出来るだけ再利用したい。というわけで、C言語製の[SPTK](http://sp-tk.sourceforge.net/) をGoから使えるようにする


## cgo

GoにはC言語のライブラリを使うには、cgoというパッケージを使えばできる。使い方は、公式のページ等を見るといいと思う http://golang.org/cmd/cgo/

Cの関数や変数などには、 `C.` でアクセスできる

## ラッパー

例えば以下のように書く。MFCCの計算を例に上げる。必要に応じで`SPTK.h`に定義されている関数をラップする

```go
package sptk

// #cgo pkg-config: SPTK
// #include <stdio.h>
// #include <SPTK/SPTK.h>
import "C"

func MFCC(audioBuffer []float64, sampleRate int, alpha, eps float64, wlng, flng, m, n, ceplift int, dftmode, usehamming bool) []float64 {
	// Convert go bool to C.Boolean (so annoying..
	var dftmodeInGo, usehammingInGo C.Boolean
	if dftmode {
		dftmodeInGo = 1
	} else {
		dftmodeInGo = 0
	}
	if usehamming {
		usehammingInGo = 1
	} else {
		usehammingInGo = 0
	}

	resultBuffer := make([]float64, m)
	C.mfcc((*_Ctype_double)(&audioBuffer[0]), (*_Ctype_double)(&resultBuffer[0]), C.double(sampleRate), C.double(alpha), C.double(eps), C.int(wlng), C.int(flng), C.int(m), C.int(n), C.int(ceplift), dftmodeInGo, usehammingInGo)
	return resultBuffer
}
```

このパッケージを使う前に、 https://github.com/r9y9/SPTK を使ってSPTKをインストールする。本家のを使ってもいいですが、その場合は #cgo の設定が変わると思います。公式のSPTK、pkg-configに対応してくれんかな…

最初は、LDFLAGS つけ忘れてて、symbol not foundってなってつらまった。次回から気をつけよう

SPTKの、特に（メル）ケプストラム分析当たりは本当に難しいので、論文読んで実装するのも大変だし中身がわからなくてもラップする方が合理的、という結論に至りました。簡単なもの（例えば、メルケプからMLSA filterの係数への変換とか）は、依存関係を少なくするためにもGo nativeで書きなおした方がいいです

コードは気が向いたら上げる
