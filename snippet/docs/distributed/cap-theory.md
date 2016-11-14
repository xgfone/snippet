
分布式系统——CAP 理论
=================

`CAP`理论被很多人拿来作为分布式系统设计的金律，然而感觉大家对`CAP`这三个属性的认识却存在不少误区。从`CAP`的证明中可以看出来，这个理论的成立是需要很明确的对`C`、`A`、`P`三个概念进行界定的前提下的。在本文中笔者希望可以对论文和一些参考资料进行总结并附带一些思考。


## 一、什么是CAP理论

`CAP`原本是一个猜想，2000年PODC大会的时候大牛Brewer提出的，他认为在设计一个大规模可扩放的网络服务时候会遇到三个特性：**`一致性（consistency）`**、**`可用性（Availability）`**、**`分区容错（partition-tolerance）`**都需要的情景，然而这是不可能都实现的。之后在2003年的时候，Mit的 Gilbert 和 Lynch 就正式的证明了这三个特征确实是不可以兼得的。


## 二、CAP的概念

`Consistency`、`Availability`、`Partition-tolerance`的提法是由Brewer提出的，而Gilbert和Lynch在证明的过程中改变了`Consistency`的概念，将其转化为`Atomic`。Gilbert认为这里所说的`Consistency`其实就是数据库系统中提到的`ACID`的另一种表述：_**`一个用户请求要么成功、要么失败，不能处于中间状态（Atomic）；一旦一个事务完成，将来的所有事务都必须基于这个完成后的状态（Consistent）；未完成的事务不会互相影响（Isolated）；一旦一个事务完成，就是持久的（Durable）`**_。

对于`Availability`，其概念没有变化，指的是对于一个系统而言，所有的请求都应该‘成功’并且收到‘返回’。

对于`Partition-tolerance`，所指就是分布式系统的容错性。节点crash或者网络分片都不应该导致一个分布式系统停止服务。


## 三、基本CAP的证明思路

`CAP`的证明基于异步网络，异步网络也是反映了真实网络中情况的模型。真实的网络系统中，节点之间不可能保持同步，即便是时钟也不可能保持同步，所有的节点依靠获得的消息来进行本地计算和通讯。这个概念其实是相当强的，意味着任何超时判断也是不可能的，因为没有共同的时间标准。之后我们会扩展`CAP`的证明到弱一点的异步网络中，这个网络中时钟不完全一致，但是时钟运行的步调是一致的，这种系统是允许节点做超时判断的。

`CAP`的证明很简单，假设两个节点集{`G1`, `G2`}，由于网络分片导致`G1`和`G2`之间所有的通讯都断开了，如果在`G1`中写，在`G2`中读刚写的数据，`G2`中返回的值不可能是`G1`中的写值。由于`A`的要求，`G2`一定要返回这次读请求，由于`P`的存在，导致`C`一定是不可满足的。


## 四、CAP的扩展

`CAP`的证明使用了一些很强的假设，比如纯粹的异步网络，强的`C`、`A`、`P`要求。事实上，我们可以放松某些条件，从而达到妥协。

### 1、弱异步网络模型

弱异步网络模型中所有的节点都有一个时钟，并且这些时钟走的步调是一致的，虽然其绝对时间不一定相同，但是彼此的相对时间是固定的，这样系统中的节点可以不仅仅根据收到的消息来决定自己的状态，还可以使用时间来判断状态，比如超时什么的。

在这种场景下，`CAP`假设依旧是成立的，证明跟上面很相似。

### 2、不可能的尝试 ——放松`Availability`或者`Partition-tolerance`

放弃`Partition-tolerance`意味着把所有的机器搬到一台机器内部，或者放到一个要死大家一起死的机架上（当然机架也可能出现部分失效），这明显违背了我们希望的`scalability`。

放弃`Availability`意味着，一旦系统中出现`partition`这样的错误，系统直接停止服务，这是不能容忍的。

### 3、最后的选择 ——放松一致性

我们可以看出，证明`CAP`的关键在于对于一致性的强要求。在降低一致性的前提下，可以达到`CAP`的和谐共处，这也是现在大部分的分布式存储系统所采用的方式：`Cassandra`、`Dynamo`等。“Scalability is a bussness concern”是我们降低一致性而不是A和P的关键原因。

Brewer后来提出了`BASE(Basically Available, Soft-state, Eventually consistent)`，作为`ACID`的替代和补充。


## 五、战胜CAP

### 1. Atomikos

2008年9月CTO of atomikos写了一篇文章“[`A CAP Solution (Proving Brewer Wrong)`](http://blog.atomikos.com/2008/09/a-cap-solution-proving-brewer-wrong/)”，试图达到`CAP`都得的效果。

这篇文章的核心内容就是放松Gilbert和Lynch证明中的限制：“**`系统必须同时达到CAP三个属性`**”，放松到“**`系统可以不同时达到CAP，而是分时达到`**”。

#### Rules Beat CAP

    （1）尽量从数据库中读取数据，如果数据库不能访问，读取缓存中的数据。
    （2）所有读都必须有版本号。
    （3）来自客户端的更新操作排队等候执行，update必须包括导致这次更新的读操作的版本信息。
    （4）分区数量足够低的时候排队等待的update操作开始执行，附带的版本信息用来验证update是否应该执行。
    （5）不管是确认还是取消更新，所有的结构都异步的发送给请求方。

#### 证明

（1）系统保证了`consistency`，因为所有的读操作都是基于 `snapshot` 的，而不正确的 `update` 操作将被拒绝，不会导致错误执行。

（2）系统保证了`availability`，因为所有的读一定会返回，而写也一样，虽然可能会因为排队而返回的比较慢。

（3）系统允许节点失效。

#### 缺点

（1）读数据可能会不一致，因为之前的写还在排队。
（2）`partition`必须在有限的时间内解决。
（3）`update`操作必须在所有的节点上保持同样的顺序。

### 2. Nathan Marz

2011年11月Twitter的首席工程师`Nathan Marz`写了一篇文章，描述了他是如何试图打败`CAP`定理的：[`How to beat the CAP theorem`](http://nathanmarz.com/blog/how-to-beat-the-cap-theorem.html)

本文中，作者还是非常尊重`CAP`定律，并表示不是要“击败”`CAP`，而是尝试对数据存储系统进行重新设计，以可控的复杂度来实现`CAP`。

Marz认为一个分布式系统面临`CAP`难题的两大问题就是：在数据库中如何使用不断变化的数据，如何使用算法来更新数据库中的数据。Marz提出了几个由于云计算的兴起而改变的传统概念：

    （1）数据不存在update，只存在append操作。这样就把对数据的处理由CRUD变为CR。
    （2）所有的数据的操作就只剩下Create和Read。把Read作为一个Query来处理，而一个Query就是一个对整个数据集执行一个函数操作。

在这样的模型下，我们使用最终一致性的模型来处理数据，可以保证在`P`的情况下保证`A`。而所有的不一致性都可以通过重复进行`Query`去除掉。Martz认为就是因为要不断的更新数据库中的数据，再加上`CAP`，才导致那些即便使用最终一致性的系统也会变得无比复杂，需要用到向量时钟、读修复这种技术，而如果系统中不存在会改变的数据，所有的更新都作为创建新数据的方式存在，读数据转化为一次请求，这样就可以避免最终一致性的复杂性，转而拥抱`CAP`。

具体的做法这里略过。


## 总结

其实对于大规模分布式系统来说，`CAP`是非常稳固的，可以扩展的地方也不多。

它很大程度上限制了大规模计算的能力，通过一些设计方式来绕过`CAP`管辖的区域或许是下一步大规模系统设计的关键。


## 参考文献

[1] Seth Gilbert and Nancy Lynch. 2002. Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services. SIGACT News 33, 2 (June 2002), 51-59. DOI=10.1145/564585.564601 http://doi.acm.org/10.1145/564585.564601

[2] Guy Pardon, 2008, A CAP Solution (Proving Brewer Wrong), http://blog.atomikos.com/2008/09/a-cap-solution-proving-brewer-wrong/

[3] Werner Vogels, 2007, Availability & Consistency, http://www.infoq.com/presentations/availability-consistency

[4] Nathan Marz, 2011, How to beat the CAP theorem, http://nathanmarz.com/blog/how-to-beat-the-cap-theorem.html

---

From: http://www.cnblogs.com/mmjx/archive/2011/12/19/2290540.html
