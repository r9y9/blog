---
layout: post
title: 統計的声質変換クッソムズすぎワロタ
date: 2014-07-05
comments: true
categories: voice-conversion, machine-learning, speech-signal-processing
---

## 2014/10/12 追記 

少なくともGVのコードに致命的なバグがあったことがわかりました。よって、あまりあてにしないでください…（ごめんなさい


こんにちは。

最近、統計的声質変換の勉強をしていました。で、メジャーなGMM（混合ガウスモデル）ベースの変換を色々やってみたので、ちょろっと書きます。実は（というほどでもない?）シンプルなGMMベースの方法だと音質クッソ悪くなってしまうんですが、色々試してやっとまともに聞ける音質になったので、試行錯誤の形跡を残しておくとともに、音声サンプルを貼っておきます。ガチ勢の方はゆるりと見守ってください

基本的に、以下の論文を参考にしています

- [T. Toda, A. W. Black, and K. Tokuda, “Voice conversion based on maximum likelihood estimation of spectral parameter trajectory,” IEEE Trans. Audio, Speech, Lang. Process, vol. 15, no. 8, pp. 2222–2235, Nov. 2007](http://isw3.naist.jp/~tomoki/Tomoki/Journals/IEEE-Nov-2007_MLVC.pdf).

## GMMベースの声質変換の基本

シンプルなGMMベースの声質変換は大きく二つのフェーズに分けられます。

- 参照話者と目標話者のスペクトル特徴量の結合GMM $P(x,y)$を学習する
- 入力$x$が与えらたとき、$P(y|x)$が最大となるようにスペクトル特徴量を変換する

あらかじめ話者間の関係をデータから学習しておくことで、未知の入力が来た時にも変換が可能になるわけです。

具体的な変換プロセスとしては、音声を

- 基本周波数
- 非周期性成分
- スペクトル包絡

の3つに分解し、スペクトル包絡の部分（≒声質を表す特徴量）に対して変換を行い、最後に波形を再合成するといった方法がよく用いられます。基本周波数や非周期性成分も変換することがありますが、ここではとりあえず扱いません

シンプルな方法では、フレームごとに独立に変換を行います。

GMMベースのポイントは、東大の齋藤先生の以下のツイートを引用しておきます。

<blockquote class="twitter-tweet" lang="en"><p><a href="https://twitter.com/shurabaP">@shurabaP</a> GMMベースの声質変換の肝は、入力xが与えられた時の出力yの条件付き確率P(y|x) が最大になるようにyを選ぶという確率的な考えです。私のショボい自作スクリプトですが、HTKを使ったGMMの学習レシピは研究室内部用に作ってあるので、もし必要なら公開しますよ。</p>&mdash; Daisuke Saito (@dsk_saito) <a href="https://twitter.com/dsk_saito/statuses/48442052534472706">March 17, 2011</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

ちなみに僕はscipy.mixture.GMMを使いました。HTKヤダー

## やってみる

さて、実際にやってみます。データベースには、[CMU_ARCTIC speech synthesis databases](ht
tp://www.festvox.org/cmu_arctic/)を使います。今回は、女性話者の二人を使いました。

音声の分析合成には、[WORLD](http://ml.cs.yamanashi.ac.jp/world/)を使います。WORLDで求めたスペクトル包絡からメルケプストラム（今回は32次元）に変換したものを特徴量として使いました。

学習では、学習サンプル10641フレーム（23フレーズ）、GMMの混合数64、full-covarianceで学習しました。

### 変換元となる話者（参照話者）
<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/157362625&amp;color=ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false"></iframe>

### 変換対象となる話者（目標話者）
<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/157362613&amp;color=ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false"></iframe>

### GMMベースのframe-by-frameな声質変換の結果

<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/157371966&amp;color=ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false"></iframe>

はぁー、正直聞けたもんじゃないですね。声質は目標話者に近づいている感がありますが、何分音質が悪い。学習条件を色々変えて試行錯誤しましたけどダメでした

## GMMベースの声質変換の弱点

さて、なぜダメかを考えます。もう考えつくされてる感あるけど、大事なところだけ整理します

### フレーム毎に独立な変換処理

まず、音声が時間的に独立なわけないですよね。フレームごとに独立に変換すると、時間的に不連続な点が出てきてしまいます。その結果、ちょっとノイジーな音声になってしまったのではないかと考えられます。

これに対する解決法としては、戸田先生の論文にあるように、動的特徴量も併せてGMMを学習して、系列全体の確率が最大となるように変換を考えるトラジェクトリベースのパラメータ生成方法があります。[^1]

[^1]: ただ、これはトラジェクトリベースのパラメータ生成法の提案であって、トラジェクトリモデル自体を学習してるわけではないんだよなー。普通に考えると学習もトラジェクトリで考える方法があっていい気がするが、 <del>まだ見てないですね。</del> ありました。追記参照

さて、やってみます。参照音声、目標音声は↑で使ったサンプルと同じです。

### トラジェクトリベースの声質変換の結果

<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/157371969&amp;color=ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false"></iframe>

あんま変わらないですね。計算量めっちゃ食うのに、本当につらい。実装が間違ってる可能性もあるけど…

他の方法を考えるとするならば、まぁいっぱいあると思うんですが、スペクトル包絡なんて時間的に不連続にコロコロ変わるようなもんでもない気がするので、確率モデルとしてそういう依存関係を考慮した声質変換があってもいいもんですけどね。あんま見てない気がします。

ちょっと調べたら見つかったもの↓

- [Kim, E.K., Lee, S., Oh, Y.-H. (1997). "Hidden Markov Model Based Voice Conversion Using Dynamic Characteristics of Speaker", Proc. of Eurospeech’97, Rhodes, Greece, pp. 2519-2522.](http://koasas.kaist.ac.kr/bitstream/10203/17632/1/25.pdf)

### 過剰な平滑化

これはGMMに限った話ではないですが、GMMベースのFrame-by-Frameな声質変換の場合でいえば、変換後の特徴量は条件付き期待値を取ることになるので、まぁ常識的に考えて平滑化されますよね。

これに対する解法としては、GV（Global Variance）を考慮する方法があります。これは戸田先生が提案されたものですね。

さて、やってみます。wktk

### GVを考慮したトラジェクトリベースの声質変換の結果

<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/157371971&amp;color=ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false"></iframe>

多少ましになった気もしなくもないけど、やっぱり音質はいまいちですね。そして計算量は激マシします。本当につらい。学会で聞いたGVありの音声はもっと改善してた気がするんだけどなー音声合成の話だけど。僕の実装が間違ってるんですかね…

## ムズすぎわろた

以上、いくつか試しましたが、統計的声質変換は激ムズだということがわかりました。え、ここで終わるの？という感じですが、最後に一つ別の手法を紹介します。

## 差分スペクトル補正に基づく統計的声質変換

これまでは、音声を基本周波数、非周期性成分、スペクトル包絡に分解して、スペクトル包絡を表す特徴量を変換し、変換後の特徴量を元に波形を再合成していました。ただ、よくよく考えると、そもそも基本周波数、非周期性成分をいじる必要がない場合であれば、わざわざ分解して再合成する必要なくね？声質の部分のみ変換するようなフィルタかけてやればよくね？という考えが生まれます。実は、そういったアイデアに基づく素晴らしい手法があります。それが、差分スペクトル補正に基づく声質変換です。

詳細は、以下の予稿をどうぞ

[小林 和弘, 戸田 智基, Graham Neubig, Sakriani Sakti, 中村 哲. "差分スペクトル補正に基づく統計的歌声声質変換", 日本音響学会2014年春季研究発表会(ASJ). 東京. 2014年3月.](http://www.phontron.com/paper/kobayashi14asj.pdf)

では、やってみます。歌声ではなく話し声ですが。他の声質変換の結果とも聴き比べてみてください。

### 差分スペクトル補正に基づく声質変換の結果

<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/157362603&amp;color=ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false"></iframe>

かなり音声の自然性は上がりましたね。これはヘタすると騙されるレベル。本当に素晴らしいです。しかも簡単にできるので、お勧めです。↑のは、GMMに基づくframe-by-frameな変換です。計算量も軽いので、リアルタイムでもいけますね。

## おわりに

声質変換であれこれ試行錯誤して、ようやくスタートラインにたてた感があります。今後は新しい方法を考えようかなーと思ってます。

おわり

## おわび

<blockquote class="twitter-tweet" lang="en"><p>お盆の間に学習ベースの声質変換のプログラム書く（宿題） <a href="https://twitter.com/hashtag/%E5%AE%A3%E8%A8%80?src=hash">#宣言</a></p>&mdash; 山本りゅういち (@r9y9) <a href="https://twitter.com/r9y9/statuses/366928228465655808">August 12, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

約1年かかりました……。本当に申し訳ありませんでした(´･_･`) 

## 追記

Twitterで教えてもらいました。トラジェクトリベースで学習も変換も行う研究もありました

<blockquote class="twitter-tweet" lang="en"><p><a href="https://twitter.com/r9y9">@r9y9</a> つ トラジェクトリＧＭＭな特徴量変換 <a href="http://t.co/kUn7bp9EUt">http://t.co/kUn7bp9EUt</a></p>&mdash; 縄文人（妖精系研究者なのです） (@dicekicker) <a href="https://twitter.com/dicekicker/statuses/485376823308455936">July 5, 2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
