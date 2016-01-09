ipv4 的一般设置
==============

作为一个一般性的提醒,多数速度限制功能都不对 loopback 起作用,所以不要进行本地测试。限制是由“jiffies” 来提供的,并强迫使用前面提到过的 TBF。

内核内部有一个时钟,每秒钟发生“HZ”个 jiffies(滴嗒)。在 Intel 平台上,HZ 的值一般都是 100。所以设置*_rate 文件的时候,如果是 50,就意味着每秒允许 2 个包。TBF 配置成为如果有多余的令牌就允许 6 个包的突发。

下面列表中的一些条目摘录自 Alexey Kuznetsov <kuznet@ms2.inr.ac.ru> 和 Andi Kleen <ak@muc.de> 写的 /usr/src/linux/Documentation/networking/ip-sysctl.txt。

##### /proc/sys/net/ipv4/icmp_destunreach_rate
    一旦内核认为它无法发包,就会丢弃这个包,并向发包的主机发送 ICMP 通知。

##### /proc/sys/net/ipv4/icmp_echo_ignore_all
    根本不要响应 echo 包。请不要设置为缺省,它可能在你正被利用成为 DoS 攻击的跳板时可能有用。

##### /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts [Useful]
    如果你 ping 子网的子网地址,所有的机器都应该予以回应。这可能成为非常好用的拒绝服务攻击工具。
    设置为 1 来忽略这些子网广播消息。

##### /proc/sys/net/ipv4/icmp_echoreply_rate
    设置了向任意主机回应 echo 请求的比率。

##### /proc/sys/net/ipv4/icmp_ignore_bogus_error_responses
    设置它之后,可以忽略由网络中的那些声称回应地址是广播地址的主机生 成的 ICMP 错误。

##### /proc/sys/net/ipv4/icmp_paramprob_rate
    一个相对不很明确的 ICMP 消息,用来回应 IP 头或 TCP 头损坏的异常数据包。
    你可以通过这个文件控制消息的发送比率。

##### /proc/sys/net/ipv4/icmp_timeexceed_rate
    这个在 traceroute 时导致著名的“Solaris middle star”。这个文件控制发送 ICMP Time Exceeded 消息的比率。

##### /proc/sys/net/ipv4/igmp_max_memberships
    主机上最多有多少个 igmp (多播)套接字进行监听。
    求助: Is this true?

##### /proc/sys/net/ipv4/inet_peer_gc_maxtime
    求助: Add a little explanation about the inet peer storage? Minimum interval between garbage
    collection passes. This interval is in effect under low (or absent) memory pressure on the pool.
    Measured in jiffies.

##### /proc/sys/net/ipv4/inet_peer_gc_mintime
    每一遍碎片收集之间的最小时间间隔。当内存压力比较大的时候,调整这 个间隔很有效。以 jiffies 计。

##### /proc/sys/net/ipv4/inet_peer_maxttl
    entries 的最大生存期。在 pool 没有内存压力的情况下(比如,pool 中 entries 的数量很少的时候),
    未使用的 entries 经过一段时间就会过期。以 jiffies 计。

##### /proc/sys/net/ipv4/inet_peer_minttl
    entries 的最小生存期。应该不小于汇聚端分片的生存期。
    当 pool 的大小 不大于 inet_peer_threshold 时, 这个最小生存期必须予以保证。以 jiffies 计。

##### /proc/sys/net/ipv4/inet_peer_threshold
    The approximate size of the INET peer storage. Starting from this threshold entries will be
    thrown aggressively. This threshold also determines entries' time-to-live and time intervals
    between garbage collection passes. More entries, less time-to-live, less GC interval.

##### /proc/sys/net/ipv4/ip_autoconfig
    这个文件里面写着一个数字,表示主机是否通过 RARP、BOOTP、DHCP 或者其它机制取得其 IP 配置。否则就是 0。

##### /proc/sys/net/ipv4/ip_default_ttl
    数据包的生存期。设置为 64 是安全的。如果你的网络规模巨大就提高这 个值。
    不要因为好玩而这么做——那样会产生有害的路由环路。实际上, 在很多情况下你要考虑能否减小这个值。

##### /proc/sys/net/ipv4/ip_dynaddr 74
    如果你有一个动态地址的自动拨号接口,就得设置它。当你的自动拨号接 口激活的时候,本地所有没有收到答复的 TCP
    套接字会重新绑定到正确 的地址上。这可以解决引发拨号的套接字本身无法工作,重试一次却可以 的问题。

##### /proc/sys/net/ipv4/ip_forward
    内核是否转发数据包。缺省禁止。

##### /proc/sys/net/ipv4/ip_local_port_range
    用于向外连接的端口范围。缺省情况下其实很小：1024 到 4999。

##### /proc/sys/net/ipv4/ip_no_pmtu_disc
    如果你想禁止“沿途 MTU 发现”就设置它。“沿途 MTU 发现”是一种技 术,可以在传输路径上检测出最大可能的 MTU 值。

##### /proc/sys/net/ipv4/ipfrag_high_thresh
    用于 IP 分片汇聚的最大内存用量。分配了这么多字节的内存后,一旦用 尽,分片处理程序就会丢弃分片。
    When ipfrag_high_thresh bytes of memory is allocated for this purpose, the fragment handler
    will toss packets until ipfrag_low_thresh is reached.

##### /proc/sys/net/ipv4/ip_nonlocal_bind
    如果你希望你的应用程序能够绑定到不属于本地网卡的地址上时,设置这 个选项。如果你的机器没有专线连接
    (甚至是动态连接)时非常有用,即使 你的连接断开,你的服务也可以启动并绑定在一个指定的地址上。

##### /proc/sys/net/ipv4/ipfrag_low_thresh
    用于 IP 分片汇聚的最小内存用量。

##### /proc/sys/net/ipv4/ipfrag_time
    IP 分片在内存中的保留时间(秒数)。

##### /proc/sys/net/ipv4/tcp_abort_on_overflow
    一个布尔类型的标志,控制着当有很多的连接请求时内核的行为。启用的 话,如果服务超载,内核将主动地发送 RST 包。

##### /proc/sys/net/ipv4/tcp_fin_timeout
    如果套接字由本端要求关闭,这个参数决定了它保持在 FIN-WAIT-2 状态 的时间。对端可以出错并永远不关闭连接,
    甚至意外当机。缺省值是 60 秒。2.2 内核的通常值是 180 秒,你可以按这个设置,但要记住的是,即 使你的机器是
    一个轻载的 WEB 服务器,也有因为大量的死套接字而内存 溢出的风险,FIN-WAIT-2 的危险性比 FIN-WAIT-1 要小,
    因为它最多只 能吃掉 1.5K 内存,但是它们的生存期长些。参见 tcp_max_orphans。

##### /proc/sys/net/ipv4/tcp_keepalive_time
    当 keepalive 起用的时候,TCP 发送 keepalive 消息的频度。缺省是 2 小时。

##### /proc/sys/net/ipv4/tcp_keepalive_intvl
    当探测没有确认时,重新发送探测的频度。缺省是 75 秒。

##### /proc/sys/net/ipv4/tcp_keepalive_probes
    在认定连接失效之前,发送多少个 TCP 的 keepalive 探测包。缺省值是 9。
    这个值乘以 tcp_keepalive_intvl 之后决定了,一个连接发送了 keepalive 之 后可以有多少时间没有回应。

##### /proc/sys/net/ipv4/tcp_max_orphans
    系统中最多有多少个 TCP 套接字不被关联到任何一个用户文件句柄上。如果超过这个数字,孤儿连接将即刻被复位
    并打印出警告信息。这个限制 仅仅是为了防止简单的 DoS 攻击,你绝对不能过分依靠它或者人为地减 小这个值,
    更应该增加这个值(如果增加了内存之后)。This limit exists only to prevent simple DoS attacks,
    you _must_ not rely on this or lower the limit artificially, but rather increase it
    (probably, after increasing installed memory), if network conditions require more than
    default value, and tune network services to linger and kill such states more aggressively.
    让我再次提醒你：每个孤儿套接字最多能够吃掉你 64K 不可交换的内存。

##### /proc/sys/net/ipv4/tcp_orphan_retries
    本端试图关闭 TCP 连接之前重试多少次。缺省值是 7,相当于 50 秒~16 分钟(取决于 RTO)。
    如果你的机器是一个重载的 WEB 服务器,你应该考 虑减低这个值,因为这样的套接字会消耗很多重要的资源。
    参见 tcp_max_orphans。

##### /proc/sys/net/ipv4/tcp_max_syn_backlog
    记录的那些尚未收到客户端确认信息的连接请求的最大值。对于有 128M 内存的系统而言,缺省值是 1024,
    小内存的系统则是 128。如果服务器不 堪重负,试试提高这个值。注意!如果你设置这个值大于 1024,
    最好同时调整 include/net/tcp.h 中的 TCP_SYNQ_HSIZE , 以保证
    TCP_SYNQ_HSIZE*16 ≤ tcp_max_syn_backlo，然后重新编译内核。

##### /proc/sys/net/ipv4/tcp_max_tw_buckets
    系统同时保持 timewait 套接字的最大数量。如果超过这个数字,time-wait 套接字将立刻被清除并打印警告信息。
    这个限制仅仅是为了防止简单的 DoS 攻击,你绝对不能过分依靠它或者人为地减小这个值,如果网络实际需要大于缺省值,
    更应该增加这个值(如果增加了内存之后)。

##### /proc/sys/net/ipv4/tcp_retrans_collapse
    为兼容某些糟糕的打印机设置的“将错就错”选项。再次发送时,把数据 包增大一些,来避免某些 TCP 协议栈的 BUG。

##### /proc/sys/net/ipv4/tcp_retries1
    在认定出错并向网络层提交错误报告之前,重试多少次。
    缺省设置为 RFC 规定的最小值：3，相当于3秒 ~ 8分钟(取决于 RIO)。

##### /proc/sys/net/ipv4/tcp_retries2
    在杀死一个活动的 TCP 连接之前重试多少次。RFC 1122 规定这个限制应 该长于 100 秒。这个值太小了。
    缺省值是 15，相当于 13~30 分钟(取决 于 RIO)。

##### /proc/sys/net/ipv4/tcp_rfc1337
    这个开关可以启动对于在 RFC1337 中描述的“tcp 的 time-wait 暗杀危机” 问题的修复。
    启用后,内核将丢弃那些发往 time-wait 状态 TCP 套接字的 RST 包。却省为 0。

##### /proc/sys/net/ipv4/tcp_sack
    特别针对丢失的数据包使用选择性 ACK,这样有助于快速恢复。

##### /proc/sys/net/ipv4/tcp_stdurg
    使用 TCP 紧急指针的主机需求解释。因为绝大多数主机采用 BSD 解释, 所以如果你在 Linux 上打开它,
    可能会影响它与其它机器的正常通讯。缺 省是 FALSE。

##### /proc/sys/net/ipv4/tcp_syn_retries
    在内核放弃建立连接之前发送 SYN 包的数量。

##### /proc/sys/net/ipv4/tcp_synack_retries
    为了打开对端的连接,内核需要发送一个 SYN 并附带一个回应前面一个 SYN 的 ACK。
    也就是所谓三次握手中的第二次握手。这个设置决定了内 核放弃连接之前发送 SYN+ACK 包的数量。

##### /proc/sys/net/ipv4/tcp_timestamps
    时间戳可以避免序列号的卷绕。一个 1Gbps 的链路肯定会遇到以前用过的序列号。
    时间戳能够让内核接受这种“异常”的数据包。

##### /proc/sys/net/ipv4/tcp_tw_recycle
    能够更快地回收 TIME-WAIT 套接字。缺省值是 1。除非有技术专家的建议和要求,否则不应修改。

##### /proc/sys/net/ipv4/tcp_window_scaling
    一般来说 TCP/IP 允许窗口尺寸达到 65535 字节。对于速度确实很高的网 络而言这个值可能还是太小。
    这个选项允许设置上 G 字节的窗口大小, 有利于在带宽*延迟很大的环境中使用。
