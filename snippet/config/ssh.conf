```ini
# 1. 关于 SSH Server 的整体设定
#Port 22　　　　　　　　　　   # SSH 预设使用 22 这个 port
Protocol 2  　　　　　　　     # 选择的 SSH 协议版本，可以是 1 也可以是 2 。
　　　　　　　　　　　　　     # 如果要同时支持两者，就必须要使用 2,1 这个分隔了！
#ListenAddress 0.0.0.0　　     # 监听的主机适配卡。如果不设定的话，则预设所有接口
PidFile /var/run/sshd.pid　　　# 可以放置 SSHD 这个 PID 的档案
LoginGraceTime 600　　　　     # 当使用者连上 SSH server 之后，会出现输入密码的画面，
　　　　　　　　　　　　　     # 在该画面中，在多久时间内没有成功连上 SSH server ，
　　　　　　　　　　　　　     # 就断线！时间为秒！
Compression yes　　　　　　    # 是否可以使用压缩指令


# 2. 说明主机的 Private Key 放置的档案，预设使用下面的档案即可
HostKey /etc/ssh/ssh_host_key　　　　# SSH version 1 使用的私钥
HostKey /etc/ssh/ssh_host_rsa_key　　# SSH version 2 使用的 RSA 私钥
HostKey /etc/ssh/ssh_host_dsa_key　　# SSH version 2 使用的 DSA 私钥

# 2.1 关于 version 1 的一些设定
#KeyRegenerationInterval 3600　 　　 # 由前面联机的说明可以知道， version 1 会使用
　　　　　　　　　　　　　　　　　　 # server 的 Public Key ，那么如果这个 Public
　　　　　　　　　　　　　　　　　　 # Key 被偷的话，岂不完蛋？所以需要每隔一段时间
　　　　　　　　　　　　　　　　　　 # 来重新建立一次！这里的时间为秒！
ServerKeyBits 768 　　　　　　　　　 # 这个就是 Server key 的长度！


# 3. 关于登录文件的讯息数据放置与 daemon 的名称
SyslogFacility AUTH　　　　　　　　　# 当有人使用 SSH 登入系统的时候，SSH会记录资
　　　　　　　　　　　　　　　　　　 # 讯，这个信息要记录在什么 daemon name 底下
LogLevel INFO　　　　　　　　　　　　# 登录记录的等级


# 4. 安全设定项目

# 4.1 登入设定部分
PermitRootLogin yes　　 　 # 是否允许 root 登入！预设是允许的！
UserLogin no　　　　　　　 # 在 SSH 底下本来就不接受 login 这个程序的登入！
StrictModes yes　　　　　　# 当使用者的 host key 改变之后，Server 就不接受联机，
　　　　　　　　　　　　　 # 可以抵挡部分的木马程序！
#RSAAuthentication yes　　 # 是否使用纯的 RSA 认证！仅针对 version 1
PubkeyAuthentication yes　 # 是否允许 Public Key！只有 version 2
AuthorizedKeysFile .ssh/authorized_keys
　　　　　　　　　　　　　 # 上面这个在设定若要使用不需要密码登入的账号时，
                           # 那么那个账号的存放档案所在档名！

# 4.2 认证部分
RhostsAuthentication no　　# 本机系统不止使用 .rhosts ，因为仅使用 .rhosts 太
　　　　　　　　　　　　　 # 不安全了，所以这里一定要设定为 no ！
IgnoreRhosts yes　　　　　 # 是否取消使用 ~/.ssh/.rhosts 来做为认证！
RhostsRSAAuthentication no # 这个选项是专门给 version 1 用的，使用 rhosts 档案在
　　　　　　　　　　　　　 # /etc/hosts.equiv配合 RSA 演算方式来进行认证！不要使用
HostbasedAuthentication no # 这个项目与上面的项目类似，不过是给 version 2 使用的！
IgnoreUserKnownHosts no　　# 是否忽略家目录内的 ~/.ssh/known_hosts 这个档案所记录
　　　　　　　　　　　　　 # 的主机内容！
PasswordAuthentication yes # 密码验证当然是需要的！
PermitEmptyPasswords no　　# 若上面那一项如果设定为 yes 的话，这一项就最好设定
　　　　　　　　　　　　　 # 为 no ，这个项目在是否允许以空的密码登入！

ChallengeResponseAuthentication yes  # 挑战任何的密码认证！所以，任何 login.conf
　　　　　　　　　　　　　　　　　　 # 规定的认证方式，均可适用！
#PAMAuthenticationViaKbdInt yes      # 是否启用其它的 PAM 模块！启用这个模块将会
　　　　　　　　　　　　　　　　　　 # 导致 PasswordAuthentication 设定失效！
　
# 4.3 与 Kerberos 有关的参数设定
#KerberosAuthentication no
#KerberosOrLocalPasswd yes
#KerberosTicketCleanup yes
#KerberosTgtPassing no
　
# 4.4 底下是有关在 X-Window 底下使用的相关设定
X11Forwarding yes
#X11DisplayOffset 10
#X11UseLocalhost yes

# 4.5 登入后的项目
PrintMotd no               # 登入后是否显示出一些信息呢。
PrintLastLog yes　　　　 　# 显示上次登入的信息！预设是 yes ！
KeepAlive yes　　　　　　  # 一般而言，如果设定这项目的话，那么 SSH Server 会传送
　　　　　　　　　　　　 　# KeepAlive 的讯息给 Client 端，以确保两者的联机正常！
　　　　　　　　　　　　 　# 在这个情况下，任何一端死掉后， SSH 可以立刻知道，
                           # 而不会有僵尸程序的发生！
UsePrivilegeSeparation yes # 使用者的权限设定项目！
MaxStartups 10　　　　　 　# 同时允许几个尚未登入的联机画面。当我们连上 SSH ，
　　　　　　　　　　　　 　# 但是尚未输入密码时，这个时候就是我们所谓的联机画面！
　　　　　　　　　　　　 　# 在这个联机画面中，为了保护主机，所以需要设定最大值。

# 4.6 关于使用者抵挡的设定项目
DenyUsers *　　　　　　　 # 设定受抵挡的使用者名称，如果是全部的使用者，那就是全部
　　　　　　　　　　　　　# 挡吧！若是部分使用者，可以将该账号填入！例如下列！
DenyUsers test
DenyGroups test　　　　　 # 与 DenyUsers 相同！仅抵挡几个群组而已！


# 5. 关于 SFTP 服务的设定项目
Subsystem  sftp  /usr/lib/ssh/sftp-server

# 6. 加速 SSH 登录
UseDNS no
GSSAPIAuthentication no

# 7. 克隆会话
Host *
    ControlMaster auto
    ControlPath ~/.ssh/%h-%p-%r
    ControlPersist yes
```
