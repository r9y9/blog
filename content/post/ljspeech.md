---
title: "LJSpeech は価値のあるデータセットですが、ニューラルボコーダの品質比較には向かないと思います"
date: 2019-06-11T00:00:30+09:00
draft: false
tag: [ "Speech", "DNN", "LJSpeech"]
categories: ["Speech synthesis"]
---

- LJSpeech Dataset: https://keithito.com/LJ-Speech-Dataset/

## まとめ

最近いろんな研究で [LJSpeech](https://keithito.com/LJ-Speech-Dataset/) が使われていますが、合成音の品質を比べるならクリーンなデータセットを使ったほうがいいですね。でないと、合成音声に含まれるノイズがモデルの限界からくるノイズなのかコーパスの音声が含むノイズ（LJSpeechの場合リバーブっぽい音）なのか区別できなくて、公平に比較するのが難しいと思います。

例えば、LJSpeechを使うと、ぶっちゃけ [WaveGlow](https://nv-adlr.github.io/WaveGlow) がWaveNetと比べて品質がいいかどうかわかんないですよね…[^1].
例えば最近のNICT岡本さんの研究 ([基本周波数とメルケプストラムを用いたリアルタイムニューラルボコーダに関する検討]( https://www.slideshare.net/Takuma_OKAMOTO/ss-135604814)) を引用すると、実際にクリーンなデータで実験すれば（Noise shaping なしで）MOS は WaveNet (**4.19**) > WaveGlow (3.27) と、結構な差が出たりします。LJSpeechを使った場合の WaveGlow (**3.961**) > WaveNet (3.885) と比べると大きな差ですね。

[^1]: 僕の実装 をbest publicly availableWaveNet implementation として比較に使っていただいて恐縮ですが…。

とはいえ、End-to-end音声合成を試すにはとてもいいデータセットであると思うので、積極的に活用しましょう。最近 [LibriTTS](https://arxiv.org/abs/1904.02882) が公開されたので、そちらも合わせてチェックするといいですね。

## Why LJSpeech

[LJSpeech](https://keithito.com/LJ-Speech-Dataset/) は、[keithito](https://keithito.com/) さんによって2017年に公開された、単一女性話者によって録音された24時間程度の英語音声コーパスです。なぜ近年よく使われて始めているのかと言うと（2019年6月時点で[Google scholarで27件の引用](https://scholar.google.co.jp/scholar?cites=8632543993730273058)）、End-to-end 音声合成の研究に用いるデータセットとして、LJSpeechは最もといっていいほど手軽に手に入るからだと考えています。LJSpeech は public domainで配布されており、利用に制限もありませんし、企業、教育機関、個人など様々な立場から自由に使用することができます。End-to-end 音声合成（厳密にはseq2seq モデルの学習）は一般に大量のデータが必要なことが知られていますが、その要件も満たしていることから、特にEnd-to-end音声合成の研究で用いられている印象を受けます。最近だと、[FastSpeech: Fast, Robust and Controllable Text to Speech](https://speechresearch.github.io/fastspeech/) にも使われていましたね。


## 個人的な経験

個人的には、過去に以下のブログ記事の内容で使用してきました。

- [Tacotron: Towards End-to-End Speech Synthesis / arXiv:1703.10135 [cs.CL]](https://r9y9.github.io/blog/2017/10/15/tacotron/)
- [【単一話者編】Deep Voice 3: 2000-Speaker Neural Text-to-Speech / arXiv:1710.07654 [cs.SD]](https://r9y9.github.io/blog/2017/12/13/deepvoice3/)
- [【108 話者編】Deep Voice 3: 2000-Speaker Neural Text-to-Speech / arXiv:1710.07654 [cs.SD]](https://r9y9.github.io/blog/2017/12/22/deepvoice3_multispeaker/)
- [Efficiently Trainable Text-to-Speech System Based on Deep Convolutional Networks with Guided Attention. [arXiv:1710.08969]](https://r9y9.github.io/blog/2017/11/23/dctts/)
- [WaveNet vocoder をやってみましたので、その記録です / WaveNet: A Generative Model for Raw Audio [arXiv:1609.03499]](https://r9y9.github.io/blog/2018/01/28/wavenet_vocoder/)
- [WN-based TTSやりました / Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions [arXiv:1712.05884]](https://r9y9.github.io/blog/2018/05/20/tacotron2/)

この記事を書くにあたって整理してみて、ずいぶんとたくさんお世話になっていることが改めてわかりました。keithitoさん本当にありがとうございます。

2017年、僕がTacotronで遊び始めた当時、End-to-end音声合成が流行ってきていたのですが、フリーで手に入って、End-to-end 音声合成にも使えるような程々に大きな（> 20時間）コーパスって、あんまりなかったんですよね。今でこそ [M-AILABS](https://www.caito.de/2019/01/the-m-ailabs-speech-dataset/) 、[LibriTTS](https://arxiv.org/abs/1904.02882)、日本語なら [JSUT](https://sites.google.com/site/shinnosuketakamichi/publication/jsut) もありますが、当時は選択肢は少なかったと記憶しています。今はいい時代になってきていますね。

## 最後に

久しぶりに短いですがブログを書きました。LJSpeechは良いデータセットですので、積極的に活用しましょう。ただ、データセットの特徴として、録音データが若干リバーブがかかったような音になっていることから、ニューラルボコーダの品質比較には（例えば WaveGlow vs WaveNet）あんまり向かないかなと思っています。

2017年に、End-to-end音声合成を気軽に試そうと思った時にはLJSpeechは最有力候補でしたが、現在は他にもいろいろ選択肢がある気がします。以下、僕がぱっと思いつくものをまとめておきますので、参考までにどうぞ。

## End-to-end音声合成に使える手軽に手に入るデータセット

- LJSpeech Dataset: https://keithito.com/LJ-Speech-Dataset/
- LibriTTS: https://arxiv.org/abs/1904.02882
- JSUT: https://sites.google.com/site/shinnosuketakamichi/publication/jsut
- M-AILABS: https://www.caito.de/2019/01/the-m-ailabs-speech-dataset/
- VCTK: https://homepages.inf.ed.ac.uk/jyamagis/page3/page58/page58.html

## 参考

- WaveNet: https://deepmind.com/blog/wavenet-generative-model-raw-audio/
- WaveGlow: https://nv-adlr.github.io/WaveGlow
- FastSpeech: https://speechresearch.github.io/fastspeech/
- 岡本拓磨，戸田智基，志賀芳則，河井恒，"基本周波数とメルケプストラムを用いたリアルタイムニューラルボコーダに関する検討"，日本音響学会講演論文集，2019年春季, pp. 1057–1060, Mar. 2019. [slides](https://www.slideshare.net/Takuma_OKAMOTO/ss-135604814)
