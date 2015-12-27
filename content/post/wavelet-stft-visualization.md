---
layout: post
title: "短時間フーリエ変換と連続ウェーブレット変換のvisualization"
date: 2013-10-20
comments: true
categories: wavelet-transform short-time-fourier-transform signal-processing visualization
---

## STFT(短時間フーリエ変換)によるスペクトログラム

<div align="center"><img src="/images/spectrogram_linear_clipped_rev_1.png "STFT spectrogram"" class="image"></div>


## STFTによるスペクトログラム（Y軸を対数にしたもの）
<div align="center"><img src="/images/spectrogram_log_clipped_rev_1.png "STFT spectrogram (with log-y-axis)"" class="image"></div>

## 連続ガボールウェーブレット変換によるスペクトログラム
<div align="center"><img src="/images/wavelet_spectrogram_clipped_rev_1.png "Gabor Wavelet spectrogram"" class="image"></div>

メモリも軸も無くて発表資料に貼ったら間違いなく怒られる奴だけど許して。でもだいたいの違いはわかると思う。図はgnuplotで作りました

STFTのlog-y-axisと比べるとよくわかるけど、ウェーブレットは低域もちゃんと綺麗にとれてますね。

みんなもっとウェーブレット変換使おう（提案

## 分析に使った音声
決して聞いてはならない

<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/116165738"></iframe>
