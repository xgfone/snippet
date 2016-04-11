
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

### Install Softwares
#### Add i386 Arch and Update the System
```
dpkg --add-architecture i386
apt-get update
apt-get isntall aptitude
```

#### Install Some Softwares
```
aptitude install libssl build-essential vim git vim-gtk libssl-dev
aptitude install gdebi alacarte meld remmina devhelp
```

#### SecureCRT
See BaiduPan.

#### VPN Proxy
```
apt-get install network-manager-openvpn-gnome
apt-get install network-manager-pptp
apt-get install network-manager-pptp-gnome
apt-get install network-manager-strongswan
apt-get install network-manager-vpnc
apt-get install network-manager-vpnc-gnome
/etc/init.d/network-manager restart
```
#### Optional
```
aptitude install fcitx-table-wubi fcitx-pinyin fcitx-table-wbpy
aptitude install mysql-workbench chromium
```

### Configure
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

#### Optional
```
dpkg-reconfigure locales
```

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
