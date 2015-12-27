---
layout: post
title: "QtのQMediaPlayerを使って簡単なAudio playerを作る"
date: 2013-10-27
comments: true
categories: qt media-player
---

<div align="center"><img src="/images/media-player_clipped_rev_1.png "A simple media player demo"" class="image"></div>

Qtのmultimediaを使えば簡単に出来る。最低限の機能しかないけど試しに作ってみた。再生、停止、スライダー、ボリューム調整とかだけなら、100行くらいでできる。

https://github.com/r9y9/media-player-demo

あまりにも簡単なコードだけど、何か音が流れるだけで満足してしまうのは普段低レベルのコードばっか書いてるからか…

感想はさておき、適当なアプリ作るのに、以下の当たりを参考にした

- [Qt Multimedia Overview](http://qt-project.org/doc/qt-5.0/qtmultimedia/multimediaoverview.html)
- [QMediaPlayer Class](http://qt-project.org/doc/qt-5.0/qtmultimedia/qmediaplayer.html) 
- [MediaPlayer](http://qt-project.org/doc/qt-5.0/qtmultimedia/qml-qtmultimedia5-mediaplayer.html)

## メディアの再生

[QMediaPlayer Class](http://qt-project.org/doc/qt-5.0/qtmultimedia/qmediaplayer.html) から引用すれば、

```cpp
player = new QMediaPlayer;
connect(player, SIGNAL(positionChanged(qint64)), this, SLOT(positionChanged(qint64)));
player->setMedia(QUrl::fromLocalFile("/Users/me/Music/coolsong.mp3"));
player->setVolume(50);
player->play();
```

で再生できる。簡単過ぎる。。

Qt5 になってから、さらにMultimediaが進化したらしいので、これからも色々使っていきたい。特にグラフィック周りがすごくなったとかなってないとか。今試行錯誤中


## Qtめも

- Resourceを登録するとき、ちゃんとリソースファイルを"保存"しないとdesigner上では登録したリソースが出てこない
- volume(50)だとけっこう小さい。ちなみに単位なんやねんということだけど、classのドキュメントには書いてなかった。

