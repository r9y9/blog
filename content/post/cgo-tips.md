---
layout: post
title: "cgo の基本的な使い方とポインタ周りのTips (Go v1.2)"
date: 2014-03-22
comments: true
categories: Go cgo
---

C/C++ライブラリのGoラッパーを書くためには、cgoというパッケージを使うのだけど、特にCのポインタ周りにハマりどころが多かったので、少しまとめとく

cgoの基礎については、以下の二つを読むことを推奨

* http://golang.org/cmd/cgo/
* https://code.google.com/p/go-wiki/wiki/cgo

この記事では、cgo基本的な使い方と、いくつかポインタ絡みのTipsをまとめる。Tipsのみ必要な場合は、最初の方は飛ばして下さい

## cgo

> Cgo enables the creation of Go packages that call C code.

http://golang.org/cmd/cgo/

cgoとは、GoからCの関数/型にアクセスするために用いるパッケージのこと。cgoを使えば、GoからCのコードが呼べる。つまり、**Cで書かれたライブラリが、Goでも再利用できる**。

なお、go v1.2 から、C++もサポートされている様子
http://golang.org/doc/go1.2#cgo_and_cpp

ただし、C++ライブラリの使用方法については現時点でドキュメントはほぼ無し。僕の経験では、extern "C" を付けておくとC++用のコンパイラでコンパイルされたライブラリでも呼べる

## 基本的な使い方

まず、Cの型/関数にアクセスするために、cgoパッケージのimportを行う

```go
import "C"
```

import文のすぐ上のコメントにinclude <ヘッダ.h> と書けば、コンパイルする際に自動で読み込まれるので、必要なヘッダを書く

```go
// #include <stdio.h>
// #include <stdlib.h>
import "C"
```

これで、C.int, C.float, C.double, *C.char、C.malloc, C.free などのようにして、Cの型や関数にアクセスできる

## 外部ライブラリを呼ぶ

通常は、ヘッダファイルをincludeするだけでなく、何かしらのライブラリとリンクして用いることが多いので、そのような場合には、ライブラリの依存関係をgoのコードに記述する

cgoでは、includeの設定と同様に、CFLAGS、CPPFLAGS、CXXFLAGS、LDFLAGS、pkg-configを記述することができる

pkg-configを使うと 、

```go
// #cgo pkg-config: png cairo
// #include <png.h>
import "C"
```

こんな感じ（[Goの公式ページ](http://golang.org/cmd/cgo/)から参照）

## Tips

さて、ここからTips。主に、[WORLD](ml.cs.yamanashi.ac.jp/world/)のGoラッパーを書いていたときに得た知見です。ラッパーは、[Github](https://github.com/r9y9/go-world)にあげた

## 1. GoのスライスをCのポインタとして関数の引数に渡す

例えば、[]float64 -> double* のイメージ

これは比較的簡単にできる。以前qiitaにも書いた
http://qiita.com/r9y9/items/e6d879c9b7d4f2697593

```go
(*C.double)(&slice[0])
```

のようにキャストしてやればOK

## 2. GoのスライスのスライスをCのポインタのポインタとして関数の引数に渡す

[][]float64 -> double** のようなイメージ

例として、worldから引っ張ってきた以下のようなCの関数を考える

```c++
void Star(double *x, int x_length, int fs, double *time_axis, double *f0,
  int f0_length, double **spectrogram);
```

\*\*spectrogramには処理結果が格納される。もちろん処理結果はGoの型で扱いたいんだが、では**\*\*spectrogramにどうやってGoの型を渡すか？**ということが問題になる

doubleの二次元配列なので、

```go
s := [][]float64
```

というスライスのスライスを考えて、キャストして渡したいところだけど、結論から言うとこれはできない

ではどうするかというと、苦肉の策として、
```go
wspace := make([]*C.double, len(f0))
```

というスライスを考えて、

```
(**C.double)(&wspace[0])
```

とすれば、double\*\*として関数の引数に渡すことができる。他にも方法がある気がするが、これでも期待通りの動作をする（あまりハックっぽいことしたくない…

まとめると、

* [][]float64 -> double**はできないが、
* []*C.double -> double\*\*はできる。よって、一応Goの型をdouble**に渡すことはできる

です。

## 3. ポインタのポインタからスライスのスライスへの変換

double** -> [][]float64 のようなイメージ

Tipsその2の例より、Cの関数の処理が終われば\*\*spectrogramにデータが格納される。もちろん処理結果はGoの型で扱いたいので、[][]float64 にしたい。ただし、先程の例では、Cの関数に渡した型は実際には []*C.doubleで、Cの型を含んでいる。

そこで、次に問題になるのは、**[]*C.doubleにから[][]float64 に変換するにはどうするか？**ということ。そして、これも面倒です…（※節の頭でdouble\*\* -> [][]float64と書いたけど、正確には []*C.double -> [][]float64）

結論から言えば、直接の変換は難しいけど中間変数をかませばできる

* []bytes型でtmp変数を作り、`C.GoBytes` を使って*C.double -> []bytes にコピー
* encoding/binaryパッケージを使って、[]bytes -> []float64 に書き込み
* この処理をsliceOfSlices[0], sliceOfSlices[1], ... に対して繰り返す

以上。とても面倒ですね…

さて、結局上のStarのラッパーは以下のようになった

```go
func Star(x []float64, fs int, timeAxis, f0 []float64) [][]float64 {
	FFTSize := C.size_t(C.GetFFTSizeForStar(C.int(fs)))
	numFreqBins := FFTSize/2 + 1

	// Create workspace
	wspace := make([]*C.double, len(f0))
	for i := range wspace {
		wspace[i] = (*C.double)(C.malloc(byteSizeOfFloat64 * numFreqBins))
		defer C.free(unsafe.Pointer(wspace[i]))
	}

	// Perform star
	C.Star((*C.double)(&x[0]),
		C.int(len(x)),
		C.int(fs),
		(*C.double)(&timeAxis[0]),
		(*C.double)(&f0[0]),
		C.int(len(f0)),
		(**C.double)(&wspace[0]))

	// Copy to go slice
	spectrogram := make([][]float64, len(f0))
	for i := range spectrogram {
		spectrogram[i] = CArrayToGoSlice(wspace[i], C.int(numFreqBins))
	}

	return spectrogram
}
```

上で使っているutility function

```go
func CArrayToGoSlice(array *C.double, length C.int) []float64 {
	slice := make([]float64, int(length))
	b := C.GoBytes(unsafe.Pointer(array), C.int(byteSizeOfFloat64*length))
	err := binary.Read(bytes.NewReader(b), binary.LittleEndian, slice)
	if err != nil {
		panic(err)
	}
	return slice
}
```

* []*C.double のスライスを作り、作業領域のメモリを確保する（Tips2の内容+メモリ確保）
* []*C.double のスライスをdouble** にキャストして、Cの関数を実行（Tips2の内容）
* []*C.double から[][]float64に変換する（Tips3の内容）

という手順になってます

**※2013/03/27 追記**
:もっとシンプルかつ効率的（copyの必要がないように）に書けた。[][]float64で返り値用のスライスを作り、それを[]*double型に変換してCに渡せば、[][]float64に変更が反映されるので、そもそも[]*doubleから[][]float64に変換する必要はなかった。

```go
func Star(x []float64, fs int, timeAxis, f0 []float64) [][]float64 {
	FFTSize := C.size_t(C.GetFFTSizeForStar(C.int(fs)))
	numFreqBins := C.size_t(FFTSize/2 + 1)

	spectrogram := make([][]float64, len(f0))
	for i := range spectrogram {
		spectrogram[i] = make([]float64, numFreqBins)
	}

	spectrogramUsedInC := Make2DCArrayAlternative(spectrogram)

	// Perform star
	C.Star((*C.double)(&x[0]),
		C.int(len(x)),
		C.int(fs),
		(*C.double)(&timeAxis[0]),
		(*C.double)(&f0[0]),
		C.int(len(f0)),
		(**C.double)(&spectrogramUsedInC[0]))

	return spectrogram
}
```

```go

func Make2DCArrayAlternative(matrix [][]float64) []*C.double {
	alternative := make([]*C.double, len(matrix))
	for i := range alternative {
		// DO NOT free because the source slice is managed by Go
		alternative[i] = (*C.double)(&matrix[i][0])
	}
	return alternative
}
```

## おわりに

* ポインタのポインタを引数に取る関数のラップはめんどくさい
* Goは使いやすいのに ~~cgoは使いにくい~~
* cgoつらい
* よりいい方法があれば教えて下さい

## 2014/08/10 追記 

cgo使いにくいと書いたけど、あとから考えてみればcgoさんまじ使いやすかったです（遅い

Juliaのccallはもっと使いやすい。
