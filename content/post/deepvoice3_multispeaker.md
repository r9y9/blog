+++
date = "2017-12-22T15:30:00+09:00"
draft = false
title = "【108 話者編】Deep Voice 3: 2000-Speaker Neural Text-to-Speech / arXiv:1710.07654 [cs.SD]"
tags  = [ "Speech", "DNN"]
categories = ["Speech synthesis", "Python"]

+++


- 論文リンク: [arXiv:1710.07654](https://arxiv.org/abs/1710.07654)
- コード: https://github.com/r9y9/deepvoice3_pytorch
- VCTK: http://homepages.inf.ed.ac.uk/jyamagis/page3/page58/page58.html
- 音声サンプルまとめ: https://r9y9.github.io/deepvoice3_pytorch/


## 三行まとめ

- [arXiv:1710.07654: Deep Voice 3: 2000-Speaker Neural Text-to-Speech](https://arxiv.org/abs/1710.07654) を読んで、複数話者の場合のモデルを実装しました
- 論文のタイトル通りの2000話者とはいきませんが、[VCTK](http://homepages.inf.ed.ac.uk/jyamagis/page3/page58/page58.html) を使って、108 話者対応の英語TTSモデルを作りました（学習時間1日くらい）
- 入力する話者IDを変えることで、一つのモデルでバリエーションに富んだ音声サンプルを生成できることを確認しました

## 概要

[【単一話者編】Deep Voice 3: 2000-Speaker Neural Text-to-Speech / arXiv:1710.07654 [cs.SD]](/blog/2017/12/13/deepvoice3/) の続編です。

論文概要は前回紹介したものと同じなので、話者の条件付けの部分についてのみ簡単に述べます。なお、話者の条件付けに関しては、DeepVoice2の論文 ([arXiv:1705.08947 [cs.CL]](https://arxiv.org/abs/1705.08947)) の方が詳しいです。

まず基本的に、話者の情報は trainable embedding としてモデルに組み込みます。text embeddingのうようにネットワークの入力の一箇所に入れるような設計では学習が上手くかない（話者情報を無視するようになってしまうのだと思います）ため、ネットワークのあらゆるところに入れるのがポイントのようです。具体的には、Encoder, Decoder (+ Attention), Converterのすべてに入れます。さらに具体的には、ネットワークの基本要素である Gated linear unit + Conv1d のすべてに入れます。詳細は論文に記載のarchitectureの図を参照してください。

話者の条件付けに関して、一つ注意を加えるとすれば、本論文には明示的に書かれていませんが、 speaker embeddingは各時間stepすべてにexpandして用いるのだと思います（でないと実装するときに困る）。DeepVoice2の論文にはその旨が明示的に書かれています。

## VCTK の前処理

実験に入る前に、VCTKの前処理について、簡単にまとめたいと思います。VCTKの音声データには、数秒に渡る無音区間がそれなりに入っているので、それを取り除く必要があります。以前、[日本語 End-to-end 音声合成に使えるコーパス JSUT の前処理](/blog/2017/11/12/jsut_ver1/) で書いた内容と同じように、音素アライメントを取って無音区間を除去します。僕は以下の二つの方法をためしました。

- [Gentle](https://github.com/lowerquality/gentle) ([Kaldi](https://github.com/kaldi-asr/kaldi)ベース)
- [Merlin](https://github.com/CSTR-Edinburgh/merlin) 付属のアライメントツール ([festvox](http://festvox.org/cmu_arctic/)ベース) ([便利スクリプト](https://gist.github.com/kastnerkyle/cc0ac48d34860c5bb3f9112f4d9a0300))

論文中には、（無音除去のため、という文脈ではないのですが[^1]）Gentleを使った旨が書かれています。しかし、試したところアライメントが失敗するケースがそれなりにあり、[loop](https://github.com/facebookresearch/loop) は後者の方法を用いており良い結果も出ていることから、結論としては僕は後者を採用しました。なお、両方のコードは残してあるので、気になる方は両方ためしてみてください。

[^1]: VCTKの無音区間除去のためという文脈ではなく、テキストにshort pause / long pause を挿入するためです

## 実験

[VCTK](http://homepages.inf.ed.ac.uk/jyamagis/page3/page58/page58.html) の108話者分のすべて[^2]を使用して、20時間くらい（30万ステップ x 2）学習しました。30万ステップ学習した後できたモデルをベースに、さらに30万ステップ学習しました[^3]。モデルは、単一話者の場合とほとんど同じですが、変更を加えた点を以下にまとめます。

[^2]: transcriptionがない1話者 (p315) のデータは除いています
[^3]: Dropoutをきつくするとロスが下がりにくく、一方でゆるくすると汎化しにくい印象がありました。ので、Dropoutきつめである程度汎化させたあと、Dropoutをゆるめにしてfine turningする、といった戦略を取ってみました。

- **共通**: Speaker embedding を追加しました。
- **共通**: Speaker embeddingをすべての時間ステップにexpandしたあと、Dropoutを適用するようにしました（論文には書いていませんが、結論から言えば重要でした…）
- **Decoder**: アテンションのレイヤー数を2から1に減らしました

計算速度は、バッチサイズ16で、8.6 step/sec くらいでした。GPUメモリの使用量は9GB程度でした。Convolution BlockごとにLinearレイヤーが追加されるので、それなりにメモリ使用量が増えます。PyTorch v0.3.0を使いました。

学習に使用したコマンドは以下です。

```sh
python train.py --data-root=./data/vctk --checkpoint-dir=checkpoints_vctk \
   --hparams="preset=deepvoice3_vctk,builder=deepvoice3_multispeaker" \
   --log-event-path=log/deepvoice3_multispeaker_vctk_preset \
   --load-embedding=20171221_deepvoice3_checkpoint_step000300000.pth
 # << 30万ステップで一旦打ち切り >>
 # もう一度0から30万ステップまで学習しなおし
 python train.py --data-root=./data/vctk --checkpoint-dir=checkpoints_vctk_fineturn \
   --hparams="preset=deepvoice3_vctk,builder=deepvoice3_multispeaker" \
   --log-event-path=log/deepvoice3_multispeaker_vctk_preset_fine \
   --restore-parts=./checkpoints_vctk/checkpont_step000300000.pth
```

学習を高速化するため、LJSpeechで30万ステップ学習したモデルのembeddingの部分を再利用しました。また、cyclic annealingのような効果が得られることを期待して、一度学習を打ち切って、さらに0stepからファインチューニングしてみました。

コードのコミットハッシュは [0421749](https://github.com/r9y9/deepvoice3_pytorch/tree/0421749af908905d181f089f06956fddd0982d47) です。正確なハイパーパラメータが知りたい場合は、ここから辿れると思います。

### アライメントの学習過程 (~30万ステップ)

<div align="center"><img src="/images/deepvoice3_multispeaker/alignments.gif" /></div>

### 学習された Speaker embedding の可視化

<div align="center"><img src="/images/deepvoice3_multispeaker/speaker_embedding.png" /></div>

論文のappendixに書かれているのと同じように、学習されたEmbeddingに対してPCAをかけて可視化しました。論文の図とは少々異なりますが、期待通り、男女はほぼ線形分離できるようになっていることは確認できました。

### 音声サンプル

最初に僕の感想を述べておくと、LJSpeechで単一話者モデルを学習した場合と比べると、汎化しにくい印象がありました。文字がスキップされるといったエラーケースも比較して多いように思いました。
たくさんサンプルを貼るのは大変なので、興味のある方は自分で適当な未知テキストを与えて合成してみてください。学習済みモデルは [deepvoice3_pytorch#pretrained-models](https://github.com/r9y9/deepvoice3_pytorch#pretrained-models) からダウンロードできるようにしてあります。

### [Loop](https://ytaigman.github.io/loop/#network-3-multiple-speakers-from-vctk) と同じ文章

Some have accepted this as a miracle without any physical explanation

 (69 chars, 11 words)

 speaker IDが若い順に12サンプルの話者ID を与えて、合成した結果を貼っておきます。

**225, 23,  F,    English,    Southern,  England** (ID, AGE,  GENDER,  ACCENTS,  REGION)

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/loop/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker0.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**226,  22,  M,    English,    Surrey**

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/loop/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker1.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**227,  38,  M,    English,    Cumbria**

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/loop/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker2.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**228,  22,  F,    English,    Southern  England**

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/loop/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker3.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**229,  23,  F,    English,    Southern  England**

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/loop/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker4.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**230,  22,  F,    English,    Stockton-on-tees**

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/loop/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker5.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**231,  23,  F,    English,    Southern  England**

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/loop/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker6.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**232,  23,  M,    English,    Southern  England**

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/loop/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker7.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**233,  23,  F,    English,    Staffordshire**

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/loop/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker8.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**234,  22,  F,    Scottish,  West  Dumfries**

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/loop/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker9.wav" autoplay/>
Your browser does not support the audio element.
</audio>



**236,  23,  F,    English,    Manchester**

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/loop/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker10.wav" autoplay/>
Your browser does not support the audio element.
</audio>

**237,  22,  M,    Scottish,  Fife**

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/loop/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker11.wav" autoplay/>
Your browser does not support the audio element.
</audio>

声質だけでなく、話速にもバリエーションが出ているのがわかります。`231` の最初で一部音が消えています（こういったエラーケースはよくあります）。

#### [keithito/tacotron のサンプル](https://keithito.github.io/audio-samples/) と同じ文章

簡単に汎化性能をチェックするために、未知文章でテストします。

- 男性 (292,  23,  M,    NorthernIrish,  Belfast)
- 女性 (288,  22,  F,    Irish,  Dublin)

の二つのサンプルを貼っておきます。

Scientists at the CERN laboratory say they have discovered a new particle.

(74 chars, 13 words)

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/3_keithito/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker62.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<div align="center"><img src="/audio/deepvoice3_multispeaker/3_keithito/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker62_alignment.png" /></div>


<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/3_keithito/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker61.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<div align="center"><img src="/audio/deepvoice3_multispeaker/3_keithito/0_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker61_alignment.png" /></div>


There's a way to measure the acute emotional intelligence that has never gone out of style.

(91 chars, 18 words)

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/3_keithito/1_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker62.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<div align="center"><img src="/audio/deepvoice3_multispeaker/3_keithito/1_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker62_alignment.png" /></div>

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/3_keithito/1_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker61.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<div align="center"><img src="/audio/deepvoice3_multispeaker/3_keithito/1_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker61_alignment.png" /></div>


President Trump met with other leaders at the Group of 20 conference.

(69 chars, 13 words)

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/3_keithito/2_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker62.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<div align="center"><img src="/audio/deepvoice3_multispeaker/3_keithito/2_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker62_alignment.png" /></div>

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/3_keithito/2_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker61.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<div align="center"><img src="/audio/deepvoice3_multispeaker/3_keithito/2_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker61_alignment.png" /></div>


The Senate's bill to repeal and replace the Affordable Care Act is now imperiled.

(81 chars, 16 words)

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/3_keithito/3_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker62.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<div align="center"><img src="/audio/deepvoice3_multispeaker/3_keithito/3_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker62_alignment.png" /></div>

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/3_keithito/3_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker61.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<div align="center"><img src="/audio/deepvoice3_multispeaker/3_keithito/3_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker61_alignment.png" /></div>


Generative adversarial network or variational auto-encoder.

(59 chars, 7 words)

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/3_keithito/4_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker62.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<div align="center"><img src="/audio/deepvoice3_multispeaker/3_keithito/4_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker62_alignment.png" /></div>

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/3_keithito/4_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker61.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<div align="center"><img src="/audio/deepvoice3_multispeaker/3_keithito/4_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker61_alignment.png" /></div>


The buses aren't the problem, they actually provide a solution.

(63 chars, 13 words)

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/3_keithito/5_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker62.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<div align="center"><img src="/audio/deepvoice3_multispeaker/3_keithito/5_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker62_alignment.png" /></div>

<audio controls="controls" >
<source src="/audio/deepvoice3_multispeaker/3_keithito/5_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker61.wav" autoplay/>
Your browser does not support the audio element.
</audio>

<div align="center"><img src="/audio/deepvoice3_multispeaker/3_keithito/5_20171222_deepvoice3_vctk108_checkpoint_step000300000_speaker61_alignment.png" /></div>

ところどころ音が抜けているのが目立ちます。色々実験しましたが、やはり単一話者 24hのデータで学習したモデルに比べると、一話者あたり30分~1h程度のデータでは、汎化させるのが難しい印象を持ちました。

## まとめ

- 複数話者版のDeepVoice3を実装して、実際に108話者のデータセットで学習し、それなりに動くことを確認できました
- 複数話者版のDeepVoice3では、アテンションの学習が単一話者の場合と比べて難しい印象でした。アテンションレイヤーの数を2から1に減らすと、アライメントがくっきりする傾向にあることを確認しました。
- VCTKの前処理大事、きちんとしましょう
- Speaker embedding にDropoutをかけるのは、論文には記載されていませんが、結果から言って重要でした。ないと、音声の品質以前の問題として、文字が正しく発音されない、といった現象に遭遇しました。
- Speaker embedding をすべての時刻に同一の値をexpandしてしまうと過学習しやすいのではないかいう予測を元に、各時刻でランダム性をいれることでその問題を緩和できないかと考え、Dropoutを足してみました。上手く言ったように思います
- 論文の内容について詳しく触れていませんが、実はけっこう雑というか、文章と図に不一致があったりします（例えば図1にあるEncoder PreNet/PostNet は文章中で説明がない）。著者に連絡して確認するのが一番良いのですが、どういうモデルなら上手くいくか考えて試行錯誤するのも楽しいので、今回は雰囲気で実装しました。それなりに上手く動いているように思います

次は、DeepVoice3、Tacotron 2 ([arXiv:1712.05884 [cs.CL]](https://arxiv.org/abs/1712.0588)) で有効性が示されている WaveNet Vocoder を実装して、品質を改善してみようと思っています。

## 参考

- [Wei Ping, Kainan Peng, Andrew Gibiansky, et al, "Deep Voice 3: 2000-Speaker Neural Text-to-Speech", arXiv:1710.07654, Oct. 2017.](https://arxiv.org/abs/1710.07654)
- [Sercan Arik, Gregory Diamos, Andrew Gibiansky,, et al, "Deep Voice 2: Multi-Speaker Neural Text-to-Speech", arXiv:1705.08947, May 2017.](https://arxiv.org/abs/1705.08947)
- [Jonathan Shen, Ruoming Pang, Ron J. Weiss, et al, "Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions", arXiv:1712.05884, Dec 2017.](https://arxiv.org/abs/1712.05884)

## 関連記事

- [【単一話者編】Deep Voice 3: 2000-Speaker Neural Text-to-Speech / arXiv:1710.07654 [cs.SD] | LESS IS MORE](/blog/2017/12/13/deepvoice3/)
- [Efficiently Trainable Text-to-Speech System Based on Deep Convolutional Networks with Guided Attention. [arXiv:1710.08969] | LESS IS MORE](/blog/2017/11/23/dctts/)
- [日本語 End-to-end 音声合成に使えるコーパス JSUT の前処理 | LESS IS MORE](/blog/2017/11/12/jsut_ver1/)
