
TC 对包进行分类的高级过滤器
=====================

过滤器用与把数据包分类并放入相应的子队列。这些过滤器在分类的队列规定内部被调用。

下面就是我们可用的分类器(部分):

**fw**

    根据防火墙如何对这个数据包做标记进行判断。如果你不想学习 tc 的过滤器语法,这倒是一个捷径。

**u32**

    根据数据包中的各个字段进行判断,如源 IP 地址等等。

**route**

    根据数据包将被哪条路由进行路由来判断。

**rsvp**, **rsvp6**

    根据数据包的 RSVP 情况进行判断。只能用于你自己的网络,互联网并不 遵守 RSVP。

**tcindex**

    用于 DSMARK 队列规定。

通常来说，总有很多途径可实现对数据包分类，最终取决于你喜欢使用哪种系统。

分类器一般都能接受几个参数，为了方便我们列出来:

**protocol**

    这个分类器所接受的协议。一般来说你只会接受 IP 数据。必要参数。

**parent**

    这个分类器附带在哪个句柄上。句柄必须是一个已经存在的类。必要参数。

**prio**

    这个分类器的优先权值。优先权值低的优先。

**handle**

    对于不同过滤器,它的意义不同。

后面所有的节都假定你试图对去往 HostA 的流量进行整形。并且假定根类配置为 1: ，并且你希望把选中的数据包送给 1:1 类。

## u32 分类器

U32 分类器是当前实现中最先进的过滤器。全部基于哈希表实现,所以当有很多过滤器的时候仍然能够保持健壮。

U32 过滤器最简单的形式就是一系列记录,每条记录包含两个部分:一个选择器和一个动作。下面要讲的选择器用来与 IP 包相匹配,一旦成功匹配就执行其指定的动作。最简单的动作就是把数据包发送到特定的类队列。

用来配置过滤器的 tc 命令行由三部分组成：过滤器说明、选择器和动作。

一个过滤器可以如下定义:
```shell
tc filter [add | del | change | replace | show] dev ETH_STR [pre PRIO] protocol PROTO
          [estimator INTERVAL TIME_CONSTANT] [root | classid CLASSID] [handle FILTERID]
          [[FILTER_TYPE] [help | OPTIONS]]
tc filter show [dev ETH_STR] [root | parent CLASSID]

FILTER_TYPE := { rsvp | u32 | fw | route | etc. }
FILTERID := ... format depends on classifier, see there
OPTIONS := ... try tc filter add <desired FILTER_KIND> help
```

### FW 分类器
```shell
$ tc filter add fw help 
Usage: ... fw [ classid CLASSID ] [ police POLICE_SPEC ]
       POLICE_SPEC := ... look at TBF
       CLASSID := X:Y

NOTE: CLASSID is parsed as hexadecimal input.
```

此时，`tc filter ... handle NUM fw classid CLASSID`中的 `NUM` 为 iptables 中 `--set-mark`，如：
```shell
iptables -t mangle -A POSTROUTING -d 192.168.1.0/24 -j MARK --set-mark 1
```

### U32 选择器

```shell
$ tc filter add u32 help
Usage: ... u32 [ match SELECTOR ... ] [ link HTID ] [ classid CLASSID ]
               [ police POLICE_SPEC ] [ offset OFFSET_SPEC ]
               [ ht HTID ] [ hashkey HASHKEY_SPEC ]
               [ sample SAMPLE ]
or         u32 divisor DIVISOR

Where: SELECTOR := SAMPLE SAMPLE ...
       SAMPLE := { ip | ip6 | udp | tcp | icmp | u{32|16|8} | mark } SAMPLE_ARGS [divisor DIVISOR]
       FILTERID := X:Y:Z

NOTE: CLASSID is parsed at hexadecimal input.
```

u32 选择器包含了能够对当前通过的数据包进行匹配的特征定义。它其实只是定义了 IP 包头中某些位的匹配而已,但这种看似简单的方法却非常有效。让我们看看这个从实际应用的系统中抄来的例子:
```
# tc filter add dev eth0 protocol ip parent 1:0 pref 10 u32 match u32 00100000 00ff0000 at 0 flowid 1:10
```
现在,命令的第一行已经不用解释了,前面都说过了。我们把精力集中在用 “match” 选项描述选择器的第二行。这个选择器将匹配那些 IP 头部的第二个字节是 0x10 的数据包。你应该猜到了，00ff 就是匹配掩码,确切地告诉过滤器应该匹配哪些位。在这个例子中是 0xff，所以会精确地匹配这个字节是否等于 0x10。 “at”关键字的意思是指出从数据包的第几个字节开始匹配——本例中是从数据 包的开头开始。完全地翻译成人类语言就是:“匹配那些 TOS 字段带有‘最小延迟’属性的数据包”。

让我们看看另一个例子:
```
# tc filter add dev eth0 protocol ip parent 1:0 pref 10 u32 match u32 00000016 0000ffff at nexthdr+0 flowid 1:10
```
“nexthdr”选项意味着封装在 IP 包中的下一个 PDU 的头部,也就是说它的上层协议的头。匹配操作就是从这个协议的头部开始的, 应该发生在头部开始的第 16 位处。在 TCP 和 UDP 协议的头部,这个部分存放的是这个报文的目标端口。数字是按照先高厚低的格式存储的,所以 0x0016 就是十进制的 22(如果是 TCP 的话就是 ssh 服务)。其实,这个匹配在没有上下文的情况下含义很模糊,我们放在后面讨论。

理解了上面的例子之后,下面这条选择器就很好懂了:
```
match c0a80100 ffffff00 at 16
```
表示了：匹配从 IP 头开始数的第 17 个字节到第 19 个字节。这个选择器将匹配所有去往 192.168.1.0/24 的数据包。成功分析完上面这个例子后,我们就已经掌 握 u32 选择器了。

#### 普通选择器

普通选择器定义了要对数据包进行匹配的特征、掩码和偏移量。使用普通选择器, 你实际上可以匹配 IP(或者上层协议)头部的任意一个 bit, 虽然这样的选择器比特殊选择器难读和难写。

一般选择器的语法是:
```
match [ u32 | u16 | u8 ] PATTERN MASK [ at OFFSET | nexthdr+OFFSET]
```
利用 u32、u16 或 u8 三个关键字中的一个来指明特征的 bit 数。然后 PATTERN 和 MASK 应该按照它定义的长度紧挨着写。OFFSET 参数是开始进行比较的偏移量(以字节计)。如果给出了“nexthdr+”关键字,偏移量就移到上层协议头部开始的位置。

一些例子:
```
# tc filter add dev ppp14 parent 1:0 prio 10 u32 match u8 64 0xff at 8 flowid 1:4
```
如果一个数据包的 TTL 值等于 64,就将匹配这个选择器。TTL 就位于 IP 包头的 第 9 个字节。

匹配带有 ACK 位的 TCP 数据包:
```
# tc filter add dev ppp14 parent 1:0 prio 10 u32 \
            match ip protocol 6 0xff \
            match u8 0x10 0xff at nexthdr+13 \
            flowid 1:3
```

用这个匹配小于 64 字节的 ACK 包:
```
# # match acks the hard way,
# # IP protocol 6,
# # IP header length 0x5(32 bit words),
# # IP Total length 0x34 (ACK + 12 bytes of TCP options)
# # TCP ack set (bit 5, offset 33)
# tc filter add dev ppp14 parent 1:0 protocol ip prio 10 u32 \
            match ip protocol 6 0xff \
            match u8 0x05 0x0f at 0 \
            match u16 0x0000 0xffc0 at 2 \
            match u8 0x10 0xff at 33 \
            flowid 1:3
```
这个规则匹配了带有 ACK 位,且没有载荷的 TCP 数据包。这里我们看见了同时使用两个选择器的例子,这样用的结果是两个条件进行逻辑“与”运算。如果我们查查 TCP 头的结构,就会知道 ACK 标志位于第 14 个字节的第 5 个 bit(0x10)。

作为第二个选择器,如果我们采用更复杂的表达,可以写成`match u8 0x06 0xff at 9`,而不是使用特殊选择器 protocol,因为 TCP 的协议号是 6(写在 IP 头的第 十个字节)。另一方面,在这个例子中我们不使用特殊选择器也是因为没有用来匹配 TCP 的 ACK 标志的特殊选择器。

下面这个选择器是上面选择器的改进版,区别在于它不检查 IP 头部的长度。为什么呢？因为上面的过滤器只能在 32 位系统上工作。
```
# tc filter add dev ppp14 parent 1:0 protocol ip prio 10 u32 \
            match ip protocol 6 0xff \
            match u8 0x10 0xff at nexthdr+13 \
            match u16 0x0000 0xffc0 at 2 \
            flowid 1:3
```

#### 特殊选择器

下表是从 tc 程序的源代码中找出的特殊选择器。

##### ip or ip6
```
match [ip | ip6] src IPV4_ADDR/SUBNET_MASK
match [ip | ip6] dst IPV4_ADDR/SUBNET_MASK
match [ip | ip6] protocol NUMBER            # INT_NUM is the protocol number of `tcp` or `udp`.
match [ip | ip6] dport NUMBER               # NUMBER is the destination port of `tcp` or `udp`, etc.
match [ip | ip6] sport NUMBER               # NUMBER is the source port of `tcp` or `udp`, etc.
match [ip | ip6] icmp_type NUMBER           # NUMBER is the type of `ICMP`.
match [ip | ip6] icmp_code NUMBER           # NUMBER is the code of `ICMP`.
```

##### tcp or udp
```
match [tcp | udp] src PORT_NUM
match [tcp | udp] dst PROT_NUM
```

##### icmp
```
match icmp type NUMBER
match icmp code NUMBER
```

#### 一些范例
```
# tc filter add dev ppp0 parent 1:0 prio 10 u32 match ip tos 0x10 0xff flowid 1:4
```
求助: tcp dport match does not work as described below:

上述规则匹配那些 TOS 字段等于 0x10 的数据包。TOS 字段位于数据包的第二个字节,所以与值等价的普通选择器就是:“match u8 0x10 0xff at 1”。这其实给了我们一个关于 U32 过滤器的启示：特殊选择器全都可以翻译成等价的普通选择器,而且在内核的内存中,恰恰就是按这种方式存储的。这也可以导出另一个结论：tcp 和 udp 的选择器实际上是完全一样的,这也就是为什么不能仅用“match tcp dport 53 0xffff”一个选择器去匹配发到指定端口的 TCP 包,因为它也会匹配 送往指定端口的 UDP 包。你一定不能忘了还得匹配协议类型,按下述方式来表示:
```
# tc filter add dev ppp0 parent 1:0 prio 10 u32 \
            match tcp dport 53 0xffff \
            match ip protocol 0x6 0xff \
            flowid 1:2
```

## 路由分类器

这个分类器过滤器基于路由表的路由结果。当一个数据包穿越一个类，并到达一个标有“route”的过滤器的时候,它就会按照路由表内的信息进行分裂。当一个数据包遍历类,并到达一个标记“路由”过滤器的时候,就会按照路由表的相应 信息分类。
```
# tc filter add dev eth1 parent 1:0 protocol ip prio 100 route
```
我们向节点 1:0 里添加了一个优先级是 100 的路由分类器。当数据包到达这个节点时,就会查询路由表,如果匹配就会被发送到给定的类,并赋予优先级 100。要最后完成,你还要添加一条适当的路由项:

这里的窍门就是基于目的或者源地址来定义“realm”。象这样做:
```
# ip route add Host/Network via Gateway dev Device realm RealmNumber
```
例如，我们可以把目标网络 192.168.10.0 定义为 realm 10:
```
# ip route add 192.168.10.0/24 via 192.168.10.1 dev eth1 realm 10
```

我们再使用路由过滤器的时候,就可以用 realm 号码来表示网络或者主机了,并可以用来描述路由如何匹配过滤器:
```
# tc filter add dev eth1 parent 1:0 protocol ip prio 100 route to 10 classid 1:10
```
这个规则说：凡是去往 192.168.10.0 子网的数据包匹配到类 1:10。

路由过滤器也可以用来匹配源策略路由。比如,一个 Linux 路由器的 eth2 上连接了一个子网:
```
# ip route add 192.168.2.0/24 dev eth2 realm 2
# tc filter add dev eth1 parent 1:0 protocol ip prio 100 route from 2 classid 1:2
```
这个规则说：凡是来自 192.168.2.0 子网(realm 2)的数据包, 匹配到 1:2。

## 管制分类器

为了能够实现更复杂的配置,你可以通过一些过滤器来匹配那些达到特定带宽的数据包。你可以声明一个过滤器来来按一定比率抑制传输速率,或者仅仅不匹配 那些超过特定速率的数据包。

如果现在的流量是 5M, 而你想把它管制在 4M, 那么你要么可以停止匹配整个的 5M 带宽,要么停止匹配 1M 带宽,来给所配置的类进行 4M 速率的传输。

如果带宽超过了配置的速率, 你可以丢包、可以重新分类或者看看是否别的过滤器能匹配它。

### 管制的方式

有两种方法进行管制。

如果你编译内核的时候加上了“Estimators”,内核就可以替你为每一个过滤器测 量通过了多少数据,多了还是少了。这些评估对于 CPU 来讲非常轻松,它只不过是每秒钟累计 25 次通过了多少数据,计算出速率。

另一种方法是在你的过滤器内部,通过 TBF(令牌桶过滤器)来实现。TBF 只匹配到达到你配置带宽的数据流,超过的部分则按照事先指定的“越限动作”来处理。

#### 靠内核评估

这种方式非常简单,只有一个参数“avrate”。所有低于 avrate 的数据包被保留, 并被过滤器分到所指定的类中去,而那些超过了 avrate 的数据包则按照越限动作来处理,缺省的越限动作是“reclassify”(重分类)。

内核使用 EWMA 算法来核算带宽, 以防止对瞬时突发过于敏感。

#### 靠令牌桶过滤器

使用下列参数:
* buffer/maxburst
* mtu/minburst
* mpu
* rate

它们的意义与前面介绍 TBF 时所说的完全一样。但仍然要指出的是:如果把一个 TBF 管制器的 mtu 参数设置过小的话,将没有数据包通过, whereas the egress TBF qdisc will just pass them slower。

另一个区别是, 管制器只能够通过或者丢弃一个数据包, 而不能因为为了延迟而暂停发送。

### 越限动作

如果你的过滤器认定一个数据包越限,就会按照“越限动作”来处理它。当前,支持三种动作:

#### continue
    让这个过滤器不要匹配这个包,但是其它的过滤器可能会匹配它。

#### drop
    这是个非常强硬的选项——让越限的数据包消失。它的用途不多,经常被 用于 ingress 管制。
    比如,你的 DNS 在请求流量大于 5Mbps 的时候就会失灵,你就可以利用这个来保证请求量不会超标。

#### Pass/OK
    让数据包通过。可用于避免复杂的过滤器,但要放在合适的地方。

#### reclassify
    最经常用于对数据包进行重分类以达到最好效果。这是缺省动作。

### 范例
```shell
#! /bin/sh -x
#
# sample script on using the ingress capabilities
# this script shows how one can rate limit incoming SYNs
# Useful for TCP-SYN attack protection. You can use
# IPchains to have more powerful additions to the SYN (eg
# in addition the subnet)
#
#path to various utilities;
#change to reflect yours.
#
TC=/sbin/tc
IP=/sbin/ip
IPTABLES=/sbin/iptables
INDEV=eth2
#
# tag all incoming SYN packets through $INDEV as mark value 1
############################################################
$IPTABLES -A PREROUTING -i $INDEV -t mangle -p tcp --syn -j MARK --set-mark 1
############################################################
#
# install the ingress qdisc on the ingress interface
############################################################
$TC qdisc add dev $INDEV handle ffff: ingress
############################################################
#
#
# SYN packets are 40 bytes (320 bits) so three SYNs equals
# 960 bits (approximately 1kbit); so we rate limit below
# the incoming SYNs to 3/sec (not very useful really; but
#serves to show the point - JHS
############################################################
$TC filter add dev $INDEV parent ffff: protocol ip prio 50 handle 1 \
    fw police rate 1kbit burst 40 mtu 9k drop flowid :1
############################################################
#
echo "---- qdisc parameters Ingress ----------"
$TC qdisc ls dev $INDEV
echo "---- Class parameters Ingress ----------"
$TC class ls dev $INDEV
echo "---- filter parameters Ingress ----------"
$TC filter ls dev $INDEV parent ffff:

#deleting the ingress qdisc
#$TC qdisc del $INDEV ingress
```

## 当过滤器很多时如何使用散列表

如果你需要使用上千个规则——比如你有很多需要不同 QoS 的客户机——你可能会发现内核花了很多时间用于匹配那些规则。

缺省情况下,所有的过滤器都是靠一个链表来组织的,链表按 priority 的降序排列。如果你有 1000 个规则,那么就有可能需要 1000 次匹配来决定一个包如何处理。

而如果你有 256 个链表,每个链表 4 条规则的话,这个过程可以更快。也就是说如果你能把数据包放到合适的链表上,可能只需要匹配 4 次就可以了。

利用散列表可以实现。比如说你有 1024 个用户使用一个 Cable MODEM, IP 地址范围是 1.2.0.0 到 1.2.3.255, 每个 IP 都需要不同容器来对待, 比如“轻量级”、“中量级”和“重量级”。你可能要写 1024 个规则,象这样:
```
# tc filter add dev eth1 parent 1:0 protocol ip prio 100 match ip src 1.2.0.0 classid 1:1
# tc filter add dev eth1 parent 1:0 protocol ip prio 100 match ip src 1.2.0.1 classid 1:1
...
# tc filter add dev eth1 parent 1:0 protocol ip prio 100 match ip src 1.2.3.254 classid 1:3
# tc filter add dev eth1 parent 1:0 protocol ip prio 100 match ip src 1.2.3.255 classid 1:2
```

为了提高效率,我们应该利用 IP 地址的后半部分作为散列因子,建立 256 个散列表项。第一个表项里的规则应该是这样:
```
# tc filter add dev eth1 parent 1:0 protocol ip prio 100 match ip src 1.2.0.0 classid 1:1
# tc filter add dev eth1 parent 1:0 protocol ip prio 100 match ip src 1.2.1.0 classid 1:1
# tc filter add dev eth1 parent 1:0 protocol ip prio 100 match ip src 1.2.2.0 classid 1:3
# tc filter add dev eth1 parent 1:0 protocol ip prio 100 match ip src 1.2.3.0 classid 1:2
```
下一个表项应该这么开始:
```
# tc filter add dev eth1 parent 1:0 protocol ip prio 100 match ip src 1.2.0.1 classid 1:1
...
```
这样的话, 最坏情况下也只需要 4 次匹配, 平均 2 次。

具体配置有些复杂, 但是如果你真有很多规则的话,还是值得的。

我们首先生成 root 过滤器,然后创建一个 256 项的散列表:
```
# tc filter add dev eth1 parent 1:0 prio 5 protocol ip u32
# tc filter add dev eth1 parent 1:0 prio 5 handle 2: protocol ip u32 divisor 256
```
然后我们向表项中添加一些规则:
```
# tc filter add dev eth1 protocol ip parent 1:0 prio 5 u32 ht 2:7b: match ip src 1.2.0.123 flowid 1:1
# tc filter add dev eth1 protocol ip parent 1:0 prio 5 u32 ht 2:7b: match ip src 1.2.1.123 flowid 1:2
# tc filter add dev eth1 protocol ip parent 1:0 prio 5 u32 ht 2:7b: match ip src 1.2.3.123 flowid 1:3
# tc filter add dev eth1 protocol ip parent 1:0 prio 5 u32 ht 2:7b: match ip src 1.2.4.123 flowid 1:2
```
这是第 123 项, 包含了为 1.2.0.123、1.2.1.123、1.2.2.123 和 1.2.3.123 准备的匹配规则,分别把它们发给 1:1、1:2、1:3 和 1:2。注意,我们必须用 16 进制来表示散列表项, 0x7b 就是 123。

然后创建一个“散列过滤器”,直接把数据包发给散列表中的合适表项:
```
# tc filter add dev eth1 protocol ip parent 1:0 prio 5 u32 ht 800:: \
            match ip src 1.2.0.0/16 \
            hashkey mask 0x000000ff at 12 \
            link 2:
```
我们定义散列表叫做“800:”, 所有的过滤都从这里开始。然后我们选择源地址(它们位于 IP 头的第 12、13、14、15 字节),并声明我们只对它的最后一部分感兴趣。这个例子中,我们发送到了前面创建的第 2 个散列表项。

这比较复杂,然而实际上确实有效而且性能令人惊讶。注意,这个例子我们也可以处理成理想情况——每个表项中只有一个过滤器!

From: 《Linux 的高级路由和流量控制 HOWTO（中文版）》