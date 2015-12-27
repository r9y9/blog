---
layout: post
title: "音声分析変換合成システムWORLDのGoラッパーを書いた"
date: 2014-03-22
comments: true
categories: Speech-signal-processing Go
---

## 音声分析変換合成システムWORLD

WORLDとは、山梨大学の森勢先生が作られている高品質な音声分析変換合成システムです。非常に高品質かつ高速に動作するのが良い所です。詳細は以下のURLへ

http://ml.cs.yamanashi.ac.jp/world/

オリジナルはC+＋で書かれていますが、Goからも使えるようにラッパーを書きました。非常にいいソフトウェアなので、もしよろしければどうぞ

## GO-WORLD

https://github.com/r9y9/go-world

使い方について、ほんの少し解説を書きます

※ubuntu12.04でのみ動作確認してます。

## 準備

### 1. WORLDのインストール

まずWORLDをインストールする必要があります。公式のパッケージではinstallerに相当するものがなかったので、作りました

https://github.com/r9y9/world

```bash
 ./waf configure && ./waf
 sudo ./waf install
```

でインストールできます。

なお、WORLDは最新版ではなく0.1.2としています。最新版にすると自分の環境でビルドコケてしまったので…

### 2. GO-WORLDのインストール

```bash
go get github.com/r9y9/go-world
```

簡単ですね！

## 使い方

### 1. インポートする

```go
import "github.com/r9y9/go-world"
```

### 2. worldのインスタンスを作る

```go
w := world.New(sampleRate, framePeriod) // e.g. (44100, 5)
```

### 3. 好きなworldのメソッドを呼ぶ

#### 基本周波数の推定: Dio 

```go
timeAxis, f0 := w.Dio(input, w.NewDioOption()) // default option is used
```

#### スペクトル包絡の推定: Star

```go
spectrogram := w.Star(input, timeAxis, f0)
```

#### 励起信号の推定: Platinum

```go
residual := w.Platinum(input, timeAxis, f0, spectrogram)
```

#### パラメータから音声の再合成: Synthesis

```go
synthesized := w.Synthesis(f0, spectrogram, residual, len(input))
```

## 使い方例. 

音声（wavファイル）を分析して、パラメータから音声を再合成する例を紹介します。80行弱と少し長いですがはっつけておきます

```go
package main

import (
	"flag"
	"fmt"
	"github.com/mjibson/go-dsp/wav"
	"github.com/r9y9/go-world"
	"log"
	"os"
)

var defaultDioOption = world.DioOption{
	F0Floor:          80.0,
	F0Ceil:           640.0,
	FramePeriod:      5,
	ChannelsInOctave: 4.0,
	Speed:            6,
}

// 音声を基本周波数、スペクトル包絡、励起信号の三つに分解したあと、再合成します
func worldExample(input []float64, sampleRate int) []float64 {
	w := world.New(sampleRate, defaultDioOption.FramePeriod)

	// 1. Fundamental frequency
	timeAxis, f0 := w.Dio(input, defaultDioOption)

	// 2. Spectral envelope
	spectrogram := w.Star(input, timeAxis, f0)

	// 3. Excitation spectrum
	residual := w.Platinum(input, timeAxis, f0, spectrogram)

	// 4. Synthesis
	return w.Synthesis(f0, spectrogram, residual, len(input))
}

// 音声を基本周波数、スペクトル包絡、非周期成分の三つに分解したあと、再合成します
func worldExampleAp(input []float64, sampleRate int) []float64 {
	w := world.New(sampleRate, defaultDioOption.FramePeriod)

	// 1. Fundamental frequency
	timeAxis, f0 := w.Dio(input, defaultDioOption)

	// 2. Spectral envelope
	spectrogram := w.Star(input, timeAxis, f0)

	// 3. Apiriodiciy
	apiriodicity, targetF0 := w.AperiodicityRatio(input, f0)

	// 4. Synthesis
	return w.SynthesisFromAperiodicity(f0, spectrogram, apiriodicity, targetF0, len(input))
}

func GetMonoDataFromWavData(data [][]int) []float64 {
	y := make([]float64, len(data))
	for i, val := range data {
		y[i] = float64(val[0])
	}
	return y
}

func main() {
	ifilename := flag.String("i", "default.wav", "Input filename")
	flag.Parse()

	// Read wav data
	file, err := os.Open(*ifilename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	w, werr := wav.ReadWav(file)
	if werr != nil {
		log.Fatal(werr)
	}
	input := GetMonoDataFromWavData(w.Data)
	sampleRate := int(w.SampleRate)

	synthesized := worldExample(input, sampleRate)
	// synthesized := worldExampleAp(input, sampleRate)

	for i, val := range synthesized {
		fmt.Println(i, val)
	}
}
```

Goだとメモリ管理きにしなくていいしそこそこ速いし読みやすいし書きやすいし楽でいいですね（信者

## おわりに

* GoはC++ほど速くはないですが、C++の何倍も書きやすいし読みやすい（メンテしやすい）ので、個人的にオススメです（パフォーマンスが厳しく要求される場合には、C++の方がいいかもしれません）
* WORLD良いソフトウェアなので使いましょう

## ちなみに

元はと言えば、オレオレ基本周波数推定（YINもどき）が微妙に精度悪くて代替を探していたとき、

* SPTKのRAPTかSWIPE使おうかな…
* RAPTもSWIPEもSPTK.hにインタフェースがない…
* うわRAPTのコード意味わからん
* SWIPEのコードまじ謎
* 後藤さんのPreFest実装しよう
* あれ上手くいかない…orz
* どうしようかな…

となっていたときに、森勢先生が書いたと思われる以下の文献を見つけて、

[2-2 基本周波数推定（歌声研究に関する視点から）](http://crestmuse.jp/handbookMI/pdf/2_2_PitchExtraction_Morise.pdf)

> 本方法は，低域に雑音が存在する音声に対する推定は困難であるが，低域の雑音が存在しない音声の場合，SWIPE′ や NDF と実質的に同等の性能を達成しつつ，計算時間を SWIPE′の 1/42, NDF の 1/80 にまで低減可能である．

あぁworld使おう（白目

となり、ラッパーを書くにいたりましたとさ、おしまい
