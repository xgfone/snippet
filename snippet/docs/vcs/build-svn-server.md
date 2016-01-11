
### 建议与说明
对于版本控制系统，最好使用Git（C语言开发）或Mercurial（Python开发），二者都是分布式VCS。

如果你还在用CVS，那笔者只能认为你还生活在远古时代；如果是SVN，那你就生活清朝末民国初。如果你生活在二十一世纪，那你可以选用Git或Mercurial，或者其他更先进的VCS。

笔者记忆不好，本文仅是做个简单的备忘——不一定什么时候可能会跟民国初期的先进知识份子打交道。

SVN是集中式VCS，客户端一旦无法连接到服务端（如：服务端崩溃或客户端无网络等），代码就无法更新、提交；而分布式VCS，每个客户端都是一个中心，换句话说，就是分布式VCS没有中心这一概念，客户端只要向本地提交，等能够连上其他客户端（或将其中一个客户端作为中央VCS）时，再推送（Push）过去即可。


### 安装Subversion
```shell
$ sudo apt-get install subversion  # Debian/Ubuntu 系列的Linux
$ sudo yum install subversion      # RedHat/CentOS 系列的Linux
```

### 验证安装
```
$ svnserve --version  # 以下是输出
svnserve, version 1.7.9 (r1462340)
   compiled Oct 15 2013, 12:40:34

Copyright (C) 2013 The Apache Software Foundation.
This software consists of contributions made by many people; see the NOTICE
file for more information.
Subversion is open source software, see http://subversion.apache.org/

The following repository back-end (FS) modules are available:

* fs_base : Module for working with a Berkeley DB repository.
* fs_fs : Module for working with a plain file (FSFS) repository.

Cyrus SASL authentication is available.
```

### 服务搭建
#### 1、创建一个repo目录
```shell
$ mkdir ~/svn
```
此目的是存放所有的SVN服务repo，这一步可省略不要

#### 2、创建一个repo
```shell
$ svnadmin create ~/svn/testrepo
$ ls ~/svn/testrepo
conf  db  format  hooks  locks  README.txt
```

##### 说明
conf 目录是存储配置文件的地方
```shell
$ ls ~/svn/testrepo/conf
authz  passwd  svnserve.conf
```
其中，svnserve.conf 是SVN服务配置文件；paaswd用户口令、密码文件；authz是权限配置文件

###### （1）svnserve.conf 文件配置项主要有以下5项

    anon-access: 控制非鉴权用户访问版本库的权限。
    auth-access: 控制鉴权用户访问版本库的权限。
    password-db: 指定用户名口令文件名。
    authz-db:    指定权限配置文件名，通过该文件可以实现以路径为基础的访问控制。
    realm:       指定版本库的认证域，即在登录时提示的认证域名称。
                 若两个版本库的认证域相同，建议使用相同的用户名口令数据文件

###### （2）passwd文件存储账号和密码，每行一个账号，格式如下

    [users]
    username1 = password1
    username2 = password2
    username3 = password3
    username4 = password4
    username5 = password5
    username6 = password6
    username7 = password7

###### （3）authz文件
可以为用户设一个别名，以及将用户分成不同的组，然后指定每个repo对不同用户或组的访问权限。
authz配置的具体语法请参见authz文件中的说明。

_**一个配置例子**_
```
[groups]                 # 将不同的用户分到不同的组中
admin = username1,username2
devel1 = username3,username4
devel2 = username5,username6

# 为所有库指定默认访问规则：所有人可以读，管理员可以写，危险分子没有任何权限
[/]    # 对应~/svn 目录
* = r
@admin = rw
dangerman =

[testrepo:/]
@devel1 = rw
@devel2 = rw
username7 = rw

[proj1:/]
@devel1 = rw

[proj2:/]
@devel2 = rw
username7 = rw
```

### 启动和停止SVN服务

#### 1、启动SVN
```shell
$ svnserve -d -r ~/svn/testrepo
```
-d 表示作为守护进程在后台运行

-r 指定SVN服务的根目录（例子中为~/svn）

#### 2、停止SVN
首先通过ps命令找到svnserve服务的进程ID，然后用kill命令将其杀死。
```shell
$ ps aux | grep svn
xgf  9993  0.0  0.0  73384  1116 ?  Ss  11:15  0:00 svnserve -d -r /home/xgf/svn
xgf  10100  0.0  0.0  13648  988 pts/0  S+  11:16  0:00 grep --color=auto svnserve
$ kill 9993
```

### 签出（checkout）一个Repo
```shell
$ svn svn://127.0.0.1/testrepo
```

### 日常使用

#### 1、更新Repo
```shell
$ svn up(date)
```

#### 2、新增一个文件（或目录）
```shell
$ svn add filename
```

#### 3、提交更新
```shell
$ svn commit [-m "Description"]
```

### SVN服务支持HTTP
svnserve 默认开启3690端口，提供 SVN 协议；但有些公司会禁止除80（HTTP）等以外的其他端口。为了继续使用 SVN 服务，可以将SVN关联到HTTP服务器（如Apache）上，即通过HTTP协议来访问SVN服务。

由于 SVN 也随着 CVS 进入老年，如果有需要，就再 Baidu 或 Google 一下吧。
