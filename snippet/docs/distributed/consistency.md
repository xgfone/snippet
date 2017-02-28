# 分布式一致性原理

## Paxos

1. [The Part Time Parliament](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/The-Part-Time-Parliament.pdf)
2. [Paxos Simple](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/paxos-simple-Copy.pdf)

**注：**1990年，Lamport 把上面第一篇论文交给 ACM TOCS 的评委，但由于该论文是以故事形式而非严谨的数学证明来阐述的，且 Lamport 又拒绝做任何修改，因此，该篇论文没有被接受。其后，MIT 的 Nancy Lynch 根据 Lamport 的原文用数学的形式化术语重新定义并证明了 Paxos 算法。于是，1998 年，ACM TOCS 终于接受了 Lamport 的论文。后来，Lamport 本人作出让步，于 2001 年放弃了故事的描述方式，而使用了通俗易懂的语言重新讲述了原文，即上面的第二篇论文。虽然如此，但第二篇论文坚持不需要数学来协助描述，因此，您会看到整篇文章中没有任何数学符号；不同的是，第二篇论文比第一篇更加通俗易懂了。

### 经典实现

#### Chubby
Chubby 是 Google 根据 Paxos 算法实现的分布式锁服务，用于 GFS 和 Big Table 等大型系统的分布式协作。

#### ZooKeeper
ZooKeeper 由 Apache Hadoop 的子项目发展而来，于 2010 年 11 月成为 Apache 的顶级项目。 ZooKeeper 为分布式应用提供了高效且可靠的分布式协调服务，提供了诸如统一命名服务、配置管理和分布式锁等分布式的基础服务。但是，在解决分布式数据一致性方面，ZooKeeper 并没有直接采用 Paxos 算法，而是采用了一种称为 ZAB(ZooKeeper Atomic Broadcast，ZooKeeper原子消息广播协议) 的一致性协议。ZAB 是 Paxos 的变体或简化。

1. [基本讲解与应用场景](http://www.ibm.com/developerworks/cn/opensource/os-cn-zookeeper)
2. [永久回调](http://www.cnblogs.com/viviman/archive/2013/03/11/2954118.html)
3. [异步通知——Watcher](http://zoutm.iteye.com/blog/708468)
4. [跨中心部署](http://agapple.iteye.com/blog/1184023)
5. [ZooKeeper解惑](http://www.cnblogs.com/gpcuster/archive/2010/12/29/1921213.html)

使用服务器集群提高性能只对“`读`”服务有效，对“`写`”服务无效，“`写`”服务器应该使用`主/从`模式，同一时间只使用一台服务器。在“`写`”服务器内部，使用支持`actor模型`的编程语言，保证关键操作的串行。最后老生常谈，支持actor模型的编程语言是：`Erlang`，`Go`，`Scala`，`F#`, etc.

在`多核并行`计算模式下，我认定基于`消息传递`的`actor模型`（源自erlang）是正确的编程方式，在actor模型下，可以简单实现基于服务层的串行操作，保证“`写`”操作的完整和一致。使用`actor模型`，需要用`主/备`的部署架构来消除单点故障，实现`主/备`的部署架构，最简单可靠的方法是使用`zookeeper`。

**`高并发需求`** -> **`异步计算`**(使用actor model) -> **`master/slave`**(使用zookeeper)


## Raft

1. [演示教程](http://thesecretlivesofdata.com/raft)
2. [Raft论文(英PDF)](https://ramcloud.atlassian.net/wiki/download/attachments/6586375/raft.pdf) | [中文版1](https://github.com/maemual/raft-zh_cn/blob/master/raft-zh_cn.md) | [中文版2](http://www.infoq.com/cn/articles/raft-paper)

### 经典实现

#### ETCD

- [etcd：从应用场景到实现原理的全方位解读](http://www.infoq.com/cn/articles/etcd-interpretation-application-scenario-implement-principle)
