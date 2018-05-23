+++
date = "2018-05-20T14:21:30+09:00"
draft = false
title = " WN-based TTSやりました / Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions [arXiv:1712.05884]"
tags  = [ "Speech", "DNN", "WaveNet"]
categories = ["Speech synthesis", "Python"]
+++

Thank you for coming to see my blog post about WaveNet text-to-speech.

<audio controls="controls" >
<source src="/audio/tacotron2/intro.wav" autoplay/>
Your browser does not support the audio element.
</audio>

- 論文リンク: https://arxiv.org/abs/1712.05884
- オンラインデモ: [Tacotron2: WaveNet-based text-to-speech demo](https://colab.research.google.com/github/r9y9/Colaboratory/blob/master/Tacotron2_and_WaveNet_text_to_speech_demo.ipynb)
- コード [r9y9/wavenet_vocoder](https://github.com/r9y9/wavenet_vocoder), [Rayhane-mamah/Tacotron-2](https://github.com/Rayhane-mamah/Tacotron-2)
- 音声サンプル: https://r9y9.github.io/wavenet_vocoder/

## 三行まとめ

- 自作WaveNet (**WN**) と既存実装Tacotron 2 (WNを除く) を組み合わせて、英語TTSを作りました
- LJSpeechを学習データとした場合、自分史上 **最高品質** のTTSができたと思います
- Tacotron 2と Deep Voice 3 のabstractを読ませた音声サンプルを貼っておきますので、興味のある方はどうぞ

なお、Tacotron 2 の解説はしません。申し訳ありません（なぜなら僕がまだ十分に読み込んでいないため）

## 背景

過去に、WaveNetを実装しました（参考: [WaveNet vocoder をやってみましたので、その記録です / WaveNet: A Generative Model for Raw Audio [arXiv:1609.03499]](/blog/2018/01/28/wavenet_vocoder/)）。過去記事から引用します。

> Tacotron2 は、あとはやればほぼできる感じですが、直近では僕の中で優先度が低めのため、しばらく実験をする予定はありません。興味のある方はやってみてください。

やりたいことの一つとしてあったとはいえ、当初の予定通り、スクラッチでTacotron 2を実装する時間は取れなかったのですが、既存実装を使ってみたところ十分に上手く動いているように思えたので、ありがたく使わせていただき、WaveNet TTSを実現することができました。というわけで、結果をここにカジュアルに残しておこうという趣旨の記事になります。

オープンなデータセット、コードを使って、実際どの程度の品質が得られるのか？学習/推論にどのくらい時間がかかるのか？いうのが気になる方には、参考になるかもしれませんので、よろしければ続きをどうぞ。

## 実験条件

細かい内容はコードに譲るとして、重要な点だけリストアップします

### Pre-trained models、hyper parameters へのリンク

- Tacotron2 (mel-spectrogram prediction part): trained 189k steps on LJSpeech dataset ([Pre-trained model](https://www.dropbox.com/s/vx7y4qqs732sqgg/pretrained.tar.gz?dl=0), [Hyper params](https://github.com/r9y9/Tacotron-2/blob/9ce1a0e65b9217cdc19599c192c5cd68b4cece5b/hparams.py)).
- WaveNet: trained over 1000k steps on LJSpeech dataset ([Pre-trained model](https://www.dropbox.com/s/zdbfprugbagfp2w/20180510_mixture_lj_checkpoint_step000320000_ema.pth?dl=0), [Hyper params](https://www.dropbox.com/s/0vsd7973w20eskz/20180510_mixture_lj_checkpoint_step000320000_ema.json?dl=0))

### WaveNet

- 1000k step以上訓練されたモデル (2018/1/27に作ったもの、10日くらい[^1]学習した）をベースに、さらに 320k step学習（約3日）しました。再学習したのは、以前のコードには [wavenet_vocoder/issues/33](https://github.com/r9y9/wavenet_vocoder/issues/33) こんなバグがあったからです。
- 評価には、exponential moving averagingされたパラメータを使いました。decay パラメータはTaco2論文と同じ 0.9999
- 学習には、Mel-spectrogram prediction networkにより出力される Ground-truth-aligned (GTA) なメルスペクトログラムではなく、生音声から計算されるメルスペクトログラムを使いました。時間の都合上そうしましたが、GTAを使うとより品質が向上すると考えられます

### Tacotron 2 (mel-spectrogram prediction)

- https://github.com/Rayhane-mamah/Tacotron-2 にはWaveNet実装も含まれていますが、mel-spectrogram prediction の部分だけ使用しました[^2]
- https://github.com/Rayhane-mamah/Tacotron-2/issues/30#issue-317360759 で公開されている 182k step学習されたモデルを、さらに7k stepほど（数時間くらい）学習させました。再学習させた理由は、自分の実装とRayhane氏の実装で想定するメルスペクトログラムのレンジが異なっていたためです（僕: `[0, 1]`, Rayhane: `[-4, 4]`）。そういう経緯から、`[-4, 4]` のレンジであったところ，`[0, 4]` にして学習しなおしました。直接 `[0, 1]` にして学習しなかったのは（それでも動く、と僕は思っているのですが）、mel-spectrogram のレンジを大きく取った方が良い、という報告がいくつかあったからです（例えば https://github.com/Rayhane-mamah/Tacotron-2/issues/4#issuecomment-377728945 )。Attention seq2seq は経験上学習が難しいので、僕の直感よりも先人の知恵を優先することにした次第です。WNに入力するときには、 Taco2が出力するメルスペクトログラムを `c = np.interp(c, (0, 4), (0, 1))` とレンジを変換して与えました

[^1]: 曖昧な表現で申し訳ございません
[^2]: 僕が使った当時は、WNの部分は十分にテストされていなかったのと、WNのコードは僕のコードをtfにtranslateした感じな（著者がそういってます）ので、WNは自分の実装を使った次第です

## デモ音声

https://r9y9.github.io/wavenet_vocoder/ にサンプルはたくさんあります。が、ここでは違うサンプルをと思い、Tacotron 2 と Deep Voice 3の abstract を読ませてみました。
学習データに若干残響が乗っているので（ノイズっぽい）それが反映されてしまっているのですが、個人的にはまぁまぁよい結果が得られたと思っています。興味がある方は、DeepVoice3など僕の過去記事で触れているTTS結果と比べてみてください。

なお、推論の計算速度は,、僕のローカル環境（GTX 1080Ti, i7-7700K）でざっと 170 timesteps / second といった感じでした。これは、Parallel WaveNet の論文で触れられている数字とおおまかに一致します。

This paper describes Tacotron 2, a neural network architecture for speech synthesis directly from text.

<audio controls="controls" >
<source src="/audio/tacotron2/20180510_mixture_lj_checkpoint_step000320000_ema_speech-mel-00001.wav" autoplay/>
Your browser does not support the audio element.
</audio>


The system is composed of a recurrent sequence-to-sequence feature prediction network that maps character embeddings to mel-scale spectrograms, followed by a modified WaveNet model acting as a vocoder to synthesize timedomain waveforms from those spectrograms.

<audio controls="controls" >
<source src="/audio/tacotron2/20180510_mixture_lj_checkpoint_step000320000_ema_speech-mel-00002.wav" autoplay/>
Your browser does not support the audio element.
</audio>


Our model achieves a mean opinion score of 4.53 comparable to a MOS of 4.58 for professionally recorded speech.

<audio controls="controls" >
<source src="/audio/tacotron2/20180510_mixture_lj_checkpoint_step000320000_ema_speech-mel-00003.wav" autoplay/>
Your browser does not support the audio element.
</audio>


To validate our design choices, we present ablation studies of key components of our system and evaluate the impact of using mel spectrograms as the input to WaveNet instead of linguistic, duration, and F0 features.

<audio controls="controls" >
<source src="/audio/tacotron2/20180510_mixture_lj_checkpoint_step000320000_ema_speech-mel-00004.wav" autoplay/>
Your browser does not support the audio element.
</audio>


We further demonstrate that using a compact acoustic intermediate representation enables significant simplification of the WaveNet architecture.

<audio controls="controls" >
<source src="/audio/tacotron2/20180510_mixture_lj_checkpoint_step000320000_ema_speech-mel-00005.wav" autoplay/>
Your browser does not support the audio element.
</audio>


We present Deep Voice 3, a fully-convolutional attention-based neural text-to-speech system.

<audio controls="controls" >
<source src="/audio/tacotron2/20180510_mixture_lj_checkpoint_step000320000_ema_speech-mel-00006.wav" autoplay/>
Your browser does not support the audio element.
</audio>


Deep Voice 3 matches state-of-the-art neural speech synthesis systems in naturalness while training ten times faster.

<audio controls="controls" >
<source src="/audio/tacotron2/20180510_mixture_lj_checkpoint_step000320000_ema_speech-mel-00007.wav" autoplay/>
Your browser does not support the audio element.
</audio>


We scale Deep Voice 3 to data set sizes unprecedented for TTS, training on more than eight hundred hours of audio from over two thousand speakers.

<audio controls="controls" >
<source src="/audio/tacotron2/20180510_mixture_lj_checkpoint_step000320000_ema_speech-mel-00008.wav" autoplay/>
Your browser does not support the audio element.
</audio>


In addition, we identify common error modes of attention-based speech synthesis networks, demonstrate how to mitigate them, and compare several different waveform synthesis methods.

<audio controls="controls" >
<source src="/audio/tacotron2/20180510_mixture_lj_checkpoint_step000320000_ema_speech-mel-00009.wav" autoplay/>
Your browser does not support the audio element.
</audio>


We also describe how to scale inference to ten million queries per day on one single-GPU server.

<audio controls="controls" >
<source src="/audio/tacotron2/20180510_mixture_lj_checkpoint_step000320000_ema_speech-mel-00010.wav" autoplay/>
Your browser does not support the audio element.
</audio>

## オンラインデモ

[Tacotron2: WaveNet-based text-to-speech demo](https://colab.research.google.com/github/r9y9/Colaboratory/blob/master/Tacotron2_and_WaveNet_text_to_speech_demo.ipynb)

Google Colabで動かせるようにデモノートブックを作りました。環境構築が不要なので、手軽にお試しできるかと思います。

## 雑記

- WaveNetを学習するときに、Mel-spectrogram precition networkのGTAな出力でなく、生メルスペクトログラムをそのまま使っても品質の良い音声合成ができるのは個人的に驚きでした。これはつまり、Taco2が　(non teacher-forcingな条件で) 十分良いメルスペクトログラムを予測できている、ということなのだと思います。
- 収束性を向上させるために、出力を127.5 倍するとよい、という件ですが、僕はやっていません。なぜなら、僕がまだこの方法の妥当性を理解できていないからです。[@\_\_dhgrs\_\_さんの報告](https://twitter.com/__dhgrs__/status/995962302896599040) によると、やはり有効に働くようですね…
- これまた [@\_\_dhgrs\_\_さんのブログ記事](http://www.monthly-hack.com/entry/2018/02/23/203208) にも書かれていますが、Mixture of Logistic distributions (MoLとします) を使った場合は、categoricalを考えてsoftmaxを使う場合に比べると十分な品質を得るのに大幅に計算時間が必要になりますね、、体験的には10倍程度です。計算にあまりに時間がかかるので、スクラッチで何度も学習するのは厳しく、学習済みモデルを何度も繰り返しfine turningしていくという、秘伝のタレ方式で学習を行いました（再現性なしです、懺悔）
- https://github.com/Rayhane-mamah/Tacotron-2 今回使わせてもらったTaco2実装は、僕の実装も一部使われているようでした。これとは別の NVIDIA から出た https://github.com/NVIDIA/tacotron2 の謝辞には僕の名前を入れていただいていたり、他にもそういうケースがそれなりにあって、端的にいって光栄であり、うれしいお思いです。
- 非公開のデータセットを使って学習/生成したWaveNet TTS のサンプルもあります。公開できないのでここにはあげていませんが、とても高品質な音声合成（主観ですが）ができることを確認しています
- このプロジェクトをはじめたことで、なんと光栄にも[NICT](http://www.nict.go.jp/)でのトークの機会をもらうことができました。オープソースについて是非はあると思いますが、個人的には良いことがとても多いなと思います。プレゼン資料は、https://github.com/r9y9/wavenet_vocoder/issues/57 に置いてあります（が、スライドだけで読み物として成立するものではないと思います、すみません）

## おわりに

WaveNet TTSをようやく作ることができました。Sample-levelでautoregressive modelを考えるというアプローチが本当に動かくのか疑問だったのですが、実際に作ってみて、上手く行くということを体感することができました。めでたし。

Googleの研究者さま、素晴らしい研究をありがとうございます。WaveNetは本当にすごかった

## 参考

- [Aaron van den Oord, Sander Dieleman, Heiga Zen, et al, "WaveNet: A Generative Model for Raw Audio", 	arXiv:1609.03499, Sep 2016.](https://arxiv.org/abs/1609.03499)
- [Aaron van den Oord, Yazhe Li, Igor Babuschkin, et al, "Parallel WaveNet: Fast High-Fidelity Speech Synthesis", 	arXiv:1711.10433, Nov 2017.](https://arxiv.org/abs/1711.10433)
- [Tamamori, Akira, et al. "Speaker-dependent WaveNet vocoder." Proceedings of Interspeech. 2017.](http://www.isca-speech.org/archive/Interspeech_2017/pdfs/0314.PDF)
- [Jonathan Shen, Ruoming Pang, Ron J. Weiss, et al, "Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions", arXiv:1712.05884, Dec 2017.](https://arxiv.org/abs/1712.05884)
- [Wei Ping, Kainan Peng, Andrew Gibiansky, et al, "Deep Voice 3: 2000-Speaker Neural Text-to-Speech", arXiv:1710.07654, Oct. 2017.](https://arxiv.org/abs/1710.07654)
- [Tom Le Paine, Pooya Khorrami, Shiyu Chang, et al, "Fast Wavenet Generation Algorithm", arXiv:1611.09482, Nov. 2016](https://arxiv.org/abs/1611.09482)
- [VQ-VAEの追試で得たWaveNetのノウハウをまとめてみた。 - Monthly Hacker's Blog](http://www.monthly-hack.com/entry/2018/02/23/203208)
