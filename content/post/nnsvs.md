---
title: "    NNSVS: Pytorchベースの研究用歌声合成ライブラリ"
date: 2020-05-10T14:42:25+09:00
draft: false
---

- コード: https://github.com/r9y9/nnsvs
- Discussion: https://github.com/r9y9/nnsvs/issues/1
- [Demo on Google colab](https://colab.research.google.com/github/r9y9/Colaboratory/blob/master/Neural_network_based_singing_voice_synthesis_demo_using_kiritan_singing_database_(Japanese).ipynb)

> 春が来た　春が来た　どこに来た。　山に来た　里に来た、野にも来た。花がさく　花がさく　どこにさく。山にさく　里にさく、野にもさく。

<audio controls="controls" ><source src="/audio/nnsvs/20200510_haru.wav" autoplay/>Your browser does not support the audio element.</audio>

## NNSVS はなに？

*Neural network-based singing voice synthesis library for research*


研究用途を目的とした、歌声合成エンジンを作るためのオープンソースのライブラリを作ることを目指したプロジェクトです。このプロジェクトについて、考えていることをまとめておこうと思います。

### なぜやるか？

- [NEUTRINO](https://n3utrino.work/) レベルの品質の歌声合成エンジンが作れるのかやってみたかった
- オープンソースのツールがほぼない分野なので、ツールを作ると誰かの役にも立っていいかなと思った。研究分野が盛り上がると良いですね

というのが理由です。前者の割合が大きいです。

### 研究用途

機械学習や信号処理にある程度明るい人を想定しています。歌声合成技術を使って創作したい人ではなく、どのようにすればより良い歌声合成を作ることができるのか？といった興味を持つ人が主な対象です。

創作活動のために歌声合成の技術を使う場合には、すでに優れたツールがあると思いますので、そちらを使っていただくのがよいと思います[^1]。[NEUTRINO](https://n3utrino.work/)、[Synthesizer V](https://synthesizerv.com/jp/)、[CeVIO](http://cevio.jp/) など

[^1]: NEUTRINO並の品質の歌声合成エンジンが作れたらいいなとは思っていますが、まだまだ道のりは長そうです。

### オープンソース

オープンソースであることを重視します。歌声合成ソフトウェアは多くありますが、オープンソースのものは多くありません[^2]。このプロジェクトは僕が趣味として始めたもので、ビジネスにする気はまったくないので[^3]、誰でも自由に使えるようにしたいと思っています。オープンなソフトウェアが、研究分野の一助になることを期待しています。

[^2]: http://sinsy.sourceforge.net/ 有名なものにsinsyがありますが、DNNモデルの学習など、すべてがオープンソースなわけではありません
[^3]: 万が一の場合は、察してください…

### Pytorchベース

過去に [nnmnkwii](https://github.com/r9y9/nnmnkwii)という音声合成のためのライブラリを作りました。その際には、任意の数値微分ライブラリと使えるようにと考えて設計しましたが、nnsvsはあえてpytorchに依存した形で作ります。

PYtorchと切り離して設計すると汎用的にしやすい一方で、[Kaldi](https://github.com/kaldi-asr/kaldi) や[ESPnet](https://github.com/espnet/espnet) のようなプロジェクトで成功している**レシピ**というものが作りずらいです。ESPnetに多少関わって、再現性の担保の重要性を身にしみて感じつつあるので、Pytorchベースの学習、推論など、歌声合成のモデルを構築するために必要なすべてをひっくるめたソフトウェアを目指したいと思います。

### レシピの提供

再現性を重視します。そのために、KaldiやESPnetの成功に習って、レシピという実験を再現するのに必要なすべてのステップが含まれたスクリプトを提供します。レシピは、データの前処理、特徴量抽出、モデル学習、推論、波形の合成などを含みます。

例えば、このブログのトップに貼った音声サンプルを合成するのに使われたモデルは、公開されているレシピで再現することが可能です。歌声合成エンジンを作るためのありとあらゆるものを透明な形で提供します。

## プロジェクトの進め方について

完全に完成してから公開する、というアプローチとは正反対で、構想のみで実態はまったくできていない状態から始めて、進捗を含めてすべてオープンで確認できるような状態で進めます。進捗は https://github.com/r9y9/nnsvs/issues/1 から確認できます。

過去に[wavenet vocoder](https://github.com/r9y9/wavenet_vocoder)をつくったときにも同じような方法ではじめました。突然知らない人がコメントをくれたりするのがオープンソースの面白いところの一つだと思っているので、この方式で進めます。


## 現時点の状況

[きりたんデータベース](https://zunko.jp/kiridev/login.php)を使って、parametric SVS（Sinsyの中身に近いもの）が一通り作れるところまでできました。MusicXMLを入力として、音声波形を出力します。作った歌声合成システムは、time-lagモデル、音素継続長モデル、音響モデルの3つのtrainableなモデルで成り立っています。音楽/言語的特徴量は[sinsy](https://github.com/r9y9/sinsy)で抽出して、音声分析合成には[WORLD](https://github.com/mmorise/World)を使います。仕組みは、以下の論文の内容に近いです。

- Y. Hono et al, "Recent Development of the DNN-based Singing Voice Synthesis System — Sinsy," Proc. of APSIPA, 2017. ([PDF](http://www.apsipa.org/proceedings/2018/pdfs/0001003.pdf))

Mixture density networkは使っていない、ビブラートパラメータを推定していない等、違いはたくさんあります。現時点では劣化sinsyといったところですね T.T

## 開発履歴

### 2020/04/08 (初期版)

一番最初につくったものです。見事な音痴歌声合成になりました。TTSの仕組みを使うだけでは当然だめでした、というオチです。音響モデルでは対数lf0を予測するようにしました。このころはtime-lagモデルを作っていなくて、phonetic timeingはアノテーションされたデータのものを使っています。

<div align="center">
<iframe width="90%" height="200" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/792271372&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe>
</div>

### 2020/04/26 (本ブログ執筆時点での最新版)

Time-lag, duration, acoustic modelのすべてを一旦実装し終わったバージョンです。lf0の絶対値を予測するのではなく、relativeなlf0を予測するように変えました。phonetic timing はすべて予測されたものを使っています。ひととおりできたにはいいですが、完成度はいまいちというのが正直なところですね

<div align="center">
<iframe width="90%" height="200" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/806654083&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe>
</div>


## 今後の予定

https://github.com/r9y9/nnsvs/issues/1 を随時更新しますが、重要なものをいくつかピップアップします。

- **音響モデルの強化**：特にF0のモデル化が難しい印象で、改善を考えています。いまは本当に適当なCNNをつかっていますが、autoreggresive modelに変えたいと思っています。いくつか選択肢がありますが、WaveNetのようなモデルにする予定です。https://mtg.github.io/singing-synthesis-demos/ 彼らの論文を大いに参考にする予定です。NIIのWangさんのshallow ARモデルを使うもよし。最重要課題で、目下やることリストに入っています
- **離散F0モデリング**: NIIのWangさんの論文が大変参考になりました。音声合成では広く連続F0が使われている印象ですが、離散F0モデリングを試したいと思っています。
- **Transformerなどの強力なモデル**: 今年の [ICASSP 2020](https://2020.ieeeicassp.org/) で [Feed-forward Transformerを使った歌声合成の研究発表](https://mtg.github.io/singing-synthesis-demos/transformer/)がありましたが、近年のnon-autoregressiveモデルの発展はすごいので、同様のアプローチを試してみたいと思っています。製品化は考えないし、どんなにデカくて遅いモデルを使ってもよし
- **ニューラルボコーダ**: 音響モデルの改善がある程度できれば、ニューラルボコーダを入れて高品質にできるといいですね。
- **音楽/言語特徴量の簡略化**: 今は450次元くらいの特徴量を使っていますが、https://mtg.github.io/singing-synthesis-demos/ 彼らのグループの研究を見ると、もっとシンプルにできそうに思えてきています。音楽/言語特徴量の抽出は今はsinsyに頼りっきりですが、どこかのタイミングでシンプルにしたいと思っています。
- **Time-lag/duration modelの改善**: 現時点ではめっちゃ雑なつくりなので、https://mtg.github.io/singing-synthesis-demos/ 彼らの研究を見習って細部まで詰めたい
- **音素アライメントツール**: きりたんDBの音素アライメントが微妙に不正確なのがあったりします。今のところある程度手修正していますが、自動でやったほうがいいのではと思えてきました。
- **その他データセット**: JVSなど。きりたんDBである程度できてからですかね

## これまで歌声合成をやってみての所感

歌声合成クッソムズすぎワロタ

新しいことにチャレンジするのはとても楽しいですが、やっぱり難しいですね。離散化F0、autoregressive modelの導入でそれなりの品質に持っていけるという淡い期待をしていますが、さてどうなることやら。地道に頑張って改善していきます。


## 参考

- きりたんデータベース: https://zunko.jp/kiridev/login.php
- NEUTRINO: https://n3utrino.work/
- NNSVS: https://github.com/r9y9/nnsvs
- NNSVS 進捗: https://github.com/r9y9/nnsvs/issues/1
- sinsy: http://sinsy.sourceforge.net/
- My fork of sinsy: https://github.com/r9y9/sinsy
- nnmnkwii: https://github.com/r9y9/nnmnkwii
- WORLD: https://github.com/mmorise/World
- Y. Hono et al, "Recent Development of the DNN-based Singing Voice Synthesis System — Sinsy," Proc. of APSIPA, 2017. ([PDF](http://www.apsipa.org/proceedings/2018/pdfs/0001003.pdf))