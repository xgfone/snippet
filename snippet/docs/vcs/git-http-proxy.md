
如何让 Git 使用 HTTP 代理服务器
===========================

如果是 `git clone http://` 或 `git clone https://` 的话直接把代理服务器加到环境变量就可以了：
```shell
$ export http_proxy="http://username:password@squid.vpsee.com:3128/"
$ export https_proxy="http://username:password@squid.vpsee.com:3128/"
```

如果是 `git clone git://` 的话麻烦一些（可能有的 git 源不提供 http/https 的方式），需要先安装 `socat`，然后创建一个叫做 gitproxy 的脚本并填上合适的服务器地址、端口号等，最后配置 git 使用 gitproxy 脚本：
```shell
$ sudo apt-get install socat
$ sudo vi /usr/bin/gitproxy
#!/bin/bash
PROXY=squid.vpsee.com
PROXYPORT=3128
PROXYAUTH=username:password
exec socat STDIO PROXY:$PROXY:$1:$2,proxyport=$PROXYPORT,proxyauth=$PROXYAUTH
$ sudo  chmod +x /usr/bin/gitproxy
$ git config --global core.gitproxy gitproxy
```

From: http://www.cnblogs.com/popsuper1982/p/3800557.html
