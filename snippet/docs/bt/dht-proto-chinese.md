DHT协议 - 译
============

BitTorrent 使用“分布式哈希表” (DHT) 来存储种子的 peer 信息，且不需要专门的服务器。这样，每一个 peer 都变成一个 tracker。DHT 协议基于 Kademila，且用 `UDP` 实现。

请注意文档中的术语以免产生误解。**_peer 实现了 BitTorrent 协议，既是服务器也是客户端，且监听在 `TCP` 端口。node 实现了 DHT 协议，同样既是服务器也是客户端，监听在 `UDP` 端口。_**DHT 由 node 和 peer 的位置信息构成。BitTorrent 客户端有一个 DHT node，用来和 DHT 中的其他 node 通信用，从而获取 peer 的位置。


## 概览

每一个 node 都有一个全球唯一标识符，称作 node ID。Node ID 是从 160-bit 的空间中随机选取的，这和 BitTorrent 的 infohashes 一致。距离参数（Distance metric）用来比较两个 node ID 之间的接近程度。Nodes 必须维护一个包含其他 node 联系信息的路由表。对那些和自身接近的其他 Node ID，路由表中会有跟多细节。所以 DHT 中，接近自己的 ID 有很多，远的 ID 则较少。

在 Kademila 中，距离参数使用异或计算，结果为无符号整形，即 **`distance(A, B) = | A XOR B |`** 值越小越接近。

当一个 node 想要获取种子的其他 peer 时，它先计算种子的 infohash 和路由表中已有 nodes 的距离参数。然后向距离种子最近的 node 询问 peer 信息。如果恰巧该 node 有，则返回给询问的 node。否则，该 node 把自己路由表中离种子最近的 node 信息返回。本 node 拿到返回信息之后，不停重复上述步骤直到没有新 node 信息返回。搜索结束时，客户端将自己的 peer 信息返回给离种子最近的 node。

peer 查询的返回值必须包含令牌(token)。如果一个 node 宣称自己拥有的 peer 正在下载种子时，必须使用最近接收到的 token。当本 node 试图下载种子时，被请求的 node 检查 IP 地址对应的 token 是否一致。这么做是为了防止恶意主机从其他主机下载种子。由于 token 仅仅由请求 node 返回给被请求 node，故协议并未规定其实现。token 在分发后一段时间内必须被接受。BitTorrent 使用 IP + secret 的 SHA1 值作为 token，每 5 分钟改变一次，有 10 分钟有效期。

## 路由表

每一个 node 维护了一个好 node 的路由表。路由表的中 node 被用作查询的起始节点，并返回查询的响应信息。

并非所有 node 是等价的，有些是“好”的，有些则不。大部分 node 能够使用 DHT 协议发送查询和接受响应，但却不能响应其他 node 的查询。所以在路由表中，必须只包含好的 node。一个好的 node 被定义为能在 15 分钟内响应查询，或者 15 分钟内曾经响应过。若 15 钟没响应，则是可疑的。若对一系列请求都失去响应，则为坏的 node。已知的好的 node 拥有更高的优先级。

路由表覆盖从 0 到 2^160 完整的 node ID 空间。路由表又被分为 bucket，每一个拥有一部分子空间。空的表只有一个 bucket，其 ID 范围为 **`min=0`** 到 **`max=2^160`**。当 ID 为 N 的 node 插入到表中时，它必须放在 **`min=0`** 到 **`max=2^160`** 之间。由于空的表只有一个 bucket，所有 node 都在该 bucket 中。每个 bucket 可以存放 K 个 node，目前 `K <= 8`。当 bucket 存满好的 node 时，不允许再插入，除非其本身就在该 bucket 中。在这种情况下，原 bucket 分裂为两个相同大小的 bucket，比如原始 bucket 分裂为 `0` 到 `2^159`，`2^159` 到 `2^160`。

当 bucket 装满了好的 node，新的 node 会被丢弃。一旦 bucket 中的某个 node 变坏，就会用新的 node 来替换这个坏的 node。如果 bucket 中有在 15 分钟内都没有活跃过的 bucket，则其为可疑的 node，这时我们向最久没有联系的 node 发送 ping。如果有回复，那么我们向下一个可疑的 node 发送 ping，不断这样循环下去，直到有某一个 node 没有给出 ping 的回复，或者当前 bucket 中的所有 node 都是好的 (即都不是可疑节点，且在过去 15 分钟内都有活动)。如果 bucket 中的某个 node 没有对我们的 ping 给出回复，还会再试一次 (再发送一次 ping，也许仍然是活跃的，但由于网络拥塞，所以发生了丢包现象，注意 DHT 的包都是 UDP 的)，而不是立即丢弃该 node 或者直接用新 node 来替代它。这样，路由表中永远是活跃的 node。

每个 bucket 都应该维护一个 lastchange 字段来表明自身的”新鲜”程度。当 bucket 中的 node 被 ping 并给出了回复，或者一个 node 被加入到了 bucket，或者有新的 node 替代了旧的，bucket 的 lastchange 字段都应当更新。如果一个 bucket 的 lastchange 在过去的 15 分钟内都没有变化，那么将重更新它。这个重更新为：从这个 bucket 所覆盖的范围中随机选择一个 node ID，并对这个 ID 执行 find_nodes 搜索。请注意，收到请求的 node 通常不需要常常更新自己所在的 bucket。反之，不常常收到请求的 node 才需要周期性地更新所在 bucket。有了上述措施，在 DHT 时，才能有足够多的好的 node。

当插入第一个 node 到路由表并启动时，这个 node 应试着查找 DHT 中离自己最近的 node。这个查找工作是通过不断的发出 find_node 消息给越来越近的 node 来完成的，当没有更近的 node 时，搜索停止。路由表应当由客户端软件保存。

## BitTorrent 协议扩展

BitTorrent 协议被扩展为可通过 tracker 得到的 peer 之间互换 node 的 UDP 端口号。在这种方式下，当下载种子时，客户端能够自动更新路由表。新安装的客户端在无 tracker 的种子中获取不到路由表，必须在种子文件中找到联系信息。

Peers 如果支持 DHT 协议，会将 BitTorrent 协议握手消息的 8 字节保留位的最后一位置为 1。如果 peer 收到一个握手消息，表明对方支持 DHT 协议，则应该发送 PORT 消息。它由字节 0x09 开始，payload 的长度是 2 个字节，包含了这个 peer 的 DHT 所使用的 UDP 端口号。当 peer 收到这样的消息是应当向对方的 IP 和消息中指定的端口号的节点发送 ping。如果收到了 ping 的回复，则将新 node 的联系信息加入到路由表中。

## 种子文件扩展

无 tracker 的种子文件中不含有 `announce` 关键字，相反，其包含有 nodes 关键字。该关键字应该包含种子创建者路由表的 K 个最近 node。也可以选择设置成已知的可用 node，比如这个种子的创建者。请不要加入 `router.bittorrent.com`。

```
nodes = [["<host>", <port>], ["<host>", <port>], ...]
nodes = [["127.0.0.1", 6881], ["your.router.node", 4804]]
```

## KRPC 协议

KRPC 协议是一个简单的 RPC 通信框架，其在 UDP 上使用 `bencoded` 编码的字典，包含请求与回复，但没有重试。有三种消息类型：**`query`**, **`response`**, **`error`**。对于 DHT 协议来说，有 4 种 `query`: **`ping`**, **`find_node`**, **`get_peers`**, **`announce_peer`**。

KRPC 消息是一个简单字典，包含 **两个** 必填关键字，附加的关键字取决于消息类型。第一个必填关键字是 **`t`**，这是一个字符串表示的 transaction ID。它由请求 node 产生，且包含在回复中，所以回复有可能对应单个 node 的多个请求。transaction ID 应该被编码成字符串表示的二进制数字，通常是两个字符，这样就能包含 `2^16` 种请求。另一个必填关键字是 **`y`**，其对应值表示消息类型，为 **`q`**, **`r`** 或 **`e`**。

### 联系信息编码
peer 的联系信息被编码成 `6` 字节的字符串。`4` 字节为 IP 地址，`2` 字节为端口号，均用 `网络字节序` 表示。

node 的联系信息被编码成 `26` 字节的字符串。`20` 字节为 node ID，剩余为 IP 和端口号信息，均用 `网络字节序` 表示。

### 查询
query 为键值对 **`y:q`**，含有两个附加关键字 **`q`** 和 **`a`**。关键字 q 的值包含了请求类型的字符串表示。关键字 a 的值包含了一个所有返回值的字典。


### 应答
response 为键值对 **`y:r`**，含有一个附加关键字 **`r`**。关键字 r 的值包含了一个所有返回值的字典。

### 错误
error 为键值对 **`y:e`**，含有一个附加关键字 **`e`**。e 为一个列表。第一个元素是整形表示的错误码。第二个元素是字符串表示的错误信息。以下为可能的错误码，

Code    |    Description
--------|--------------
201     |    Generic Error
202     |    Server Error
203     |    Protocol Error, such as a malformed packet, invalid arguments, or bad token
204     |    Method Unknown


示例，
```
generic error = {"t":"aa", "y":"e", "e":[201, "A Generic Error Ocurred"]}
bencoded = d1:eli201e23:A Generic Error Ocurrede1:t2:aa1:y1:ee
```

## DHT查询
所有的 `query` 都有一个键值对 `id:请求 node ID`。所有的 `response` 也有一个键值对 `id:响应的 node ID`。

### ping
最基本的 query 是 `ping`。这时候 `q=ping`，id 为 20 字节网络字节序表示的发送者 node ID。该 query 的响应为 `id=响应者 node ID`。
```
arguments:  {"id" : "<querying nodes id>"}

response: {"id" : "<queried nodes id>"}
```

示例，
```
ping Query = {"t":"aa", "y":"q", "q":"ping", "a":{"id":"abcdefghij0123456789"}}
bencoded = d1:ad2:id20:abcdefghij0123456789e1:q4:ping1:t2:aa1:y1:qe

Response = {"t":"aa", "y":"r", "r": {"id":"mnopqrstuvwxyz123456"}}
bencoded = d1:rd2:id20:mnopqrstuvwxyz123456e1:t2:aa1:y1:re
```

### find_node
find_node 被用来查找给定 ID 的 node 的联系信息。这时 `q == find_node`。find_node 请求包含 **`2`** 个参数，第一个参数是 `id`，包含了请求 node ID。第二个参数是 `target`，包含了请求者正在查找的 node ID。当一个 node 接收到了 find_node 的 query，他应该给出对应的回复，回复中包含 **`2`** 个关键字 `id` 和 `nodes`，nodes 是字符串类型，包含了被请求 node 的路由表中最接近目标 node 的 K(8) 个最接近的 node 的联系信息。
```
arguments:  {"id" : "<querying nodes id>", "target" : "<id of target node>"}

response: {"id" : "<queried nodes id>", "nodes" : "<compact node info>"}
```

示例，
```
find_node Query = {"t":"aa", "y":"q", "q":"find_node", "a": {"id":"abcdefghij0123456789", "target":"mnopqrstuvwxyz123456"}}
bencoded = d1:ad2:id20:abcdefghij01234567896:target20:mnopqrstuvwxyz123456e1:q9:find_node1:t2:aa1:y1:qe

Response = {"t":"aa", "y":"r", "r": {"id":"0123456789abcdefghij", "nodes": "def456..."}}
bencoded = d1:rd2:id20:0123456789abcdefghij5:nodes9:def456...e1:t2:aa1:y1:re
```

### get_peers
get_peers 与种子文件的 infohash 有关。这时 `q=get_peers`。get_peers 请求包含 **`2`** 个参数。第一个参数是 `id`，包含了请求 node 的 ID。第二个参数是 `info_hash`，它代表种子文件的 infohash。如果被请求的 node 有对应 info_hash 的 peers，他将返回一个关键字 `values`，这是一个列表类型的字符串。每一个字符串包含了 Compact IP-address/port info 格式的 peers 信息。如果被请求的 node 没有这个 infohash 的 peers，那么他将返回关键字 `nodes`，这个关键字包含了被请求 node 的路由表中离 info_hash 最近的 K 个 node，使用 Compact node info 格式回复。在这两种情况下，关键字 `token` 都将被返回。之后的 `annouce_peer` 请求中必须包含 `token`。`token` 是一个短的二进制字符串。
```
arguments:  {"id" : "<querying nodes id>", "info_hash" : "<20-byte infohash of target torrent>"}

response: {"id" : "<queried nodes id>", "token" :"<opaque write token>", "values" : ["<peer 1 info string>", "<peer 2 info string>"]}

or: {"id" : "<queried nodes id>", "token" :"<opaque write token>", "nodes" : "<compact node info>"}
```

示例
```
get_peers Query = {"t":"aa", "y":"q", "q":"get_peers", "a": {"id":"abcdefghij0123456789", "info_hash":"mnopqrstuvwxyz123456"}}
bencoded = d1:ad2:id20:abcdefghij01234567899:info_hash20:mnopqrstuvwxyz123456e1:q9:get_peers1:t2:aa1:y1:qe

Response with peers = {"t":"aa", "y":"r", "r": {"id":"abcdefghij0123456789", "token":"aoeusnth", "values": ["axje.u", "idhtnm"]}}
bencoded = d1:rd2:id20:abcdefghij01234567895:token8:aoeusnth6:valuesl6:axje.u6:idhtnmee1:t2:aa1:y1:re

Response with closest nodes = {"t":"aa", "y":"r", "r": {"id":"abcdefghij0123456789", "token":"aoeusnth", "nodes": "def456..."}}
bencoded = d1:rd2:id20:abcdefghij01234567895:nodes9:def456...5:token8:aoeusnthe1:t2:aa1:y1:re
```

### announce_peer
announce_peer 表示某个端口正在下载种子文件。announce_peer 包含 **`4`** 个参数。第一个参数是 `id`，包含了请求 node ID；第二个参数是 `info_hash`，包含了种子文件的 infohash；第三个参数是 `port`， 包含了整型的端口号，表明 peer 在哪个端口下载；第四个参数是 `token`，这是在之前的 `get_peers` 请求中收到的回复中所包含的。收到 `announce_peer` 请求的 node 必须检查这个 token 与回复的 token 是否相同。如果相同，那么被请求的 node 将记录发送者的 IP 和端口号，记录在 peer 联系信息中对应的 infohash 下。
```
arguments:  {"id" : "<querying nodes id>",
"implied_port": <0 or 1>,
"info_hash" : "<20-byte infohash of target torrent>",
"port" : <port number>,
"token" : "<opaque token>"}

response: {"id" : "<queried nodes id>"}
```

示例，
```
announce_peers Query = {"t":"aa", "y":"q", "q":"announce_peer", "a": {"id":"abcdefghij0123456789", "implied_port": 1, "info_hash":"mnopqrstuvwxyz123456", "port": 6881, "token": "aoeusnth"}}
bencoded = d1:ad2:id20:abcdefghij01234567899:info_hash20:<br />
mnopqrstuvwxyz1234564:porti6881e5:token8:aoeusnthe1:q13:announce_peer1:t2:aa1:y1:qe

Response = {"t":"aa", "y":"r", "r": {"id":"mnopqrstuvwxyz123456"}}
bencoded = d1:rd2:id20:mnopqrstuvwxyz123456e1:t2:aa1:y1:re
```

------

From: http://www.lyyyuna.com/2016/03/26/dht01/

Reference: http://www.bittorrent.org/beps/bep_0005.html

