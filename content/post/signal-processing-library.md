---
layout: post
title: "簡単、フリーで使える音声/音楽信号処理ライブラリが作りたい"
date: 2013-10-15
comments: true
categories: daily speech-signal-processing music-signal-processing
---

音声を使ったアプリケーションが作りたい、例えば自分の声を誰かの声に変えたい、自動で音痴補正したい、関西弁のゆっくりちゃん作りたい、ギターエフェクト作りたい、とか思う人も少なくないんじゃないかと思う。

信号処理のアプリケーションを一から真面目に作ろうとすると、やるべきことが多すぎて途中で断念してしまうことがある。信号処理って、Hello 信号処理までがホント長くて、File I/O やらstreaming I/O等音声入出力書いたり、スペクトルやケプストラムやらメルケプやらウェーブレットやら特徴抽出書いたり、波形合成のアルゴリズム書いたり、難しい機械学習のアルゴリズム書いたり。本当にやりたいことを実現するためには、専門家はおろか初学者にはハードルが高すぎると思う。リアルタイムでやりたい（よくある状況）とかだとなおさら大変。

もちろん、そんなの自分で書かなくてもライブラリなりツールなりはたくさんある。

- [SPTK - Speech Signal Processing Toolkit](http://sp-tk.sourceforge.net/)
- [HTS - HMM-based Speech Synthesis System](http://hts.sp.nitech.ac.jp/)
- [MMDAgenet - toolkit for building voice interaction systems.](http://www.mmdagent.jp/)
- [OpenJTalk - HMM-based Text-to-Speech System](http://open-jtalk.sourceforge.net/)
- [STK - The Synthesis ToolKit in C++ (STK)](https://ccrma.stanford.edu/software/stk/)
- [Aquila - Open source DSP library for C++](http://aquila-dsp.org/)
- [PortAudio - Portable Cross-platform Audio I/O](http://www.portaudio.com/)
- [Sonic visualiser](http://www.sonicvisualiser.org/)
- [MIRToolbox](https://www.jyu.fi/hum/laitokset/musiikki/en/research/coe/materials/mirtoolbox)
- [ISSE - An Interactive Source Separation Editor](http://isse.sourceforge.net/)
- [音声分析変換合成法STRAIGHT](http://www.wakayama-u.ac.jp/~kawahara/STRAIGHTadv/index_j.html)
- [音声分析合成システム「WORLD」](http://www.slp.is.ritsumei.ac.jp/~morise/world/)

直近で印象に残ってるのはこんなもん。どれも素晴らしいけど、傾向としては専門知識のある人向けの物が多い気がしている。一方で、専門知識がなくても使えるツールというのは、本当に少ないと思う。これは個人的に大きな問題だと思っていて、何とか解決したい。というか僕でも簡単に使える便利ツールほしい。

とまぁそんな経緯で、

- 音声/音楽信号処理をやるためのベースをすでに備えていて、アプリケーションが簡単に作れる
- 専門知識がなくてもまぁ使える
- リアルタイムアプリケーションを作れる
- 商用/学術利用共にフリー

なライブラリを作ろうと考えている。商用フリーなのは、単に僕がGPL/LPGLとか嫌いだから。フリーという制約を除けば選択肢も増えるけど、まぁ使いづらい。

[opencv](http://opencv.org/)とか、めっちゃ素晴らしいよね。まさにこういうものがほしい（作りたい）。これの音声版ですよ。何でないんだ。あったら教えて下さい。

["Any OpenCV-like C/C++ library for Audio processing?" - StackOverflow](http://stackoverflow.com/questions/6938634/any-opencv-like-c-c-library-for-audio-processing)

今頑張って作ってるので、お楽しみに。ここに書くことで、後に引けなくする作戦です。


## 余談

ライブラリ作ろうと思ったきっかけは、つい最近声質変換を作ろうとしたことにあります。自分の声を、好きな人の声に変えられたらおもしろいなぁと思って。何か火が着いちゃった時がありました。ただ、音声読み込み、FFT、ケプストラム、メルフィルタバンク、メルケプストラム、GMM、固有声空間の構築、MLSAフィルタ、短遅延アルゴリズム、overlapping addition合成（ry

もう、やることが多すぎてギブアップした。具体的にはmlsaフィルタが難しくてやめた。その時にSPTKのソースコードを読んでいたんだけど、すごいわかりにくくて、くそーっと思って、どうせなら新しく書きなおして使いやすいライブラリ作ってやろうと思ったのが、きっかけ。まぁえらそうな事書いといて、自分がほしいからっていうのが落ちなんですけどね。

ないから作る、シンプルに言えばそれだけです。あと、絶賛有志募集中です。よろしくおねがいします。
