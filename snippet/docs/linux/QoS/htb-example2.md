
### 第一步：在部署时，初始化环境
##### 清理掉网卡的上所有旧规则
```shell
tc qdisc del dev vnet0 root      # 清空根队列
tc qdisc del dev vnet0 ingress   # 清空入口流量控制规则
```
注：可能会报错，这是正常的，原因是：没有相应的规则，在清除时，会报错。
我们这里是在网卡 `vnet0` 上添加 TC 规则，下同。实际情况下，要换成正确的网卡名。

##### 初始化默认的队列、分类
```shell
tc qdisc add dev vnet0 root handle 1:0 htb default 0xff
```
创建根队列，并绑定为HTB分类，以及默认分类（`1:0xff`）——如果没有匹配的规则，则匹配的默认分类器（`1:0xff`）中。

```shell
tc class add dev vnet0 parent 1:0 classid 1:1 \
    htb rate 1048576kbps ceil 1048576kbps burst 1597b cburst 1597b
```
在根队列中添加一个总的分类（`1:1`），用来作为总的流量控制——这里的样例为 1GB。

注：单位 `kbps` 为 `千字节/秒`，即 `1000 bytes/s`，不是 `1024 bytes/s`。不建议使用 `kbit`（`1000 bits/s`）作为单位。下同。

`burst` 和 `cburst` 的值不需要另外更改，可以把它们作为一个定值。这里只需要更改 `rate` 和 `ceil` 的参数值即可。下同。

```shell
tc class add dev vnet0 parent 1:1 classid 1:0xff \
    htb rate 10240kbps ceil 10240kbps burst 1597b cburst 1597b
```
添加默认分类（`1:0xff`），并限速为 10MB/s。

```shell
tc qdisc add dev vnet0 parent 1:0xff handle 0xff:0 pfifo limit 500
```
更改默认分类的队列——将其队列设置为 `pfifo`（以`包`为单位的先入先出类型），并且队列的长度为 500 （个数据包）。

注：`pfifo`中的 p 表示 package，即该队列以数据包为单位进行计算；如果是 `bfifo`，则以`字节`为单位进行计算。

```shell
tc qdisc add dev vnet0 ingress
```
添加入口流量控制。

##### 添加默认分类器
```shell
tc filter add dev vnet0 parent 1:0 pref 5 protocol ip u32
```
添加 root 过滤器。

```shell
tc filter add dev vnet0 parent 1:0 pref 5 protocol ip handle 2: u32 divisor 256
```
创建一个 256 项的散列表，其哈希表为 2。

```shell
tc filter add dev vnet0 parent 1:0 pref 5 protocol ip u32 ht 800:: \
                        match ip src 0.0.0.0/0 \
                        hashkey mask 0x000000ff at 12 \
                        link 2:0
```
创建一个“散列过滤器”，直接把数据包发给散列表中的合适表项。

大意是：创建一个哈希表800，根据源地址的最后一个字节（如：192.168.10.11中的11）进行散列——这样分散地更加均匀，然后链接 到哈希表2中（即在2中却查找）。


### 第二步：为VM绑定网络带宽
注意：

    上层首先要为VM分类一个FlowID（整数值），该值全局唯一。
    FLOWID 是一个 32 位整数，并且必须用十六进制形式表示。

建议：

    可以使用VM的内网IP的整数值作为FlowID；如果前两个字节都相同的话，也可以只使用后两个字节的整数值。

```shell
tc class add dev vnet0 parent 1:1 classid 1:${FLOWID} \
    htb rate 2048kbps ceil 2048kbps burst 1597b cburst 1597b
```
为VM创建一个分类（`1:${FLOWID}`），并限速为 2MB/s。

```shell
tc qdisc  add dev vnet0 parent 1:${FLOWID} handle ${FLOWID}:0 pfifo limit 500
```
更改VM分类的默认队列——将其设置为 `pfifo`，将限制队列长度为 500 （个数据包）。

```shell
tc filter add dev vnet0 parent 1:0 pref 5 protocol ip u32 ht 2:${ip_4}: \
                        match ip src ${ip}/32 \
                        flowid 1:${FLOWID}
```
为VM添加过滤器——将与该VM有关的数据包全部匹配到分类（`1:${FLOWID}`）中。

注：`match ip src` 中的 `src` 和 网卡 `vnet0` 及 `${ip}`相关，具体匹配如下：

  序号  |   网卡   |   src/dst  |     IP
-------|---------|-------------|---------
   1   |  内网卡  |     dst     |  内网IP
   2   |  外网卡  |     src     |  外网IP

**说明：**

    ${ip}为IPv4地址的字符串表示，如：192.168.10.11。
    ${ip_4}表示IPv4地址的最后一个字节（十六进行的整数值），我们用它的最大范围（256）来表示位桶大小。
    ${ip_4}的范围应该是 0~255。


### 第三步：删除VM的带宽控制
    必须先删除 Filter，然后才能删除 Class。
    每个 `${HANDLE}` 唯一地表示一个 Filter。

```shell
tc filter del dev vnet0 parent 1:0 pref 10 protocol ip handle ${HANDLE} u32
```
删除VM的过滤器——由过滤器的句柄 `${HANDLE}` 来标识。

```shell
tc class  del dev vnet0 parent 1:1 classid 1:${FLOWID} htb rate 50kbit
```
删除VM的分类（`1:${FLOWID}`）。

注：为VM分配的 qdisc 不用删除了，因为它属于分类 `1:${FLOWID}`，而当删除一个分类时，该分类会自动删除属于它的所有子类及其相关的东西。

##### ${HANDLE}的查找方法
(1) 首先根据分类句柄（`1:${FLOWID}`）得到与之有关的过滤器行信息。
```
$ tc filter list dev vnet0 | grep '1:10'
filter parent 1: protocol ip pref 5 u32 fh 2:e0:800 order 2048 key ht 2 bkt e0 flowid 1:10
filter parent 1: protocol ip pref 5 u32 fh 2:fa:800 order 2048 key ht 2 bkt e0 flowid 1:10
```

(2) 然后从上述各行中提取出形如 `XXX:XXX:XXX` 的字符串，此即为 `${HANDLE}`。

(3) 最后根据各个 `${HANDLE}`，依次调用上述删除Filter命令——删除相应的Filter。

### 其它
##### 更换已存在VM的带宽限制
```shell
tc class replace dev vnet0 parent 1:1 classid 1:${FLOWID} \
    htb rate 20480kbps ceil 20480kbps burst 1597b cburst 1597b
```
将上面的 `add` 替换 `replace`，然后更换 `rate` 和 `ceil` 的参数值即可。

**参数值：**

上述要根据具体情况，具体填写的值：`rate` 和 `ceil`的参数值。

上述可能更改的默认值（可以作为定值存在）：`burst`、`cburst` 和 `limit` 的参数值。

注：`ceil` 为流量借用，我们在这和 `rate` 设置一样的值（即不允许借用）；这里可以不用指定，默认和`rate`的值一样。不过，建议这里显示指定`ceil`的值，这样一来，如果以后要支持流量借用，不 用改变代码，只需要传递不同的参数即可。另外，`rate` 有一定的损失率，即流量不可能`100%`的达到`rate`指定的值；根据简单的测试，上调 5%～10% 即可（上调到10%时，用户可以明显看到它的带宽稍微高于它购买的带宽，大约在 4% 左右）。

### 说明
以上形如：`XXX:`、`XXX::`、`XXX:XXX`、`XXX:XXX:`、`XXX:XXX:XXX` 都是`十六进制`形式的整数，前面省略 `0x`，如：

    800:
    800::
    2:1
    2:1:
    2:1:ab
    2:1:0xab
    0x2:1:0xab

都是合法的。

`CLASSID` 的完整形式是 `XXX:YYY`，其中 `XXX`是`major`，`YYY`是`minor`。`XXX:` 或 `XXX:0` 为 `QDisc`（如上述的`1:0`）， 其它情况为 `CLASS`（如上述的`1:1`及`1:${FLOWID}`）。

`FILTERID` 的完整形式是 `XXX:YYY:ZZZ`，其中，`XXX`是哈希表项（从`0x001`到`0xfff`，就相当于可以生成`0xfff`个哈希变量）；`YYY`是哈希表`XXX`的 `Bucket`，取值范围为 `0`到`位桶大小减1`，`YYY`最大为 `255`（也就是说，_**哈希表的位桶最大是256，且位桶的值要求是2的次幂，即创建哈希表时，只能指定 1、2、4、8、16、32、64、128、256**_）；`ZZZ`是`Bucket`的 `Item`。因此，可以把TC中的哈希表看成是“`哈希链表`”，XXX表示哈希链表变量，YYY表示Bucket号，ZZZ表示相应的Bucket中Item 的序号，这就唯一索引到一个元素（这里即是过滤器Filter）。

### 脚本
```shell
#!/bin/sh

ETH=$1
FLOWID=$2

###### INIT ######
# Clean
tc qdisc del dev ${ETH} root
tc qdisc del dev ${ETH} ingress

# Add the defalut qdisc and the default HTB class
tc qdisc add dev ${ETH} root handle 1:0 htb default 0xff
tc class add dev ${ETH} parent 1:0 classid 1:1 \
         htb rate 1048576kbps ceil 1048576kbps  burst 1597b cburst 1597b
tc class add dev ${ETH} parent 1:1 classid 1:0xff \
         htb rate 10240kbps ceil 10240kbps burst 1597b cburst 1597b
tc qdisc add dev ${ETH} parent 1:0xff handle 0xff:0 pfifo limit 500
tc qdisc add dev ${ETH} ingress

# Add the default filter
tc filter add dev ${ETH} parent 1:0 pref 5 protocol ip u32
tc filter add dev ${ETH} parent 1:0 pref 5 protocol ip handle 2: u32 divisor 256
tc filter add dev ${ETH} parent 1:0 pref 5 protocol ip u32 ht 800:: \
                         match ip src 0.0.0.0/0 hashkey mask 0x000000ff at 12 link 2:0

###### Add ######
#tc class  add dev ${ETH} parent 1:1 classid 1:${FLOWID} \
#          htb rate 2048kbps ceil 2048kbps burst 1597b cburst 1597b
#tc qdisc  add dev ${ETH} parent 1:${FLOWID} handle ${FLOWID}:0 pfifo limit 500
#tc filter add dev ${ETH} parent 1:0 pref 5 protocol ip u32 ht 2:${ip_4}: \
#                         match ip src ${ip}/32 flowid 1:${FLOWID}

###### Delete ######
#tc filter del dev ${ETH} parent 1:0 pref 10 protocol ip handle ${HANDLE} u32
#tc class  del dev ${ETH} parent 1:1 classid 1:${FLOWID} htb rate 50kbit
```
执行脚本：
```shell
bash init-tc.sh vnet0
```
