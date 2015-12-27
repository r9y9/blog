---
layout: post
title: "MigMix 1P, Migu 1M, Rictyとか綺麗なフォントをインストールするスクリプト "
date: 2013-07-27
comments: true
categories: font
---

家、大学、会社、レンタルサーバ、デスクトップからノートPCや仮想マシンなど、色んな環境があると思う。それぞれで、別個に環境を整えるのってとてもめんどくさい。.zshrc等の設定ファイルは、github置いておいて各環境でpullすればいい。けど、fontはデカイし、Rictyに関してはライセンスの関係もあってフォント自体を配布することは禁止されているので、github等にアップロードしておくのはいい方法ではない。

というわけで、Rictyを含め僕が使ってるフォントをインストールするスクリプトを書いた。

インストールされるのは、以下のフォント

- MigMix 1P
- Migu 1M
- Inconsolata
- Ricty
- Ricty for Powerline

基本的にはMigMix 1Pを使っていて、テキストエディタ等で等幅フォントが望ましい場合は、Migu 1M か Ricty にしてる。Ricty for Powerlineは、powerlineで必要なフォントパッチを当てたもので、ターミナルで使ってる。

https://gist.github.com/r9y9/5938857

```bash
#!/bin/bash

# Requirement: wget, unzip, git and fontforge
function check_requirement() {
    messages=()
    for r in "wget" "unzip" "git" "fontforge"
    do
 [ -z `which $r` ] && messages+=($r)
    done
    if [ ${#messages[@]} -gt 0 ]
    then
 echo "NOT found: ${messages[@]}. Try again after installing the command(s)."
 exit 1;
    fi
}

# Install directory
[ ! -d ~/.fonts ] && mkdir -p ~/.fonts/

# MigMix 1P
function install_migumix-1p() {
    wget -O migmix.zip "http://sourceforge.jp/frs/redir.php?m=jaist&f=%2Fmix-mplus-ipa%2F59021%2Fmigmix-1p-20130617.zip"
    unzip -o migmix.zip -d migmix
    find migmix -name "*.ttf" | xargs -i mv -vf {} ~/.fonts
    rm -rf migmix*
}

# Migu 1M
function install_migu-1m() {
    wget -O migu-1m.zip "http://sourceforge.jp/frs/redir.php?m=jaist&f=%2Fmix-mplus-ipa%2F59022%2Fmigu-1m-20130617.zip"
    unzip -o migu-1m.zip -d migu-1m
    find migu-1m -name "*.ttf" | xargs -i mv -vf {} ~/.fonts
    rm -rf migu-1m*
}

# Inconsolata
function install_inconsolata() {
    wget -O Inconsolata.otf "http://levien.com/type/myfonts/Inconsolata.otf"
    mv -vf Inconsolata.otf ~/.fonts
}

# Ricty
# Migu-1m and Inconsolata must be installed in advance
function install_ricty() {
    git clone https://github.com/yascentur/Ricty.git
    sh Ricty/ricty_generator.sh auto
    mv -vf Ricty*.ttf ~/.fonts
    rm -rf Ricty
}

# Powerline symbols
function install_powerline_symbols() {
    wget -O PowerlineSymbols.otf "https://github.com/Lokaltog/powerline/raw/develop/font/PowerlineSymbols.otf"
    mv -vf PowerlineSymbols.otf ~/.fonts/

    wget -O 10-powerline-symbols.conf "https://github.com/Lokaltog/powerline/raw/develop/font/10-powerline-symbols.conf"
    [ ! -d ~/.config/fontconfig/conf.d/ ] && mkdir -p ~/.config/fontconfig/conf.d/
    mv -vf 10-powerline-symbols.conf ~/.config/fontconfig/conf.d/
}

# Ricty for powerline
function install_ricty_for_powerline() {
    wget -O fontpatcher.py "https://github.com/Lokaltog/powerline/raw/develop/font/fontpatcher.py"
    wget -O fontpatcher-symbols.sfd "https://github.com/Lokaltog/powerline/raw/develop/font/fontpatcher-symbols.sfd"
    fontforge -script fontpatcher.py ~/.fonts/Ricty-Regular.ttf
    mv -vf Ricty*.ttf ~/.fonts
    rm -f fontpatcher.py
    rm -f fontpatcher-symbols.sfd
}

check_requirement

install_migumix-1p
install_migu-1m
install_inconsolata
install_ricty
install_powerline_symbols
install_ricty_for_powerline

fc-cache -fv ~/.fonts
```

これでフォントインストールはほぼ自動化。ありとあらゆることを自動化したい。
