+++
date = "2017-10-10T11:45:32+09:00"
draft = false
title = "GAN 日本語音声合成 [arXiv:1709.08041]"
tags  = [ "Speech", "DNN"]
categories = ["Speech synthesis", "Python"]

+++

論文リンク: [arXiv:1709.08041](https://arxiv.org/abs/1709.08041)

[前回の記事](/blog/2017/10/09/gantts/) の続きです。これでこのシリーズは終わりの予定です。

前回は英語音声合成でしたが、以前書いた [DNN日本語音声合成の記事](/blog/2017/08/16/japanese-dnn-tts/) で使ったデータと同じものを使い、日本語音声合成をやってみましたので、結果を残しておきます。

## 実験

### 実験条件

HTSのNIT-ATR503のデモデータ ([ライセンス](https://github.com/r9y9/nnmnkwii_gallery/blob/4899437e22528399ca50c34097a2db2bed782f8b/data/NIT-ATR503_COPYING)) から、wavデータ503発話を用います。442を学習用、56を評価用、残り5をテスト用にします（※英語音声とtrain/evalの比率は同じです）。継続長モデルは、state-levelではなくphone-levelです。サンプリング周波数が48kHzなので、mgcの次元を25から60に増やしました。モデル構造は、すべて英語音声合成の場合と同じです。ADV loss は0次を除くmgcを用いて計算しました。F0は入れていません。

[gantts](https://github.com/r9y9/gantts) の [jpブランチ](https://github.com/r9y9/gantts/tree/jp) をチェックアウトして、以下のシェルを実行すると、ここに貼った結果が得られます。

```
 ./jp_tts_demo.sh jp_tts_order59
```

ただし、シェル中に、`HTS_ROOT` という変数があり、シェル実行前に、環境に合わせてディレクトリを指定する必要があります。

```diff
diff --git a/jp_tts_demo.sh b/jp_tts_demo.sh
index 7a8f12c..b18e604 100755
--- a/jp_tts_demo.sh
+++ b/jp_tts_demo.sh
@@ -8,7 +8,7 @@ experiment_id=$1
 fs=48000

 # Needs adjastment
-HTS_DEMO_ROOT=~/local/HTS-demo_NIT-ATR503-M001
+HTS_DEMO_ROOT=HTS日本語デモの場所を指定してください

 # Flags
 run_duration_training=1
```

### 変換音声の比較

#### 音響モデルのみ適用

1. 自然音声
2. ベースライン
3. GAN

の順に音声を貼ります。聴きやすいように、soxで音量を正規化しています。

**nitech_jp_atr503_m001_j49**

<audio controls="controls" >
<source src="/audio/nit-atr503/nitech_jp_atr503_m001_j49.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/acoustic_only/baseline/test/nitech_jp_atr503_m001_j49.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/acoustic_only/gan/test/nitech_jp_atr503_m001_j49.wav" autoplay/>
Your browser does not support the audio element.
</audio>


**nitech_jp_atr503_m001_j50**

<audio controls="controls" >
<source src="/audio/nit-atr503/nitech_jp_atr503_m001_j50.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/acoustic_only/baseline/test/nitech_jp_atr503_m001_j50.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/acoustic_only/gan/test/nitech_jp_atr503_m001_j50.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**nitech_jp_atr503_m001_j51**

<audio controls="controls" >
<source src="/audio/nit-atr503/nitech_jp_atr503_m001_j51.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/acoustic_only/baseline/test/nitech_jp_atr503_m001_j51.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/acoustic_only/gan/test/nitech_jp_atr503_m001_j51.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**nitech_jp_atr503_m001_j52**

<audio controls="controls" >
<source src="/audio/nit-atr503/nitech_jp_atr503_m001_j52.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/acoustic_only/baseline/test/nitech_jp_atr503_m001_j52.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/acoustic_only/gan/test/nitech_jp_atr503_m001_j52.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**nitech_jp_atr503_m001_j53**

<audio controls="controls" >
<source src="/audio/nit-atr503/nitech_jp_atr503_m001_j53.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/acoustic_only/baseline/test/nitech_jp_atr503_m001_j53.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/acoustic_only/gan/test/nitech_jp_atr503_m001_j53.wav" autoplay/>
Your browser does not support the audio element.
</audio>


#### 音響モデル＋継続長モデルを適用

**nitech_jp_atr503_m001_j49**

<audio controls="controls" >
<source src="/audio/nit-atr503/nitech_jp_atr503_m001_j49.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/duration_acoustic/baseline/test/nitech_jp_atr503_m001_j49.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/duration_acoustic/gan/test/nitech_jp_atr503_m001_j49.wav" autoplay/>
Your browser does not support the audio element.
</audio>


**nitech_jp_atr503_m001_j50**

<audio controls="controls" >
<source src="/audio/nit-atr503/nitech_jp_atr503_m001_j50.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/duration_acoustic/baseline/test/nitech_jp_atr503_m001_j50.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/duration_acoustic/gan/test/nitech_jp_atr503_m001_j50.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**nitech_jp_atr503_m001_j51**

<audio controls="controls" >
<source src="/audio/nit-atr503/nitech_jp_atr503_m001_j51.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/duration_acoustic/baseline/test/nitech_jp_atr503_m001_j51.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/duration_acoustic/gan/test/nitech_jp_atr503_m001_j51.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**nitech_jp_atr503_m001_j52**

<audio controls="controls" >
<source src="/audio/nit-atr503/nitech_jp_atr503_m001_j52.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/duration_acoustic/baseline/test/nitech_jp_atr503_m001_j52.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/duration_acoustic/gan/test/nitech_jp_atr503_m001_j52.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**nitech_jp_atr503_m001_j53**

<audio controls="controls" >
<source src="/audio/nit-atr503/nitech_jp_atr503_m001_j53.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/duration_acoustic/baseline/test/nitech_jp_atr503_m001_j53.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/jp_tts_order59/duration_acoustic/gan/test/nitech_jp_atr503_m001_j53.wav" autoplay/>
Your browser does not support the audio element.
</audio>

どうでしょうか。ちょっと早口になってしまっている箇所もありますが、全体的には明瞭性が上がって、品質が改善されたような感じがします。若干ノイジーな感じは、音響モデルにRNNを使えば改善されるのですが、今回は計算リソースの都合上、Feed-forward型のサンプルとなっています。

### GV

`nitech_jp_atr503_m001_j49` に対して計算した結果です。

<div align="center"><img src="/images/jp-gantts/nitech_jp_atr503_m001_j49_gv.png" /></div>

英語音声合成の実験でも確認しているのですが、mgcの次元を大きく取ると、高次元でGVが若干落ちる傾向にあります。ただし、[一週間前の僕のツイート](https://twitter.com/r9y9/status/915213687891169280) によると、なぜかそんなこともなく（当時ばりばりのプロトタイピングの時期だったので、コードが残っておらず、いまは再現できないという、、すいません）、僕が何かミスをしている可能性もあります。ただ、品質はそんなに悪くないように思います。

### 変調スペクトル

評価用セットで平均を取ったものです。

<div align="center"><img src="/images/jp-gantts/ms.png" /></div>

### 特徴量の分布

`nitech_jp_atr503_m001_j49` に対して計算した結果です。

<div align="center"><img src="/images/jp-gantts/nitech_jp_atr503_m001_j49_scatter.png" /></div>

### おまけ: HTSデモと聴き比べ

HTSデモを実行すると生成されるサンプルとの聴き比べです。注意事項ですが、**実験条件がまったく異なります**。あくまで参考程度にどうぞ。

1. HTSデモ
2. ベースライン
3. GAN

の順に音声を貼ります。

1 こんにちは

<audio controls="controls" >
<source src="/audio/hts_nit_atr503_2mix/phrase01.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/test/baseline/phrase01.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/test/gan/phrase01.wav" autoplay/>
Your browser does not support the audio element.
</audio>

2 それではさようなら

HTS

<audio controls="controls" >
<source src="/audio/hts_nit_atr503_2mix/phrase02.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/test/baseline/phrase02.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/test/gan/phrase02.wav" autoplay/>
Your browser does not support the audio element.
</audio>


3 はじめまして

<audio controls="controls" >
<source src="/audio/hts_nit_atr503_2mix/phrase03.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/test/baseline/phrase03.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/test/gan/phrase03.wav" autoplay/>
Your browser does not support the audio element.
</audio>


4 ようこそ名古屋工業大学へ

<audio controls="controls" >
<source src="/audio/hts_nit_atr503_2mix/phrase04.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/test/baseline/phrase04.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/test/gan/phrase04.wav" autoplay/>
Your browser does not support the audio element.
</audio>


5 今夜の名古屋の天気は雨です

<audio controls="controls" >
<source src="/audio/hts_nit_atr503_2mix/phrase05.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/test/baseline/phrase05.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<audio controls="controls" >
<source src="/audio/jp-gantts/test/gan/phrase05.wav" autoplay/>
Your browser does not support the audio element.
</audio>


## おわりに

アイデアはシンプル、効果は素晴らしいという、僕の好きな（試したくなる）研究の紹介でした。ありがとうございました。


## 参考

- [Yuki Saito, Shinnosuke Takamichi, Hiroshi Saruwatari, "Statistical Parametric Speech Synthesis Incorporating Generative Adversarial Networks", arXiv:1709.08041 [cs.SD], Sep. 2017](https://arxiv.org/abs/1709.08041)
