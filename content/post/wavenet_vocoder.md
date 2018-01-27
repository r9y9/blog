+++
date = "2018-01-28T00:14:35+09:00"
draft = false
title = "WaveNet vocoder をやってみましたので、その記録です / WaveNet: A Generative Model for Raw Audio [arXiv:1609.03499]"
tags  = [ "Speech", "DNN", "WaveNet"]
categories = ["Speech synthesis", "Python"]

+++

- コード: https://github.com/r9y9/wavenet_vocoder
- 音声サンプル: https://r9y9.github.io/wavenet_vocoder/

## 三行まとめ

- Local / global conditioning を最低要件と考えて、WaveNet を実装しました
- DeepVoice3 / Tacotron2 の一部として使えることを目標に作りました
- PixelCNN++ の旨味を少し拝借し、16-bit linear PCMのscalarを入力として、（まぁまぁ）良い22.5kHzの音声を生成させるところまでできました

Tacotron2 は、あとはやればほぼできる感じですが、直近では僕の中で優先度が低めのため、しばらく実験をする予定はありません。興味のある方はやってみてください。

## 音声サンプル

左右どちらかが合成音声です^^

<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/0_checkpoint_step000410000_ema_predicted.wav" autoplay/>
Your browser does not support the audio element.
</audio>
<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/0_checkpoint_step000410000_ema_target.wav" autoplay/>
Your browser does not support the audio element.
</audio>


<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/1_checkpoint_step000410000_ema_predicted.wav" autoplay/>
Your browser does not support the audio element.
</audio>
<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/1_checkpoint_step000410000_ema_target.wav" autoplay/>
Your browser does not support the audio element.
</audio>


<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/2_checkpoint_step000410000_ema_predicted.wav" autoplay/>
Your browser does not support the audio element.
</audio>
<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/2_checkpoint_step000410000_ema_target.wav" autoplay/>
Your browser does not support the audio element.
</audio>


<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/3_checkpoint_step000410000_ema_predicted.wav" autoplay/>
Your browser does not support the audio element.
</audio>
<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/3_checkpoint_step000410000_ema_target.wav" autoplay/>
Your browser does not support the audio element.
</audio>


<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/4_checkpoint_step000410000_ema_predicted.wav" autoplay/>
Your browser does not support the audio element.
</audio>
<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/4_checkpoint_step000410000_ema_target.wav" autoplay/>
Your browser does not support the audio element.
</audio>


<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/5_checkpoint_step000410000_ema_predicted.wav" autoplay/>
Your browser does not support the audio element.
</audio>
<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/5_checkpoint_step000410000_ema_target.wav" autoplay/>
Your browser does not support the audio element.
</audio>


<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/6_checkpoint_step000410000_ema_predicted.wav" autoplay/>
Your browser does not support the audio element.
</audio>
<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/6_checkpoint_step000410000_ema_target.wav" autoplay/>
Your browser does not support the audio element.
</audio>


<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/7_checkpoint_step000410000_ema_predicted.wav" autoplay/>
Your browser does not support the audio element.
</audio>
<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/7_checkpoint_step000410000_ema_target.wav" autoplay/>
Your browser does not support the audio element.
</audio>


<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/8_checkpoint_step000410000_ema_predicted.wav" autoplay/>
Your browser does not support the audio element.
</audio>
<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/8_checkpoint_step000410000_ema_target.wav" autoplay/>
Your browser does not support the audio element.
</audio>


<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/9_checkpoint_step000410000_ema_predicted.wav" autoplay/>
Your browser does not support the audio element.
</audio>
<audio controls="controls" >
<source src="/audio/wavenet_vocoder/mixture_lj/9_checkpoint_step000410000_ema_target.wav" autoplay/>
Your browser does not support the audio element.
</audio>


## 自分で書いた背景

WaveNetが発表されたのは、一年以上前 ([記事](https://deepmind.com/blog/wavenet-generative-model-raw-audio/)) のことです。発表後すぐに、いくつかオープンソースの実装が出ていたように記憶しています。
一方で、僕が確認していた限りでは、local / global conditioningを十分にサポートした実装がなかったように思います。
例えば、Githubで一番スターが付いている [ibab/tensorflow-wavenet](https://github.com/ibab/tensorflow-wavene) では、いまだに十分にサポートされていません（[#112](https://github.com/ibab/tensorflow-wavenet/issues/112)）。
これはつまり、生成モデルとしては使えても、TTSには使えない、ということで、僕の要望を満たしてくれるものではありませんでした。また、ちょうど最近、Parallel WaveNetが発表されたのもあり、勉強も兼ねて、local / global conditioningを最低要件として置いて、自分で実装してみようと思った次第です。

実装を通して僕が一番知りたかった（体感したかった）のは、WaveNetで本当に自然音声並みの品質の音声を生成できるのか？ということなので、Parallel WaveNetで提案されているような推論を高速化するための工夫に関しては手を付けていませんので、あしからず。

## 実験を通して得た知見

- Dropoutの有無については、WaveNetの論文に書いていませんが、僕は5%をゼロにする形で使いました。問題なく動いていそうです。PixelCNN++にはDropoutを使う旨が書かれていたので、WaveNetでも使われているのかなと推測しています。
- Gradient clippingの有無は、両方試しましたが、なくてもあっても学習は安定していました。
- Mixture of logistic distributionsを使う場合は、分散の下限を小さくするのが重要な気がしました (PixelCNN++でいう[pixel_cnn_pp/nn.py#L54](https://github.com/openai/pixel-cnn/blob/2b03725126c580a07af47c498d456cec17a9735e/pixel_cnn_pp/nn.py#L54) の部分)。でないと、生成される音声がノイジーになりやすい印象を受けました。直感的には、external featureで条件付けする場合は特に、logistic distributionがかなりピーキー（分散がすごく小さく）なり得るので、そのピーキーな分布を十分表現できる必要があるのかなと思っています。生成時には確率分布からサンプリングすることになるので、分散の下限値を大きくとってしまった場合、ノイジーになりえるのは想像がつきます。 ref: [r9y9/wavenet_vocoder/#7](https://github.com/r9y9/wavenet_vocoder/issues/7#issuecomment-360011074)
- WaveNetの実装は（比較的）簡単だったので、人のコード読むのツライ…という方は、（僕のコードを再利用なんてせずに）自分で実装するのも良いかなと思いました。勉強にもなりました。
- WaveNetが発表された当時は、個人レベルの計算環境でやるのは無理なんじゃないかと思って手を出していなかったのですが、最近はそれが疑問に思えてきたので、実際にやってみました。僕のPCには1台しかGPUがついていませんが、個人でも可能だと示せたかと思います。
- 実験をはじめた当初、バッチサイズ1でもGPUメモリ (12GB) を使いきってしまう…とつらまっていたのですが、Parallel WaveNetの論文でも言及されている通り、音声の一部を短く（7680サンプルとか）切り取って使っても、品質には影響しなさそうなことを確認しました。参考までに、この記事に貼ったサンプルは、バッチサイズ2、一音声あたりの長さ8000に制限して、実験して得たものです。学習時間は、パラメータを変えながら重ね重ねファインチューニングしていたので正確なことは言えないのですが、トータルでいえば10日くらい学習したかもしれません。ただ、1日くらいで、それなりにまともな音声はでます。

## おわりに

- WaveNetのすごさを実際に体感することができました。まだやりたいことは残っていますが、僕はそこそこ満足しました。
- 今後のTODO及び過去/現在の進捗は、 [r9y9/wavenet_vocoder/#1](https://github.com/r9y9/wavenet_vocoder/issues/1) にまとめています。海外の方との議論も見つかるので、興味のある方は見てください。
- 実装をはじめた当初からコードを公開していたのですが、どうやら興味を持った方が複数いたようで、上記issueにて有益なコメントをたくさんもらいました。感謝感謝

## 参考にした論文

- [Aaron van den Oord, Sander Dieleman, Heiga Zen, et al, "WaveNet: A Generative Model for Raw Audio", arXiv:1609.03499, Sep 2016.](https://arxiv.org/abs/1609.03499)
- [Aaron van den Oord, Yazhe Li, Igor Babuschkin, et al, "Parallel WaveNet: Fast High-Fidelity Speech Synthesis", arXiv:1711.10433, Nov 2017.](https://arxiv.org/abs/1711.10433)
- [Tamamori, Akira, et al. "Speaker-dependent WaveNet vocoder." Proceedings of Interspeech. 2017.](http://www.isca-speech.org/archive/Interspeech_2017/pdfs/0314.PDF)
- [Jonathan Shen, Ruoming Pang, Ron J. Weiss, et al, "Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions", arXiv:1712.05884, Dec 2017.](https://arxiv.org/abs/1712.05884)
- [Wei Ping, Kainan Peng, Andrew Gibiansky, et al, "Deep Voice 3: 2000-Speaker Neural Text-to-Speech", arXiv:1710.07654, Oct. 2017.](https://arxiv.org/abs/1710.07654)
- [Tim Salimans, Andrej Karpathy, Xi Chen, Diederik P. Kingma, "PixelCNN++: Improving the PixelCNN with Discretized Logistic Mixture Likelihood and Other Modifications", arXiv:1701.05517, Jan. 2017.](https://arxiv.org/abs/1701.05517)

## 参考になったコード

- [tensorflow/magenta/nsynth/wavenet](https://github.com/tensorflow/magenta/tree/master/magenta/models/nsynth/wavenet)
- [musyoku/wavenet](https://github.com/musyoku/wavenet) コードはもちろん、こちら [#4](https://github.com/musyoku/wavenet/issues/4)  のイシューも役に立ちました。
- [ibab/tensorflow-wavenet](https://github.com/ibab/tensorflow-wavenet)
- [openai/pixel-cnn](https://github.com/openai/pixel-cnn) PixelCNN++の公式実装です
- [pclucas14/pixel-cnn-pp](https://github.com/pclucas14/pixel-cnn-pp) PixelCNN++のPyTorch実装です

## 参考になりそうなコード

※僕は参考にしませんでしたが、役に立つかもしれません

- https://github.com/kan-bayashi/PytorchWaveNetVocoder
- https://github.com/tomlepaine/fast-wavenet
- https://github.com/vincentherrmann/pytorch-wavenet
- https://github.com/dhpollack/fast-wavenet.pytorch
