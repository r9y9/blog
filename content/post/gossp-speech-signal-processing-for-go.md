---
layout: post
title: "GOSSP - Go言語で音声信号処理"
date: 2014-06-08
comments: true
categories: speech-signal-processing go
---

# C++からGoへ

みなさん、C++で信号処理のアルゴリズムを書くのはつらいと思ったことはありませんか？C++で書くと速いのはいいけれど、いかんせん書くのが大変、コンパイルエラーは読みづらい、はたまたライブラリをビルドしようとしたら依存関係が上手く解決できず……そんな覚えはないでしょうか？謎のコンパイルエラーに悩みたくない、ガーベジコレクションほしい、Pythonのようにさくっと書きたい、型推論もほしい、でも動作は速い方がいい、そう思ったことはないでしょうか。
	
そこでGoです。もちろん、そういった思いに完全に答えてくれるわけではありませんが、厳しいパフォーマンスを要求される場合でなければ、Goの方が良い場合も多いと僕は思っています。
とはいえ、まだ比較的新しい言語のため、ライブラリは少なく信号処理を始めるのも大変です。というわけで、僕がC++をやめてGoに移行したことを思い出し、Goでの信号処理の基礎と、今まで整備してきたGoでの音声信号処理ライブラリを紹介します。

Goの良いところ/悪いところについては書きません。正直、本当は何の言語でもいいと思っていますが、僕はGoが好きなので、ちょっとでもGoで信号処理したいと思う人が増えるといいなーと思って書いてみます。

あとで書きますが、僕が書いたコードで使えそうなものは、以下にまとめました。

https://github.com/r9y9/gossp 


# 基礎

## Wavファイルの読み込み/書き込み [[wav]](http://godoc.org/github.com/mjibson/go-dsp/wav)

<div align="center"><img src="/images/speech_signal.png "Speech signal example."" class="image"></div>

まずは音声ファイルの読み込みですね。wavファイルの読み込みさえできれば十分でしょう。

これは、すでに有用なライブラリが存在します。[GO-DSP](https://github.com/mjibson/go-dsp) とういデジタル信号処理のライブラリに含まれるwavパッケージを使いましょう。

次のように書くことができます。

```go
package main

import (
	"fmt"
	"github.com/mjibson/go-dsp/wav"
	"log"
	"os"
)

func main() {
	// ファイルのオープン
	file, err := os.Open("./test.wav")
	if err != nil {
		log.Fatal(err)
	}

	// Wavファイルの読み込み 
	w, werr := wav.ReadWav(file)
	if werr != nil {
		log.Fatal(werr)
	}

	// データを表示
	for i, val := range w.Data {
		fmt.Println(i, val)
	}
}
```

簡単ですね。

Goはウェブ周りの標準パッケージが充実しているので、以前[qiitaに書いた記事](http://qiita.com/r9y9/items/35a1cf139332a3072fc8)のように、wavファイルを受け取って何らかの処理をする、みたいなサーバも簡単に書くことができます

wavファイルの書き込み＋ユーティリティを追加したかったので、僕は自分でカスタムしたパッケージを使っています。

https://github.com/r9y9/go-dsp

## 高速フーリエ変換 (Fast Fourier Transform; FFT) [[fft]](http://godoc.org/github.com/mjibson/go-dsp/fft)

言わずとしれたFFTです。音のスペクトルを求めるのに必須の処理です。で、Goではどうすればいいのか？ということですが、こちらもすでに有用なライブラリが存在します。[GO-DSP](https://github.com/mjibson/go-dsp)に含まれる、fftパッケージを使いましょう。

このfftパッケージは、go routinesを使って平行化されているため速いです。僕は、1次元のフーリエ変換以外めったに使いませんが、N次元のフーリエ変換をサポートしているのもこのライブラリのいいところです。

### 参考
- [go-dsp FFT performance with go routines · Matt Jibson](http://mattjibson.com/blog/2013/01/04/go-dsp-fft-performance-with-go-routines/)

使い方は、とても簡単です。

```go
package main

import (
	"fmt"
	"github.com/mjibson/go-dsp/fft"
)

func main() {
	fmt.Println(fft.FFTReal([]float64{1, 2, 3, 4, 5, 6, 7, 8}))
}
```

## 離散コサイン変換 (Discrete Cosine Transform; DCT) [[dct]](http://godoc.org/github.com/r9y9/gossp/dct)

DCTは、Mel-Frequency Cepstrum Coefficients (通称MFCC) 求めるのに必要な変換です。こちらは、残念ながら良さそうなライブラリがなかったので、自分で書きました。

使い方はFFTとほとんど一緒です。

```go
package main

import (
	"fmt"
	"github.com/r9y9/gossp/dct"
)

func main() {
	y := dct.DCTOrthogonal([]float64{1, 2, 3, 4, 5, 6, 7, 8})
	fmt.Println(dct.IDCTOrthogonal(y)) // 直交変換では、逆変換すると元に戻る
}
```

さて、基本的なところは一旦ここまでです。次からは、少し音声寄りの信号処理手法の紹介です。

# 時間周波数解析

## 短時間フーリエ変換 (Short Time Fourier Transform; STFT) [[stft]](http://godoc.org/github.com/r9y9/gossp/stft)

<div align="center"><img src="/images/stft.png "STFT spectrogram"" class="image"></div>

STFTは、音声の時間周波数解析手法として定番の方法ですね。音声を可視化したり、何らかの認識アルゴリズムの特徴抽出に使ったり、まぁ色々です。

次のようなコードを書くと、スペクトログラムが作れます

```go
package main

import (
	"flag"
	"fmt"
	"github.com/r9y9/gossp"
	"github.com/r9y9/gossp/io"
	"github.com/r9y9/gossp/stft"
	"github.com/r9y9/gossp/window"
	"log"
	"math"
)

func main() {
	filename := flag.String("i", "input.wav", "Input filename")
	flag.Parse()

	w, werr := io.ReadWav(*filename)
	if werr != nil {
		log.Fatal(werr)
	}
	data := w.GetMonoData()

	s := &stft.STFT{
		FrameShift: int(float64(w.SampleRate) / 100.0), // 0.01 sec,
		FrameLen:   2048,
		Window:     window.CreateHanning(2048),
	}

	spectrogram := s.STFT(data)
	amplitudeSpectrogram, _ := gossp.SplitSpectrogram(spectrogram)
	PrintMatrixAsGnuplotFormat(amplitudeSpectrogram)
}

func PrintMatrixAsGnuplotFormat(matrix [][]float64) {
	fmt.Println("#", len(matrix[0]), len(matrix))
	for i, vec := range matrix {
		for j, val := range vec {
			fmt.Println(i, j, math.Log(val))
		}
		fmt.Println("")
	}
}
```

上の画像は、gnuplotで表示したものです

```
set pm3d map
sp "spectrogram.txt"
```

## 逆短時間フーリエ変換 (Inverse Short Time Fourier Transform; ISTFT) [[stft]](http://godoc.org/github.com/r9y9/gossp/stft)

ISTFTは、STFTの逆変換でスペクトログラムから時間領域の信号に戻すために使います。スペクトログラムを加工するような音源分離、ノイズ除去手法を使う場合には、必須の処理です。これはstftと同じパッケージ下にあります。

```
	reconstructed := s.ISTFT(spectrogram)
```

これで、スペクトログラムから音声を再構築することができます。

逆変換の仕組みは、意外と難しかったりします。

- [D. W. Griffin and J. S. Lim, "Signal estimation from modified short-time Fourier transform," IEEE Trans. ASSP, vol.32, no.2, pp.236–243, Apr. 1984.](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.306.7858)
- [L6: Short-time Fourier analysis and synthesis](http://research.cs.tamu.edu/prism/lectures/sp/l6.pdf)
- [Pythonで短時間フーリエ変換（STFT）と逆変換 - 音楽プログラミングの超入門（仮）](http://yukara-13.hatenablog.com/entry/2013/11/17/210204)

この辺を参考にしました。興味のある人は読んで見てください。

## 連続ウェーブレット変換 (Continuous Wavelet Transform; CWT)

<div align="center"><img src="/images/morlet_6_log.png "Morlet Wavelet spectrogram"" class="image"></div>

これは何回かブログで書きました。

- [FFTを使った連続ウェーブレット変換の高速化 - LESS IS MORE](http://r9y9.github.io/blog/2013/10/20/continuous-wavelet-tranform/)
- [連続ウェーブレット変換に使うマザーウェーブレット色々: Morlet, Paul, DOG - LESS IS MORE](http://r9y9.github.io/blog/2014/06/01/continuouos-wavelet-transform-types/)

コードは、テストがまだ通らないので開発中ということで…orz

## 逆連続ウェーブレット変換 (Inverse Continuous Wavelet Transform; ICWT)

連続ウェーブレット変換の逆変換ですね。これもけっこう難しいです。こちらもまだテストに通っていないので、開発中です。

- [逆連続ウェーブレット変換による信号の再構成 - LESS IS MORE](http://r9y9.github.io/blog/2013/10/21/signal-reconstruction-using-invere-cwt/) 

さて、この辺でまた一区切りです。次は、より音声に特化した信号処理手法を紹介します。

※以降紹介するもののうち、多くは[SPTK](http://sp-tk.sourceforge.net/)のGo-portになっていて、一部はcgoを使ってラップしただけです（後々はpure goにしたいけれど、特にメルケプストラム分析あたりは難しいのでできていません）

# 音声分析系

## 基本周波数推定 [[f0]](http://godoc.org/github.com/r9y9/gossp/f0)

<div align="center"><img src="/images/arayuru_f0.png "Fundamental frequency trajectory example."" class="image"></div>

ざっくり言えば音の高さを求める方法ですね。一応、音声に特化した方法をいくつか使えるようにしました。

- [A. de Cheveigne and H. Kawahara. YIN, a fundamental frequency estimator for speech and music. J. Acoust. Soc. Am., 111(4):1917–1930, 2002.](http://audition.ens.fr/adc/pdf/2002_JASA_YIN.pdf)
- [A. Camacho. SWIPE: A sawtooth waveform inspired pitch estimator for speech and music. PhD thesis, University of Florida, 2007.](http://www.cise.ufl.edu/~acamacho/publications/dissertation.pdf)

ただしYINはもどきです。

以前、[GO-WORLD](https://github.com/r9y9/go-world)という音声分析合成系WORLDのGoラッパーを書いたので、それを使えばF0推定手法Dioが使えます。

### 参考

- [音声分析変換合成システムWORLDのGoラッパーを書いた - LESS IS MORE](http://r9y9.github.io/blog/2014/03/22/go-world/)

## メルケプストラム分析 [[mgcep]](http://godoc.org/github.com/r9y9/gossp/mgcep)

音声合成界隈ではよく聞くメルケプストラム（※MFCCとは異なります）を求めるための分析手法です。メルケプストラムは、HMM（Hidden Markov Models; 隠れマルコフモデル）音声合成や統計的声質変換において、声道特徴（いわゆる、声質）のパラメータ表現としてよく使われています。メルケプストラムの前に、LPCとかPARCORとか色々あるのですが、現在のHMM音声合成で最もよく使われているのはメルケプストラムな気がするので、メルケプストラム分析があれば十分な気がします。

これは、SPTKをcgoを使ってラップしました

### 参考

- [徳田恵一, 小林隆夫, 深田俊明, 斎藤博徳, 今井 聖, “メルケプストラムをパラメータとする音声のスペクトル推定,” 信学論(A), vol.J74-A, no.8, pp.1240–1248, Aug. 1991.](http://ci.nii.ac.jp/naid/40004638236/)

## メル一般化ケプストラム分析 [[mgcep]](http://godoc.org/github.com/r9y9/gossp/mgcep)

メル一般化ケプストラム分析は、その名の通りメルケプストラム分析を一般化したものです。メルケプストラム分析はもちろん、LPCも包含します（詳細は、参考文献をチェックしてみてください）。論文をいくつかあさっている限り、あんまり使われていない気はしますが、これもSPTKをラップしてGoから使えるようにしました。メルケプストラム分析もメル一般化ケプストラム分析に含まれるので、mgcepという一つのパッケージにしました。

### 参考

- [Tokuda, K., Masuko, T., Kobayashi, T., Imai, S., 1994. Mel-generalized Cepstral Analysis-A Uniﬁed Approach to Speech Spectral Estimation, ISCA ICSLP-94: Inter. Conf. Spoken Lang. Proc., Yokohama, Japan, pp. 1043–1046.](http://www.utdallas.edu/~john.hanse/nPublications/JP-55-SpeechComm-Yapanel-Hansen-PMVDR-Feb08.pdf)

# 音声合成系

## 励起信号の生成 [[excite]](http://godoc.org/github.com/r9y9/gossp/excite)

<div align="center"><img src="/images/pulse_excite.png "Exciation eignal."" class="image"></div>

SPTKのexciteのGo実装です。いわゆるPulseExcitationという奴ですね。非周期成分まったく考慮しない単純な励起信号です。

高品質な波形合成が必要な場合は、WORLDやSTRAIGHTを使うのが良いです。

## MLSA (Mel Log Spectrum Approximation) デジタルフィルタ [[vocoder]](http://godoc.org/github.com/r9y9/gossp/vocoder)

MLSAフィルタは、メルケプストラムと励起信号から音声波形を合成するためのデジタルフィルタです。HMM音声合成の波形合成部で使われています（今もきっと）。Pure goで書き直しました。

昔、C++でも書いたことあります。

### 参考

- [MLSA digital filter のC++実装 - LESS IS MORE](http://r9y9.github.io/blog/2013/12/01/mlsa-filter-with-c-plus-plus/)

## MGLSA (Mel Genaralized-Log Spectrum Approximation) デジタルフィルタ [[vocoder]](http://godoc.org/github.com/r9y9/gossp/vocoder)

MGLSAフィルタは、メル一般化ケプストラムから波形を合成するためのデジタルフィルタですね。これも pure goで書きました。

## **※SPTKの再実装について**

SPTKの実装をGoで書き直したものについては、SPTKの実装と結果が一致するかどうかを確認するテストを書いてあります。よって、誤った結果になるということは（計算誤差が影響する場合を除き）基本的にないので、お気になさらず。

## 高品質な音声分析変換合成系 WORLD [[go-world]](http://godoc.org/github.com/r9y9/go-world)

[音声分析変換合成システムWORLDのGoラッパーを書いた - LESS IS MORE](http://r9y9.github.io/blog/2014/03/22/go-world/)

以前WORLDのGoラッパーを書いたので、色々使えると思います。統計ベースの音声合成とか、声質変換とか。僕は声質変換に使おうと思ってラップしました。

# おわりに

長々と書きましたが、Go言語での信号処理の基礎と、今まで整備してきた音声信号処理ライブラリを簡単に紹介しました。僕が書いたものは、まとめてGithubで公開しています。

https://github.com/r9y9/gossp

使ってももらって、あわよくばバグとか報告してもらって、改善していければいいなーというのと、あとGithubのissue管理便利だし使おうと思ってGithubに上げました。

みなさん、Goで音声信号処理始めてみませんか？

# 余談

## Pythonではダメなの？その他言語は？

なんでGoなの？と思う人がいると思います。冒頭にも書いたとおり、正直好きなのにすればいいですが、適当に書いて速いのがいいならC++だし、型を意識せずさくっと書きたいならPythonだし、そこそこ速くて型があって型推論もあって、とかだったらGoがいいかなと僕は思います。

Goの特徴（≒良さ）ついては、[20130228 Goノススメ（BPStudy #66） | SlideShare](http://www.slideshare.net/ymotongpoo/20130228-gobp-study-66-16830134)
 の11枚目が僕にはドンピシャです。

numpy, scipy, matplotlib, scikit-learnあたりが最強すぎるので、僕はpythonも良く使います。

## きっかけ

この記事を書いたきっかけは、友人にGoをおすすめしまくっていたのに全然聞いてくれなかったからでした。Goでも信号処理はできるよ
