---
layout: post
title: "Goでクロマベクトルを求める"
date: 2014-01-28
comments: true
categories: Go, Music-signal-processing
---

<div align="center"><img src="/images/pcp_result.png "Chromagram"" class="image"></div>

Chromagram。ドレミの歌の冒頭を分析した結果です

```go
package main

import (
	"fmt"
	"github.com/mjibson/go-dsp/wav"
	"github.com/r9y9/go-msptools/pcp"
	"log"
	"os"
)

func main() {
	// reading data
	file, err := os.Open("/path/to/file.wav")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	wav, werr := wav.ReadWav(file)
	if werr != nil {
		log.Fatal(werr)
	}

	// convert to []float64 from []int
	data := make([]float64, len(wav.Data[0]))
	for i := range data {
		data[i] = float64(wav.Data[0][i])
	}

	// settings for analysis
	frameShift := int(float64(wav.SampleRate) / 100.0) // 0.01 sec
	sampleRate := int(wav.SampleRate)

	// create PCP extrator
	p := pcp.NewPCP(sampleRate, frameShift)

	// analysis roop
	result := make([][]float64, p.NumFrames(data))
	for i := 0; i < p.NumFrames(data); i++ {
		pcp := p.PCP(data, i*frameShift)
		//pcp := p.PCPNormalized(data, i*frameShift)
		result[i] = pcp
	}

	// print as a gnuplot 3D plotting format
	fmt.Println("#", len(result[0]), len(result))
	for i, spec := range result {
		for j, val := range spec {
			fmt.Println(i, j, val)
		}
		fmt.Println("")
	}
}
```

こんな感じでOK。Chromagramをgnuplot形式で標準出力に出力します

## Pitch Class Profile (PCP) in Go [[Code]](https://github.com/r9y9/go-msptools/tree/master/pcp)

どうやってクロマベクトルを計算しているかざっくり説明すると、

- 入力信号をガボールウェーブレット変換
- オクターブ無視して12次元に圧縮（例えば55Hz, 110Hz, 220Hz, 440Hz はすべてAとする）

という手順で求めてます

Goかどうかなんてどうでもいいんだけど、まぁC++に比べて書きやすすぎて泣けるよね
