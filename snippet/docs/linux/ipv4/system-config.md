
## TCP高并发连接
对于想支持更高数量的TCP并发连接的通讯处理程序，就必须修改Linux对当前用户的进程同时打开的文件数量的软限制(soft limit)和硬限制(hardlimit)。其中软限制是指Linux在当前系统能够承受的范围内进一步限制用户同时打开的文件数;硬限制则是根据系统硬件资源状况(主要是系统内存)计算出来的系统最多可同时打开的文件数量。通常软限制小于或等于硬限制。


### 提高Linux系统级的最大打开文件数限制
```shell
echo 1024000 > /proc/sys/fs/file-max
```
这是Linux系统级硬限制，所有用户级的打开文件数（即所有用户打开文件数总和）限制都不应超过这个数值。通常这个系统级硬限制是Linux系统在启动时根据系统硬件资源状况计算出来的最佳的最大同时打开文件数限制，如果没有特殊需要，不应该修改此限制，除非想为用户级打开文件数限制设置超过此限制的值。


### 修改用户进程可打开文件数限制
使用`ulimit`命令查看、修改系统允许当前用户每个进程打开的文件数限制。
```shell
ulimit -u [102400]
```
如果系统回显类似于“`Operation notpermitted`”之类的话，说明上述修改失败，一般是因为`ulimit`指定的数值超过了Linux系统对该用户打开文件数的软限制或硬限制。因此，就需要修改Linux系统对用户的关于打开文件数的软限制和硬限制。

(1) 修改`/etc/security/limits.conf`文件，在文件中添加如下行：
```
USERNAME soft nofile 102400
USERNAME hard nofile 102400
```
注：可用'`*`'号表示修改所有用户的限制。

(2) 修改`/etc/pam.d/login`文件，在文件中添加如下行：
```shell
session required /lib/security/pam_limits.so
```
这是告诉Linux在用户完成系统登录后，应该调用`pam_limits.so`模块来设置系统对该用户可使用的各种资源数量的最大限制(包括用户可打开的最大文件数限制)，而`pam_limits.so`模块就会从`/etc/security/limits.conf`文件中读取配置来设置这些限制值。


### 修改网络内核对TCP连接的有关限制
```shell
## /etc/sysctl.conf
net.ipv4.ip_forward=1
net.ipv4.ip_conntrack_max = 102400
net.ipv4.ip_local_port_range = 1024 65536

net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.core.somaxconn = 262144
net.core.netdev_max_backlog = 30000

net.ipv4.route.flush=1
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.ipv4.tcp_fin_timeout = 10
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_timestamps = 1
net.ipv4.tcp_window_scaling = 0
net.ipv4.tcp_sack = 0
net.ipv4.tcp_no_metrics_save=1
net.ipv4.tcp_syncookies = 0
net.ipv4.tcp_max_orphans = 262144
net.ipv4.tcp_max_syn_backlog = 262144
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 2
```
然后执行如下命令使其生效：
```shell
/sbin/sysctl -p /etc/sysctl.conf
```
