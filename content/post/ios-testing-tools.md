---
layout: post
title: iOSアプリ開発に使える単体テスト・結合テストのツール
date: 2014-02-04
comments: true
categories: ios xcode testing
---

# まとめ

結局どれがいいのか？時と場合によるが、自分の場合、以下の二つを使うのがベストではないかと考えた

- [Kiwi](https://github.com/allending/Kiwi) (単体テスト用)
- [KIF](https://github.com/kif-framework/KIF) (UI周りの結合テスト用)

追記
unit testに関しては以下の記事がよくまとまっているので、そちらを参照した方が良いです
http://magneticbear.com/lab/ios-unit-testing/

# Why so?

## 単体テスト

代表的なツールににApple製のSenTestingやXCTestがある。が、SenTestingはXcode 5に上がってからXcodeのデフォルトがXCTestになったので、新しいアプリではあえてSenTestingを使う必要はない（ちなみにSentTestingからXCTestへの変更は容易）。

KiwiかXCTestか、といった問題は、正直人によると思うが、RSpecに慣れてる人はKiwiのが使いやすいと思う。XCTestはデフォでサポートされているし使いやすいというメリットはあるが、Kiwiは[Asynchronous Testing](https://github.com/allending/Kiwi/wiki/Asynchronous-Testing) をデフォでサポートしてるというメリットもあるので、個人的にはKiwiを選択した。XCTestとかSenTestingでもAsynchronus testingは可能だけど若干めんどいし、非同期処理のテストのしやすさはやはり重要


## 結合テスト

[iOSアプリのUIテストツール候補 | Qiita](http://qiita.com/hirayaCM/items/513786631575db8e1fb1) によくまとまってる。色々調べた結果、一番メジャーなのは [KIF](https://github.com/kif-framework/KIF) っぽい、かつKIFの方がgithubで人気だからいいんじゃねという短絡的発想です。その他ツールとの比較は、しばらくして気が向いたら書きます。。。

ちなみにGoogleさんも使ってるらしい → http://googletesting.blogspot.jp/2013/08/how-google-team-tests-mobile-apps.html

では、セットアップ方法についてまとめる。

# Kiwi [[code]](https://github.com/allending/Kiwi)

基本的に、[Getting Started with Kiwi 2.0](https://github.com/allending/Kiwi/wiki/Getting-Started-with-Kiwi-2.0) を読めばわかる

## Kiwiのセットアップ

CocoaPodsを使う場合についてのみ記述する

### Xcode 5

あらかじめXcodeでテスト用のターゲットを作成して、Podfileに以下を追加する。

```
target :単体テストのターゲットの名前, :exclusive => true do
   pod 'Kiwi/XCTest'
end
```

### Xcode 5未満

```
target :単体テストのターゲットの名前, :exclusive => true do
   pod 'Kiwi'
end
```

XCTestを使うかどうか、の違いです

## インストール

```
pod install
```

でOK、簡単。公式のtutorialは結構長いけど、基本的に確認するだけの作業


# KIF [[code]](https://github.com/kif-framework/KIF) 

## Podfile

Xcodeで結合テスト用のターゲットを作成して、Podfileに以下を追加する

```
target '結合テストのターゲットの名前', :exclusive => true do
  pod 'KIF', '~> 2.0'
end
```

## インストール

```
pod install
```

でOK、簡単。インストール方法の詳細はGithubのREADMEを参照

Githubで検索するとサンプルプロジェクト等出てくるので、そちらで動作確認をするのがおすすめです。

例えばこれ https://github.com/ishkawa/KIFNextExample

## 注意点

KIFはXCTestではなくSenTestingをベースに作られてる（XCTestに対応しようとしてる[pull request](https://github.com/kif-framework/KIF/pull/313)もあるようだけど、まだ本家にmergeされてない）。よって、リンクするライブラリにはSenTestingを指定しないといけない。KiwiはXCTestを使ってるので、注意が必要

# 継続的インテグレーション?

Jenkins or Bots 使えばいいと思います。どっちもメリットデメリットがあって難しいよなーと思うけど、Jenkinsの方が柔軟性は圧倒的に高いので、Jenkinsを使おうと思ってます。

# 参考

- [Finally, Three Ways To Automate iOS App Testing  By Brad Heintz, James Paolantonio and Aaron Schildkrout](http://www.fastcolabs.com/3012626/open-company/finally-three-ways-to-automate-ios-app-testing)
- [iOS開発でのユニットテストを身につけるには | blog.ishkawa.org](http://blog.ishkawa.org/blog/2013/08/31/unit-test/)
- [iOSアプリのUIテストツール候補 | Qiita](http://qiita.com/hirayaCM/items/513786631575db8e1fb1)
- [Kiwiを用いた振る舞いテスト | mixi-inc iOSTraining](https://github.com/mixi-inc/iOSTraining/wiki/11.3-Kiwi%E3%82%92%E7%94%A8%E3%81%84%E3%81%9F%E6%8C%AF%E3%82%8B%E8%88%9E%E3%81%84%E3%83%86%E3%82%B9%E3%83%88)

