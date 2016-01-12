
ETCD
====

[etcd：从应用场景到实现原理的全方位解读](http://www.infoq.com/cn/articles/etcd-interpretation-application-scenario-implement-principle)


## 分布式一致性介绍和Raft算法讲解

http://thesecretlivesofdata.com/raft/

https://github.com/xgfone/raft-zh_cn/blob/master/raft-zh_cn.md

https://ramcloud.atlassian.net/wiki/download/attachments/6586375/raft.pdf


Zookeeper
=========

### 1. 基本讲解与应用场景
http://www.ibm.com/developerworks/cn/opensource/os-cn-zookeeper/

### 2. 永久回调
http://www.cnblogs.com/viviman/archive/2013/03/11/2954118.html

### 3. 异步通知——Watcher
http://zoutm.iteye.com/blog/708468

### 4. 跨中心部署
http://agapple.iteye.com/blog/1184023

### 5. ZooKeeper解惑
http://www.cnblogs.com/gpcuster/archive/2010/12/29/1921213.html

使用服务器集群提高性能只对“`读`”服务有效，对“`写`”服务无效，“`写`”服务器应该使用`主/从`模式，同一时间只使用一台服务器。在“`写`”服务器内部，使用支持`actor模型`的编程语言，保证关键操作的串行。最后老生常谈，支持actor模型的编程语言是：`Erlang`，`Go`，`Scala`，`F#`, etc.

在`多核并行`计算模式下，我认定基于`消息传递`的`actor模型`（源自erlang）是正确的编程方式，在actor模型下，可以简单实现基于服务层的串行操作，保证“`写`”操作的完整和一致。使用`actor模型`，需要用`主/备`的部署架构来消除单点故障，实现`主/备`的部署架构，最简单可靠的方法是使用`zookeeper`。

**`高并发需求`** -> **`异步计算`**(使用actor model) -> **`master/slave`**(使用zookeeper)
