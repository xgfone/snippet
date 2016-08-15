
## After Installing Kali
### Pre-configuration
#### DNS
```shell
# vim /etc/resolv.conf
nameserver  233.5.5.5
nameserver  233.6.6.6
```

#### APT sources.list
```shell
#deb http://mirrors.aliyun.com/kali kali-rolling main contrib non-free
#deb http://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free
deb http://mirrors.aliyun.com/kali kali-rolling main contrib non-free
```

### Install and Configure Softwares
#### Add i386 Arch and Update the System
```shell
#dpkg --add-architecture i386
apt-get update
apt-get install aptitude
aptitude upgrade
```

#### Optional
```shell
# Configure the i10n, such as chinese.
dpkg-reconfigure locales
```

#### Install Some Softwares
```
aptitude install libssl1.0.0 build-essential vim git vim-gtk libssl-dev
aptitude install gdebi alacarte meld remmina devhelp calibre chmsee
aptitude install fcitx-table-wubi fcitx-pinyin fcitx-table-wbpy
aptitude install mysql-workbench chromium gparted gimp bcompare thunderbird soundconverter brasero
aptitude install xmind gitkraken gnome-screenshot
```

#### VPN Proxy
```
aptitude install network-manager-openvpn-gnome
aptitude install network-manager-pptp
aptitude install network-manager-pptp-gnome
aptitude install network-manager-strongswan
aptitude install network-manager-vpnc
aptitude install network-manager-vpnc-gnome
/etc/init.d/network-manager restart
```

#### vim
```shell
git clone git://github.com/xgfone/dot-vimrc.git ~/.vim
#ln -s ~/.vim/vimrc ~/.vimrc
git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
```
Then, start `vim`, and execute the command `:BundleInstall`.

#### git
```
git config --global user.name "xgfone"
git config --global user.email "xgfone@126.com"
```

#### SecureCRT
See BaiduPan.

**Notice:** The configuration is under `~/.vandyke/SecureCRT/Config`, and the session is under `~/.vandyke/SecureCRT/Config/Sessions`.

#### Sublime Text
##### Installation
Download from [here](https://www.sublimetext.com/3), then install it.

Download the configuration from [Github](https://github.com/xgfone/sublime-config), then copy them into the configuration directory, such as `~/.config/sublime_text_3`.

#### Atom
Download from [here](https://atom.io/), then install it.

About the plugin packages, see [here](https://github.com/xgfone/snippet/blob/master/snippet/config/atom-packages.md).

#### Komodo IDE
Download from [here](http://downloads.activestate.com/Komodo/releases/), then install it.

Download the preference from [here](https://github.com/xgfone/snippet/blob/master/snippet/config/komodoide-prefs.xml), then copy the configuration directory of Komodo IDE.

#### NetBeans
Download from [here](https://netbeans.org/downloads/).

#### MySQL Workbench
Download from [here](http://dev.mysql.com/downloads/workbench/).

#### WPS for Linux
Download from [here](http://community.wps.cn/download/).

Download the fonts from [here](https://github.com/xgfone/snippet/blob/master/snippet/software/symbol-fonts_1.2_all.deb?raw=true), then install it.


## Troubles

### Chromium
```
chromium --user-data-dir --disable-namespace-sandbox --disable-setuid-sandbox
```

### Fcitx
```shell
# vim  ~/.config/fcitx/profile
IMName=wubi
EnabledIMList=fcitx-keyboard-us:True,pinyin:True,googlepinyin:True,wubi:True
```

### Flash
```shell
aptitude isntall flashplugin-nonfree
#update-flashplugin-nonfree --install
```
