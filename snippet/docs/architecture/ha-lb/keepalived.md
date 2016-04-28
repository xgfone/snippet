
## Introduction

Keepalived is a **routing software** written in C. The main goal of this project is to provide simple and robust facilities for **`loadbalancing`** and **`high-availability`** to Linux system and Linux based infrastructures. Loadbalancing framework relies on well-known and widely used **`Linux Virtual Server (IPVS)`** kernel module providing Layer4 loadbalancing. Keepalived implements a set of checkers to dynamically and adaptively maintain and manage loadbalanced server pool according their health. On the other hand high-availability is achieved by **`VRRP`** protocol. VRRP is a **`fundamental brick for router failover`**. In addition, Keepalived implements a set of hooks to the VRRP finite state machine providing low-level and high-speed protocol interactions. Keepalived frameworks can be used independently or all together to provide resilient infrastructures.

In short, Keepalived provides two main functions:
```
A. Health checking for LVS systems
B. Implementation of the VRRPv2 stack to handle load balancer failover
```
```
A. 健康检查用于负载均衡，检查后端的RealServer是否存活，以便添加该RealServer到负载均衡服务池（如LVS Topology)，
   或从负载均衡服务池中移除该RealServer。
B. VRRP协议可以实现路由故障转移(Router Failover)，以此可以达到虚拟IP的漂移。
```

简单地说，通过以上功能，Keepalived可以实现了两个目的：

	(1) 高可用(HA, High Availability)：通过VRRR协议来提供——达到虚拟IP(VIP)的漂移。
	(2) 负载均衡(LB, Load Balance)：一般情况下和LVS(IPVS)一起工作。

### VRRP协议简介
随着Internet的迅猛发展，基于网络的应用逐渐增多。这就对网络的可靠性提出了越来越高的要求。斥资对所有网络设备进行更新当然是一种很好的可靠性解决方案；但本着保护现有投资的角度考虑，可以采用廉价冗余的思路，在可靠性和经济性方面找到平衡点。 

`虚拟路由冗余协议`就是一种很好的解决方案。在该协议中，对共享多存取访问介质（如以太网）上终端IP设备的默认网关(Default Gateway)进行冗余备份，从而在其中一台路由设备宕机时，备份路由设备及时接管转发工作，向用户提供透明的切换，提高了网络服务质量。  

> VRRP specifies an election protocol that dynamically assigns
> responsibility for a virtual router to one of the VRRP routers on a LAN.
> The VRRP router controlling the IP address(es) associated with a virtual
> router is called the Master, and forwards packets sent to these IP
> addresses. The election process provides dynamic fail over in the
> forwarding responsibility should the Master become unavailable. This allows
> any of the virtual router IP addresses on the LAN to be used as the default
> first hop router by end-hosts. The advantage gained from using VRRP is a
> higher availability default path without requiring configuration of dynamic
> routing or router discovery protocols on every end-host. [rfc2338]

#### 协议概述 
在基于TCP/IP协议的网络中，为了保证不直接物理连接的设备之间的通信，必须指定路由。目前常用的指定路由的方法有两种：一种是通过路由协议（比如：内部路由协议RIP和OSPF）动态学习；另一种是静态配置。在每一个终端都运行动态路由协议是不现实的，大多客户端操作系统平台都不支持动态路由协议，即使支持也受到管理开销、收敛度、安全性等许多问题的限制。因此普遍采用对终端IP设备静态路由配置，一般是给终端设备指定一个或者多个默认网关(Default Gateway)。静态路由的方法简化了网络管理的复杂度和减轻了终端设备的通信开销，但是它仍然有一个缺点：如果作为默认网关的路由器损坏，所有使用该网关为下一跳主机的通信必然要中断。即便配置了多个默认网关，如不重新启动终端设备，也不能切换到新的网关。采用虚拟路由冗余协议 (Virtual Router Redundancy Protocol，简称VRRP)可以很好的避免静态指定网关的缺陷。 

在VRRP协议中，有两组重要的概念：**`VRRP路由器`**和**`虚拟路由器`**，**`主控路由器`**和**`备份路由器`**。

	VRRP路由器是指运行VRRP的路由器，是物理实体；
	虚拟路由器是指VRRP协议创建的，是逻辑概念。

一组VRRP路由器协同工作，共同构成一台虚拟路由器。该虚拟路由器对外表现为一个具有唯一固定IP地址和MAC地址的逻辑路由器。

处于同一个VRRP组中的路由器具有两种互斥的角色：**`主控路由器`**和**`备份路由器`**。一个VRRP组中有且只有一台处于主控角色的路由器，可以有一个或者多个处于备份角色的路由器。

VRRP协议使用选择策略从路由器组中选出一台作为主控，负责ARP相应和转发IP数据包，组中的其它路由器作为备份的角色处于待命状态。当由于某种原因主控路由器发生故障时，备份路由器能在几秒钟的时延后升级为主路由器。由于此切换非常迅速而且不用改变IP地址和MAC地址，故对终端使用者系统是透明的。  

#### 工作原理 
一个VRRP路由器有唯一的标识：**`VRID`**，范围为**`0—255`**。该路由器对外表现为`唯一的虚拟MAC地址`，地址的格式为`00-00-5E-00-01-[VRID]`。

主控路由器负责对ARP请求用该MAC地址做应答。这样，无论如何切换，保证给终端设备的是唯一一致的IP和MAC地址，减少了切换对终端设备的影响。 

VRRP控制报文只有一种：**`VRRP通告(advertisement)`**。它使用IP多播数据包进行封装，组地址为**`224.0.0.18`**，**_发布范围只限于同一局域网内_**，这保证了VRID在不同网络中可以重复使用。**_为了减少网络带宽消耗，只有主控路由器才可以周期性的发送VRRP通告报文。备份路由器在连续三个通告间隔内收不到VRRP或收到优先级为0的通告后启动新的一轮VRRP选举_**。 

##### 主路由器选举
在VRRP路由器组中，按优先级选举主控路由器，VRRP协议中优先级范围是**`0—255`**。

若VRRP路由器的IP地址和虚拟路由器的接口IP地址相同，则称该虚拟路由器作VRRP组中的IP地址所有者；IP地址所有者自动具有最高优先级：255。优先级0一般用在IP地址所有者主动放弃主控者角色时使用。**可配置的优先级范围为1—254**。

优先级的配置原则可以依据链路的速度和成本、路由器性能和可靠性以及其它管理策略设定。主控路由器的选举中，高优先级的虚拟路由器获胜，因此，如果在VRRP组中有IP地址所有者，则它总是作为主控路由的角色出现。

**_对于相同优先级的候选路由器，按照IP地址大小顺序选举_**。

VRRP还提供了优先级抢占策略，如果配置了该策略，高优先级的备份路由器便会剥夺当前低优先级的主控路由器而成为新的主控路由器。 

##### 安全认证
为了保证VRRP协议的安全性，提供了两种安全认证措施：**`明文认证`**和**`IP头认证`**。

明文认证方式要求：在加入一个VRRP路由器组时，必须同时提供相同的VRID和明文密码。适合于避免在局域网内的配置错误，但不能防止通过网络监听方式获得密码。

IP头认证的方式提供了更高的安全性，能够防止报文重放和修改等攻击。 

#### 应用实例 
最典型的VRRP应用：RTA、RTB组成一个VRRP路由器组，假设RTB的处理能力高于RTA，则将RTB配置成IP地址所有者，H1、H2、H3的默认网关设定为RTB。则RTB成为主控路由器，负责ICMP重定向、ARP应答和IP报文的转发；一旦RTB失败，RTA立即启动切换，成为主控，从而保证了对客户透明的安全切换。 

在VRRP应用中，RTA在线时RTB只是作为后备，不参与转发工作，闲置了路由器RTA和链路L1。通过合理的网络设计，可以到达备份和负载分担双重效果。让RTA、RTB同时属于互为备份的两个VRRP组：在组1中RTA为IP地址所有者；组2中RTB为IP地址所有者。将H1的默认网关设定为RTA；H2、H3的默认网关设定为RTB。这样，既分担了设备负载和网络流量，又提高了网络可靠性。 

VRRP协议的工作机理与CISCO公司的HSRP（Hot Standby Routing Protocol）有许多相似之处。但二者主要的区别是在CISCO的HSRP中，需要单独配置一个IP地址作为虚拟路由器对外体现的地址，这个地址不能是组中任何一个成员的接口地址。 

使用VRRP协议，不用改造目前的网络结构，最大限度保护了当前投资，只需最少的管理费用，却大大提升了网络性能，具有重大的应用价值。

------

[Keepalived Documention](http://www.keepalived.org/documentation.html).

Download [SRC](http://www.keepalived.org/software/), then change the directory, `doc`, and execute `make help`. You can produce the different format documentions.
