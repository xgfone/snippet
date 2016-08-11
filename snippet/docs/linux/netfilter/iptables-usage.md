Linux iptables使用入门
======================

## iptables的概述

netfilter/iptables 是在 linux 2.4 及后继版本的内核中集成的一种服务，其工作在 osi 七层模型的二、三层。

netfilter/iptables 由 netfilter 组件和 iptables 组件构成，其中 netfilter 组件集成在内核的一部分，由一些信息包过滤表组成，这些表包含内核用来控制信息包过滤处理的规则集。

其模块位于 `/lib/modules/$(uname -r)/kernel/net/netfilter/`，iptables 组件是一种开发工具，它运行于用户空间，它使插入、修改和除去信息包过滤表中的规则变得容易。

## iptables中表和链

### 表和链的概述
iptables 包括 `3` 个表，即：`filter表`、`nat表`、`mangle表`，它们分别代表对经过 iptables 的数据包进行 `筛选(filter)`、`转译(nat)`、`改写(mangle)`。

iptables 包括 `5` 个链，即：`input链`、`forward链`、`output链`、`prerouting链`、`postrouting链`。

- `mangle表` 包括全部的 `5` 个链。
- `nat表` 包括 `prerouting链`、`output链`、`postrouting链`。
- `filter表` 包括 `forware链`、`input链`、`output链`。

### 表和链的功能

#### filter表
filter表主要用于过滤数据包，对数据包进行 `accept`、`drop`、`reject`、`log`等操作。

filter表包含以下 3 条链：
- `input链`：过滤所有目标地址是本机的数据包。
- `forward链`：过滤所有路过本机的数据包，也就是目的地址和源地址都不是本机的数据包。
- `output链`：过滤所有由本机产生的数据包，也就是源地址是本机的数据包。

#### nat表
nat表用于网络地址转换。

iptables可以进行以下的nat：
- `dnat`：主要用于改变数据包的目的地址，以使数据包能重新路由到某台主机。
- `snat`：主要用于改变数据包的源地址，以帮助内部网络能连接到 internet。
- `masquerade`：和 snat 完全一样，只是 masquerade 会查找可用的 ip 地址，而不像 snat 要有一个固定的 ip，所以 masquerade 一般用于 adsl/ppp 等拔号共享上网的方式.

nat表包含以下3条链：
- `prerouting链`：可以在数据包到达防火墙的时候改变包的目标地址。
- `output链`：可以改变本地产生的数据包的目标地址。
- `postrouting链`：在数据包就要离开防火墙的时候改变数据包的源地址。

#### mangle表
mangle表主要用于修改数据包，通过 mangle 可以根据需要改变包头中的内容（如ttl、tos、mark）。

mangle表主要有以下几种操作：
- `tos`：主要用于设置或改变数据包的服务类型域。
- `ttl`：主要用于改变数据包的生存时间域，可以让所有的数据包只有一个特殊的 ttl，这样可以欺骗一些 ISP，比如 ISP 不希望看到共享上网的情况。
- `mark`：主要用于给数据包设置特殊的标记，通过这些标记可以配置带宽限制和基于请求的分类，不过 mark 并没有真正改动数据包，它只是在内核空间中为包设置了标记，防火墙通过其标记对包进行过滤和高级路由。

mangle表包含全部5条链。

**注意：**

iptables 的所有链里有 3 条链是可以改变数据包的目的地址及源地址的，分别是 `nat表的prerouting链`、`nat表的postrouting链` 和 `nat表的output链`。

### 工作流程
#### 当数据包的目标地址是本机时

1. 数据包进入网络接口。
2. 进入 mangle 表的 prerouting 链，在这里可以根据需要改变数据包头内容(比如数据包的 ttl 值)。
3. 进入 nat 表的 prerouting 链，在这里可以根据需要做 dnat(目标地址转换)。
4. 进行路由判断(进入本地还是要转发)。
5. 进入 mangle 表的 input 链，在路由之后到达本地程序之前修改数据包头内容。
6. 进入 filter 表的 input 链，所有目标地址是本机的数据包都会经过这里，可以在这里对数据包的过滤和件进行设置。
7. 到达本地应用开发程序处理。

#### 当数据包的源地址是本机时

1. 本地应用开发程序产生数据包。
2. 路由判断。
3. 进入 mangle 表的 output 链，在这里可以根据需要改变包头内容。
4. 进入 nat 表的 output 链，在这里可以根据需要对防火墙产生的数据包做 dnat。
5. 进入 filter 表的 output 链，在这里可以对数据包的过滤条件进行设置。
6. 进入 mangle 表的 postrouting 链，这里主要对数据包做 dnat 操作，数据包离开本机之前修改数据包头内容。
7. 进入 nat 表的 postrouting 链。在这里对数据包做 snat(源地址转换)。
8. 离开本地。

#### 经过本机转发的数据包((源地址、目标地址都不是本机)

1. 数据包进入网络接口。
2. 进入 mangle 表的 prerouting 链，在这里可以根据需要修改数据包头内容(如 ttl 值)。
3. 进入 nat 表的 prerouting 链，在这里可以根据需要对数据包做 dnat。
4. 进入路由判断(进入本地还要转发)。
5. 进入 mangle 表的 forward 链，在这里数据包头内容被修改。这次 mangle 发生在最初的路由判断之后，在最后一次更改数据包的目标之前。
6. 进入 filter 表的 froward 链，只有需要转发的数据包才会到达这里，并且针对这些数据包的所有过滤也在这里进行，即所有转发的数据都要经过这里。
7. 进入 mangle 表的 postrouting 链，这个链也是针对一些特殊类型的数据包，这一步修改数据包内容是在所有包的目的地址的操作完成之后才进行。
8. 进入 nat 表的 postrouting 链，在这里可以根据需要对数据包做 snat，当然也包括 masquerade(伪装)，但不进行过滤。
9. 离开网络接口。

### iptables的状态机制

在 iptables 中数据包和被跟踪连接的 4 种不同状态相关联，这4种状态分别是 `new`、`established`、`related`、`invalid`。

除了本地产生的包由 `output` 链处理外，所有连接跟踪都是在 `prerouting` 链里进行处理的。

如果本机发送一个流的初始化包，状态就会在 `output` 链里被设置为 `new`。当我们收到回应的包时，状态就会在 `prerouting` 链里设置为 `established`。

#### `new` 状态
`new` 状态的数据包说明这个数据包是收到的第一个数据包，比如收到一个 syn 数据包，这是连接的第一个数据包，就会匹配 new 状态。

#### `established` 状态
只要发送并接到应答，一个数据连接就从 `new` 变为 `established`，而且该状态会继续匹配这个连接的后继数据包。说白了 `established` 表示的就是一个已经连接成功的状态。

#### `related` 状态
当一个连接和某个已处于 `established` 状态的连接有关系时，就被认为是 `related`，也就是说一个连接要想是 `related` 的，首先要有一个 `established` 的连接。

其实 `related` 状态是最常用到的，即这个数据包与我们主机发送出去的封包有关的就是 `related` 状态的数据包。

#### `invalid` 状态
`invalid` 状态表示无效的数据包。

**说明:**

不管是 `tcp/udp` 还是 `icmp`，请求被认为 `new`，应答是 `established`。也就是说，当防火墙看到一个请求包时，就认为连接处于 `new` 状态，当有应答时，就是 `established` 状态。


## iptables 的应用开发

### iptables 的命令格式如下
```
iptables [-t table] command [match] [target|jump]
```

如：`iptables -t filter -a INPUT -s 192.168.0.200 -j drop`。

- `[-t table]`：指明需要操作的表，可以指定的表包括 `filter`、`nat`、`mangle`，不指定该参数默认操作 `filter` 表。
- `command`：iptables 所作的操作，比如增加一条规则或者删除一条已存在的规则。
- `[match]`：指定一个数据包的源地址、目的地址、所使用的协议、端口等。
- `[targe/jump]`：如果数据包符合 `match` 的描述，就需要使用 `targe/jump` 定义的目标或跳转来处理数据包，比如是丢弃还是发送给其它链。

### iptables 可用的操作

#### `-L`：显示所有链的所有策略，如果没有指定表,则显示   filter 表的所有链
```
iptables -L
iptables -t filter -L
```

#### `-A <链名称>`：在所选择的链最尾部添加一条新的策略
```
iptables -t filter -A INPUT -s 192.168.75.129 -j DROP
```

#### `-D <链名称> <策略内容|策略序号>`:删除一条策略

增加一条策略：
```
$ iptables -t filter -A INPUT -s 192.168.75.129 -j DROP
```

查看 filter 表里的所有策略，并输出策略号：
```
$ iptables -t filter -L --line-numbers
chain input (policy accept)
num target prot opt source destination
1 drop all -- 192.168.75.129 anywhere
2 drop all -- 192.168.75.130 anywhere

chain forward (policy accept)
num target prot opt source destination

chain output (policy accept)
num target prot opt source destination
```

我们删除第二条 filter 表的 INPUT 策略：
```
iptables -t filter -D INPUT 2
```

**注意：**

如果我们建了两条一样的策略，比如它们的策略号为 1 和 3，这样我们不指定策略号删除策略时，是从后面的策略号删起。如果我们删除策略号为 1 的策略，后面的策略会向前面递进减 1。

#### `-R <链名称> <策略序号>`：替换所选中链指定的策略
```
iptables -t filter -R INPUT 1 -s 192.168.75.131 -j DROP
```

#### `-I <链名称> [<策略序号>]`：从所选链中指定策略前面插入一条新的策略
```
iptables -t filter -I INPUT 1 -s 192.168.75.130 -j DROP
```

#### `-F [链名称]`：清空所选链的策略,如果没有指定链,则清空指定表中的所有链的策略
```
iptables -t filter -F INPUT
```

#### `-Z [链名称]`：将所选链的所有计数器归零,如果没有指定链,则清空指定表中的所有链的策略
```
iptables -t filter -Z INPUT
```

#### `-N <链名称>`：根据用户指定的名字建立新的链
```
iptables -t filter -N NEW_CHAIN_NAME
```

#### `-X [链名称]`：删除指定的用户自定义键,如果没有定义键名称,则删除所有自定义链
```
iptables -X
```

#### `-E <旧链名称>  <新链名称>`：对自定义的链进行重命名

注意：仅仅是改变自定义链的名字，对整个表的结构和工作没有任何影响。

#### `-P <链名称> <目标>`：为链设置默认的策略,即所有不符合策略的数据包都被强制使用这个策略
```
iptables -t filter -P INPUT ACCEPT
```

### iptables 可用的数据描述

#### `[!] -p [<tcp|udp|icmp|...>]`：匹配指定的协议

- 名字不区分大小写，但必须在 `/etc/protocols` 中定义过。
- 可以使用协议对应的整数值(比如 icmp 的值是 1，tcp 是 6，udp 是 17)。
- 当不使用 `-p` 参数指定协议时，默认为 `all`(数值为 `0`)，但要注意这只代表匹配 `tcp`、`udp`、`icmp`，而不是 `/etc/protocols` 中定义所有协议。
- 在指定协议时，可以在协议前加感叹号表示取反(感叹号与协议名之间必须有空格)。

如：
```
iptables -t filter -A INPUT -p icmp -s 192.168.75.129 -j DROP
iptables -t filter -A INPUT ! -s 192.168.75.1 -j DROP
```

#### `-s <ip地址/网段>`：匹配指定源地址的ip/mask

```
iptables -t filter -A INPUT -s 192.168.75.0/24 -p icmp -j DROP
```

#### `-d <ip地址/网段>`：匹配指定的ip目标地址匹配数据包

```
iptables -t filter -A OUTPUT -d 192.168.75.129 -p icmp -j DROP
```

#### `-i <网络接口>`：以数据包进入本地所使用的网络

这个匹配操作只能用于 `input`、`forward` 和 `prerouting` 这 3 个链。

注意：
- 指定时使用网络接口名称，比如 `eth0`、`ppp0` 等。
- 我们也可以用 `! -i eth0` 的方式进行取反匹配。
- 可以使用 `加号` 作为通配符。
- 我们也可用了 `eth+` 表示所有 `ethernet` 接口。

#### `-o <网络接口>`：以数据包离开本地所使用的网络接口来匹配数据包

注：其配置方案与 `-i` 是一样的。


#### `--sport <端口>`：基于数据包的源端口来匹配数据包

- 该参数必须与 `-p` 参数配合使用。
- 不指定 `--sport` 参数时，表示所有端口。
- 可以使用连续的端口，比如：`--sport 1000:1024` 表示从 1000 到 1024 的所有端口(包括 1000 和 1024)。`--sport 1024:1000` 与 `--sport 1000:1024` 的效果相同。
- 当省略冒号前面的端口号时，比如 `--sport :1000`，则表示使用 0 到 1000 的所有端口(端口号是从 0 算起的)。
- 当省略冒号后面的端口号时，比如 `--sport 1000:`，则表示从 1000 到 65535 的所有端口(端口号最大为 65535)。
- 当在 `--sport <端口号>` 前加入 `!` 号时，表示排除该端口，比如 `! --sport 1000`，则表示除 1000 之外的所有端口。

```
iptables -t filter -A INPUT -p tcp --sport 20000:65535 -s 192.168.75.129 -j DROP
iptables -t filter -A INPUT -p tcp ! --sport 0-1000 -s 192.168.75.129 -j DROP
```

#### `--dport <端口>`：基于数据包的目的端口来匹配包,也就是说匹配目的主机连接本机的哪个端口

注：其操作方面与 `--sport` 参数相同。

#### `-m multiport --sport <端口>`：源端口多端口匹配

注：其作用同 `--sport` 一样。

- 最多可以指定 `15` 个端口，使用逗号分隔。
- 该参数必须与 `-p` 参数配合使用。

```
iptables -t filter -A INPUT -m multiport -p tcp --sport 40000,50000 -s 192.168.75.129 -j DROP
```

#### `-m multiport --dport <端口>`：目的端口多端口匹配

注：其作用同 `--dport` 一样。

- 最多可以指定 `15` 个端口，使用逗号分隔。
- 该参数必须与 `-p` 参数配合使用。


#### `-m multiport --port <端口>`：过滤条件包括源端口和目标端口

```
iptables -t filter -A INPUT -p tcp -m multiport --port 22,56000 -s 192.168.75.129 -j DROP
```

#### `--tcp-flags <检查标记列表>  <条件列表>`：匹配指定的tcp标记

它有两个参数，它们都是列表。列表内容用英文的逗号作分隔符，两个列表之间用空格分开。如：`--tcp-flags syn,fin,ack syn`。

第一个列表指定需要检查的 tcp 标记，第二个列表指定在第一个列表中出现过的且必须被设为 1 (即打开状态)的标记。也就是说第一个列表提供检查范围，第二个列表提供被设置条件。这个匹配操作可以识别 `syn`、`ack`、`fin`、`rst`、`urg`、`psh` 等标记。

```
iptables -t filter -A INPUT -p tcp --tcp-flags syn,fin,ack syn -s 192.168.75.129 -j DROP
```

#### `--syn`：匹配 `syn` 标记被设置而 `ack/rst` 标记没有设置的数据包

该参数与 `iptables -p tcp --tcp-flags syn,rst,ack syn` 有相同的效果。

```
iptables -t filter -A INPUT -p tcp --syn -s 192.168.75.129 -j DROP
```

#### `--icmp-type <类型数值>`：根据 icmp 类型匹配包

注：类型的指定可以使用十进制数值。

```
iptables -t filter -A INPUT -p icmp --icmp-type 8 -j DROP
iptables -t filter -A INPUT -p icmp --icmp-type 0 -j DROP
```

#### `--limit <匹配次数/时间>`

- 匹配操作必须由 `-m limit` 明确指定才能使用。
- 该参数用于控制某条规则在一段时间的匹配次数。
- 时间单位可以是 `秒(second/s)`、`分钟(minute/m)`、`小时(hour/h)`。

```
iptables -t filter -A INPUT -p icmp -m limit --limit 1/m -j ACCEPT
iptables -t filter -A INPUT -p icmp -j DROP
```

#### `--limit-burst <次数>`：定义 `--limit` 的峰值

注：可以理解为允许建立连接的阈值。

```
iptables -t filter -A INPUT -p icmp -m limit --limit-burst 50 -j ACCEPT
iptables -t filter -R INPUT 1 -p icmp -m limit --limit 5/m --limit-burst 50 -j ACCEPT
iptables -t filter -A INPUT -p icmp -j DROP
```

#### `--mac-source <mac地址>`：基于数据包的源 `mac` 地址匹配数据包

注：只能用于 `prerouting`、`forward`、`input`三个链。

```
iptables -t filter -A INPUT -m mac --mac-source 00:0c:29:df:13:e6 -j DROP
```

#### `--uid-owner <uid>`：按生成包的用户 `id(uid)` 来匹配数据包

```
iptables -t filter -A OUTPUT -p icmp -m owner --uid-owner 500 -j DROP
```

#### `--gid-owner <gid>`：按生成包的用户组 `id(gid)` 来匹配数据包

```
iptables -t filter -A OUTPUT -m owner --gid-owner 500 -j DROP
```

#### `--state <状态列表>`：匹配数据包的状态

多个状态使用逗号号分隔，tos 在网络设备上传输也需要网络设备的支持，否则对其优化也是没有效果的。

```
iptables -t filter -A INPUT -m state --state new,established -p tcp --dport 22 -s 192.168.75.129 -j ACCEPT
iptables -t filter -A INPUT -s 192.168.75.129 -j DROP
```

#### `--tos <tos值>`：根据 tos 字段匹配数据包

```
# 针对ssh服务,我们设置它为最小延时
iptables -A PREROUTING -t mangle -p tcp --dport ssh -j tos --set-tos minimize-delay

# 针对ftp服务,我们设置它为最大合理量
iptables -A PREROUTING -t mangle -p tcp --dport ftp -j tos --set-tos maximize-throughput

# 针对snmp服务,我们设置它为最大可靠度
iptables -A PREROUTING -t mangle -p tcp --dport snmp -j tos --set-tos maximize-reliability

# 针对icmp协议,我们采用最小花费
iptables -A PREROUTING -t mangle -p icmp -j tos --set-tos minimize-cost
```

#### `--ttl <TTL值>`：根据 ttl 的值来匹配数据包.

```
iptables -A INPUT -m ttl --ttl 64 -s 192.168.75.129 -j DROP
```

### iptables 可用动作

#### `ACCEPT`
`-j ACCEPT` 表示一旦数据包满足了指定的匹配条件，就会被允许，并且不会再去匹配当前链中的其他规则或同一个表内的其他规则，但它还要通过其它表中的链。

#### `dnat/snat/masquerade`

- `dnat`：用于进行目标网络地址转换，也就是重写数据包的目标 ip 地址，`dnat` 只能在 `nat` 表里的 `prerouting` 和 `output` 链中使用。
- `snat`：用于进行源网络地址转换，也就是重写数据包的源 ip 地址，`snat` 只能在 `nat` 表里的 `postrouting` 链中使用。
- `masquerade`：该选项与 `snat` 作用相同，只是使用该选项时不需要指明 `--to-source`。一般 `masquerade` 用于动态获取 ip 地址的链接。

```
iptables -t nat -A PREROUTING -p tcp -d 192.168.75.128 --dport 22 -s 192.168.75.129 -j dnat --to-dest 192.168.75.131:22
iptables -t nat -A POSTROUTING -p tcp -d 192.168.75.131 -s 192.168.75.129 --dport 22 -j snat --to-source 192.168.75.128
iptables -t nat -A POSTROUTING -p tcp -d 192.168.75.131 -s 192.168.75.129 --dport 22 -j masquerade
```

#### `DROP/REJECT`

- `drop`：如果数据包符合条件，这个目标就会把它阻止，但它不会向发送者返回任何信息，这就有可能会使连接的另一个方 socket 一直等待回应。
- `reject`：同 `drop` 一样，但它会在丢弃包的同时还会向发送者返回一个错误信息。

注：`drop` 和 `reject` 不会向 `accept` 那样可以通过若干个表，在匹配到数据包时，会直接拒绝，而不会让其继续前进。

```
iptables -t filter -A INPUT -s 192.168.75.129 -p icmp -j DROP
iptables -t filter -R INPUT 1 -s 192.168.75.129 -p icmp -j REJECT
```


#### `log`
如果数据包符合条件，就记录数据包的相关信息到 log 文件。

```
iptables -t filter -A INPUT -p icmp -j log --log-level debug
iptables -t filter -A INPUT -p icmp -j log --log-prefix "hacker"
```

------

From: http://www.makaidong.com/%E5%8D%9A%E5%AE%A2%E5%9B%AD%E7%89%9B/14535.shtml
