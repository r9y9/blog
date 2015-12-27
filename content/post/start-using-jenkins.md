---
layout: post
title: "Jenkinsを使い始めたのでメモ。インストール方法とかプラグインとかテーマとか"
date: 2013-11-16
comments: true
categories: jenkins
---

<div align="center"><img src="/images/jenkins_doony.png "Jenkinsをdoonyというテーマにしたもの。jenkinsおじさんはいません"" class="image"></div>

## Jenkinsとは

超高機能cronだと思えばいいよ（先輩より

## Ubuntu 12.04へのインストール

以下のURLに従えばできる。

https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+on+Ubuntu

```bash
wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins
```

まとめると、

1. 新しいjenkinsのpackageをリポジトリに追加して
2. apt-get でインストール（2013/11/16 現在だと、1.5.39が入る）

※1の手順を省くと、少しバージョン（1.4.x）の古いjenkinsが入ってしまうので注意

## Mac OS Xへのインストール

```bash
brew install jenkins
```

でおｋ。

## プラグイン

インストールしたものをメモ。他にも便利なのはたくさんあると思う

- [Configuration Slicing plugin](https://wiki.jenkins-ci.org/display/JENKINS/Configuration+Slicing+Plugin) 設定を一括で変更したいときに使う
- [Jenkins GIT plugin](https://wiki.jenkins-ci.org/display/JENKINS/Git+Plugin) Git使うために
- [Jenkins Email Extension Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Email-ext+plugin) メール機能を拡張するため
- [Jenkins Job Configuration History Plugin](https://wiki.jenkins-ci.org/display/JENKINS/JobConfigHistory+Plugin) ジョブの変更履歴がサイドバーから見れる、便利
- [Python Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Python+Plugin) Pythonスクリプト書きたい
- [Simple Theme Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Simple+Theme+Plugin) テーマ変更するのに使う
- [Timestamper](https://wiki.jenkins-ci.org/display/JENKINS/Timestamper) コンソール出力にタイムスタンプが付く、便利
- [Jenkins jQuery plugin](https://wiki.jenkins-ci.org/display/JENKINS/jQuery+Plugin) テーマにDoonyを使うためにいる

## テーマをDoonyにする

見やすい、オススメ。気に入った。

https://github.com/kevinburke/doony

上によれば、

> Doony is a series of UI improvements on top of Jenkins. Install this to make your Jenkins user experience much better.

とのこと。良い。使い方などは、githubのdoonyのREADMEを見るか、あるいは以下の日本語の記事にも書いてある。

[JenkinsのUIをすっきり変化させるテーマdoonyを試す | Safx](http://safx-dev.blogspot.jp/2013/10/jenkinsuidoony.html)

### 必要なプラグイン

- Simple Theme Plugin
- Jenkins jQuery plugin

※テーマのプラグインだけでなく、jqueryのプラグインもインストールしないとダメなので注意


## おわりに

これでテストもろもろ自動化だー


## その他メモ

- /etc/default/jenkinsでjava起動時に文字コードをutf-8にしても、コンソールのログで日本語が化ける？
     - /etc/default/jenkinsを変更前に実行したものは化けたまま。変更後に実行すると、化けない
     - Jenkinsのバージョンを1.4.xから1.5.39にしたらオプションつけなくても化けなくなった？たぶん
     - ちな、Macのbrewでインストールしたものは、日本語文字化け問題に悩まなかった。新し目のjenkinsはデフォがutf-8にでもなってんですかね
- brewでインストールすると、jenkinsユーザは作られない。ubuntuでインストールすると、jenkinsというユーザが作られ、jenkins権限でdeamonが立ち上がる
     - スクリプトでsudoするために、visudoで `jenkins ALL=(ALL) NOPASSWD:ALL` しておく
- workspaceの場所
     - brewでインストールした場合、~/.jenkins/ にできると思う
     - ubuntuの場合、/var/lib/jenkins/ にある
- Macの場合、jenkinsの実行ユーザをちゃんと考えないとですね
