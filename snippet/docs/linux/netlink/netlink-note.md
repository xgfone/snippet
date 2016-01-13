
Linux Netlink 详解
=================

打开百度、谷歌搜索引擎一搜Netlink，发现大部分文章的介绍都是关于早期的Netlink版本（2.6.11版本），这些介绍及代码都已过时（差不多快10年了），连所使用的Linux版本最低的Redhat/CentOS也都无法编译这些代码了（关于这些接口的改变，请参见下文，但本文 不再介绍低于2.6.32版本的接口）。

## 说明
现今，计算机之间的通信，最流行的TCP/IP协议。同一计算机之间的进程之间通信，经典方式是`系统调用`、`/sys`、`/proc`等，但是这些方式几乎都是用户空间主动向内核通信，而内核不能主动与用户空间通信；另外，这些方式实现起来不方便，扩展难，尤其是系统调用（内核会保持系统调用尽可能少————Linux一旦为某个系统调用分配了一个系统调用号后，就永远为它分配而不再改变，哪怕此系统调用不再使用，其相对应的系统调用号也不可再使用）。

为此，Linux首次提出了`Netlink`机制（现在已经以RFC形式提出国际标准），它基于Socket，可以解决上述问题：`用户空间可以主动向内核发送消息`，`内核既也可以主动向用户空间发送消息`，而且Netlink的扩展也十分方便————只需要以模块的方式向内核注册一下协议或Family（这是对于`Generic Netlink`而言）即可，不会污染内核，也不会过多的增加系统调用接口。

如果想要理解本文或Netlink机制， 可能需要明白Linux对Socket体系的实现方式（或者说是TCP/IP协议），比如：什么是`协议家族（Protocol Family）`、`地址家族（Address Family）`、`协议（Protocol）`、`Socket家族`、`Socket类型`等等。

Netlink虽然也是基于Socket，但只能用于同一台计算机中。Netlink Socket的标识是根据Port号来区分的，就像TCP/UDP Port一样，但Netlink Socket的Port号可达到`4`个字节。

Netlink是一种`Address Family`，同`AF_INET`、`AF_INET6`等一样，在此Family中可以定义多种Protocol（协议）。**`Netlink最多只允许定义32个协议，而且内核中已经使用了将近20个`**，也就是说，还剩余10个左右可以定义自己的协议。
另外，`Netlink数据的传输使用数据报（SOCK_DGRAM）形式`。因此，在用户空间创建一个Socket的形式如下（假设协议为XXX）：
```c
fd = socket(AF_NETLINK, SOCK_DGRAM, XXX);
```
或者
```c
fd = socket(AF_NETLINK, SOCK_RAW, XXX);
```

Netlink Socket即可以在内核创建，也可以在用户空间创建，因此有`内核Socket`和`用户空间Socket`。在使用Netlink Socket时，需要`先注册该Socket所属的协议`，**`注册时机是在创建内核Socket之时`**，换句话说就是，**`必须先创建一个内核Socket，在创建的同时，会注册该协议，然后用户空间的程序才可以创建这种协议的Socket`**。

虽然内核Socket和用户空间Socket都是Socket，但是有差别，就像内核空间与用户空间的地位一样，内核Socket比较特殊一些：**`所有内核Socket的Port号都是0`**,而**`用户空间Socket的Port号是一个正数`**（可以是任意值，随意指定，只要不重复就行，否则会报错），一般使用当前进程的PID，如果是在多线程中，可以使用线程ID。

对于不同版本的Linux内核，NETLINK接口有所变化，具体请参见下文的样例代码。

由于Netlink是基于Socket的，因此`通信是双向的`，也就是说，`内核既可以主动与用户空间通信`，`用户空间也可以主动与内核通信`，而且`用户空间Socket可以不经过内核Socket而直接与用户空间的其他Socket通信`。这就造成了三种通信方式：

    （1）内核向用户空间发送消息；
    （2）用户空间向内核发送消息；
    （3）用户空间向用户空间发送消息。

有人会说，还有一种方式：内核向内核。但请注意，由于内核Socket比较特殊（其PortID永远都是0），因此内核向内核发送Netlink消息没有什么意义（注：这是可以的，不过最好不要这样做。在新版API中，在创建这样的内核Socket时，必须指定个compare函数）。

由于Netlink Socket是双向通信的，因此，

    （1）既可以内核作为服务器，用户空间作为客户端（这样是经典模型）；
    （2）也可以用户空间作为服务器，内核作为客户端；
    （3）还可以用户空间作为服务器，另一个用户空间Socket作为客户端。

用户空间的Netlink Socket可以监听一组或几组多播组，只需要在创建时指定多播组即可。

**注：**

（1）**`只有用户空间的Socket才可以监听多播组，内核Socket不能监听多播组`**；另外，**`在用户空间，只有管理员才能监听多播组，普通用户只能创建单播Socket`**。因此，`广播/多播消息的承受者（即接收者）只能是用户空间Socket，实施者（即发送者）既可以是内核Socket，也可以是用户Socket`。

（2）`单播消息的承受者和实施者都可以是内核Socket或用户Socket`。


## 内核向用户空间发送消息
内核向用户空间发送消息时使用`netlink_unicast`（单播）和`netlink_broadcast`（广播/多播）两个函数。其接口如下：
```c
int netlink_unicast(struct sock *ssk, struct sk_buff *skb, u32 portid, int nonblock)
int netlink_broadcast(struct sock *ssk, struct sk_buff *skb, u32 portid, u32 group, gfp_t allocation)
```

### 单播
#### 参数
**ssk**

    在注册NETLINK协议时，创建的内核Socket。

**skb**

    消息缓冲区，里面存放有将要发送给其他Socket的Netlink消息。

**portid**

    接收此消息的用户Socket的Port号，如果是0，表示接收方是内核Socket；否则是用户空间Socket。

**nonblock**

    此发送动作是否阻塞，直到消息成功发送才返回。此参数是新版Linux添加的，在旧API中没有这个参数。

#### 返回值
如果发送失败（如没有Port号为portid的Socket），则返回错误码（一个负值）；如果成功，则返回实际发送的字节数。

#### 总结
如果要向用户空间Socket发送消息，则应将portid指定该Socket的Port号（一个正数）；一般不会指定为0（内核向内核发单播消息）。

### 多播
#### 参数
**ssk**

    在注册NETLINK协议时，创建的内核Socket。

**skb**

    消息缓冲区，里面存放有将要发送给其他Socket的Netlink消息。

**portid**

    排除具有portid的Socket，即Port号为此参数的Socket不允许接收此消息，一般指定为0。

**group**

    接收此消息的组。用户Socket在创建时，会指明所监听的组。

**allocation**

    在多播时，会为每个目的Socket复制一份skb；该参数指定，在复制skb时，如何分配缓冲区，一般使用GFP_ATOMIC。

#### 返回值
如果成功，返回0；如果失败，返回错误码（一个负值）。

#### 处理流程
遍历组播表中的Socket（即打开监听组的用户Socket），如果此Socke监听的组和group参数一致（即过滤没有监听此组的用户Socket）且此Socket的Port与portid参数不一致（即过滤掉portid参数指定的Socket），则向此Socket发送一个消息（即复制一份skb，然后将新生成的skb放到目的Socket的接收队列上）。

#### 总结
如果要向用户空间发送多播消息，把group参数指定为要发送的一个或几个多播组；如果想要排除某个用户空间Socket（即不想让此Socket接收此多播消息），就把portid参数指定该Socket的Port号。portid一般指定为0，即不排除任何用户空间Socket。


## 用户空间向内核/用户空间发送消息
用户空间Netlink Socket使用的是通用Socket接口，因此发向某个其他Netlink Socket发送消息时，需要指定一个目的地址。

Netlink 地址家族的地址定义为：
```c
struct sockaddr_nl {
    __kernel_sa_family_t    nl_family;   /* AF_NETLINK   */
    unsigned short          nl_pad;      /* zero         */
    __u32                   nl_pid;      /* port ID      */
    __u32                   nl_groups;   /* multicast groups mask */
}
```

`nl_family` 是地址家族，必须指定为 `AF_NETLINK`；
`nl_pad` 是用来填充的（暂时保留），必须全部为`0`；
`nl_pid` 是目的Socket的Port号，即要发送给哪个Socket，就指定为它的Port号；
`nl_groups` 是要发送的多播组，即将Netlink消息发送给哪些多播组。

### 总结
**nl_pid是用来发送单播的，nl_groups是用来发送多播的。**

用户空间Socket无论发送单播还是多播，使用的是同一个系统调用，不同之处，只是上述地址传递的参数不同（`nl_pid`和`nl_groups`）。

### 其处理流程

    （1）判断nl_groups是否为0，如果为0，则就只向Port号为nl_pid的Socket发送一个单播消息；
    （2）如果nl_groups不为0（表示要发送多播），依次执行以下步骤：
        a. 向除Port号为nl_pid、且监听nl_groups指定的组的所有Socket发送一条此Netlink消息；
        b. 向Port号为nl_pid的Socket发送一条单播消息。

    总之，无论单播还是多播，都要向Port号为nl_pid的Socket发送一条单播消息；
    如果需要发送多播，则同时也向其他监听目的多播组的Socket发送消息。

    注意：nl_pid指定的值必须存在，也就是说，必须有一个Socket的Port号为nl_pid，否则将返回一个错误。

#### 用户空间向内核发送单播
    将nl_pid指定为0, nl_groups指定为0。

#### 用户空间向用户空间发送单播
    将nl_pid指定为目的Socket的Port号，nl_groups指定为0。

#### 用户空间向用户空间发送多播
    将nl_pid可指定为任意值（一般为0，即发送一条单播给内核），nl_groups指定为多播组。

#### 总结
    发送单播时，nl_groups必须指定为0；发送多播时，nl_groups不能为0；无论是多播还是单播，nl_pid可以是任意值。
    另外，无论是单播还是多播，都会向nl_pid指定的Socket发送一条单播消息。


## NETLINK 消息结构
NETLINK是个网络协议且使用了Socket框架，就会涉及到消息缓冲区、协议等。但不像TCP/IP协议有多层，Netlink协议只有到一层，也就是说，在用户发送的真实消息体前只有一个Netlink协议头。其协议格式如下（下述格式由于博客、空间的显式，导致有些错位）：
```
<--- nlmsg_total_size(payload)------->
<-- nlmsg_msg_size(payload) -->
+----------+- - -+-------------+- - -+
| nlmsghdr | Pad |   Payload   | Pad |
+----------+- - -+-------------+- - -+
nlmsg_data(nlh)---^
```

如果有多个Netlink消息时，其格式如下：
```
 <--- nlmsg_total_size(payload)  --->
 <-- nlmsg_msg_size(payload) ->
+----------+- - -+-------------+- - -+------------
| nlmsghdr | Pad |   Payload   | Pad | nlmsghdr
+----------+- - -+-------------+- - -+------------
nlmsg_data(nlh)---^                   ^
nlmsg_next(nlh)-----------------------+
```
其中，`nlmsg_data`、`nlmsg_next`、`nlmsg_msg_size`、`nlmsg_total_size`这些函数是内核定义的辅助函数，用来获取Netlink消息中相应某部分数据的起始位置或长度的。

Netlink消息头格式在Linux内核中定义如下：
```c
struct nlmsghdr {
    __u32       nlmsg_len;      /* Length of message including header */
    __u16       nlmsg_type;     /* Message content */
    __u16       nlmsg_flags;    /* Additional flags */
    __u32       nlmsg_seq;      /* Sequence number */
    __u32       nlmsg_pid;      /* Sending process port ID */
};
```

`nlmsg_len` 是包含消息头在内的整个Netlink消息缓冲区的长度；
`nlmsg_type` 是此消息的类型；
`nlmsg_flags` 是此消息的附加标志；
`nlmsg_seq` 是此消息的序列号（可用于调试用）；
`nlmsg_pid` 是发送此消息的Socket的Port号。

注：`nlmsg_type`、`nlmsg_flags`、`nlmsg_seq`一般没什么必要性，可以设为`0`。如果高级应用（比如路由），可以将`nlmsg_type`、`nlmsg_flags`指定为相应的值。因此，一般只需要设置`nlmsg_len`和`nlmsg_pid`两个值（其他的所有值都设为`0`）即可。另外，`nlmsg_pid`一定要设置成当前发送此消息的Socket的Port号，不然会出现一些问题，比如：如果内核或其他的Socket收到此消息并会向`nlmsg_pid`发送回复性的单播消息时，此Socket就无法收到回复消息了。


## 使用Netlink的步骤
    (1) 首先在内核创建一个内核Socket并注册一个协议（一般放在系统启动或内核模块初始化之时）；
    (2) 在用户空间创建一个Netlink Socket；
    (3) 内核作为服务端或者用户空间用为服务端：
        内核作为服务端：
            用户空间首先向内核发送消息，内核回应此消息。
        用户空间作为服务端：
            内核首先向用户空间发送消息（必须知道用户Socket的Port号或者发送多播组），然后用户空间Socket回应消息。

**注：**

Netlink的使用关键是消息的发送，在发送之前，要构建Netlink消息包。

构建Netlink消息包，无论内核还是用户空间，都要构造Netlink消息头；但在内核中，一般还要设置Netlink Socket控制块。


## 样例
以下代码，默认是内核作为服务端，用户空间作为客户端。但已经另外预留了接口，稍微修改一下，即可以变为用户空间作为服务端，内核作为客户端。

内核作为客户端有个要求，需要有个时机去触发内核主动向用户空间发送消息。

注：这个时机不能是内核Socket创建之时，也就是说，不能在创建内核Socket之后立即向用户空间发送消息，因为此时用户空间还没有创建用户空间的Netlink Socket。我在测试时，一般使用另一个内核模块来触发（在加载模块之时）。

内核模块已经预留接口，并且已经将这些接口作为导出符号导出（在其他模块中可直接使用）：
```c
int test_unicast(void *data, size_t size, __u32 pid);
int test_broadcast(void *data, size_t size, __u32 group);
```
只需要调用以上函数中的任何一个，内核就可以向用户空间发送单播或多播消息。

注：以下代码，在 `Ubuntu 14.04 64 Bit` 和 `Deepin 2014 64 Bit` 下测试成功；如果编译失败，请检查内核版本是否正确，以下代码默认要求 `Linux 3.8` 以上，如果低于 `3.8`，请根据注释换成相应的接口；`CentOS 6` 使用的 Linux 内核是 `2.6.32` 的，请根据注释换成相应的接口。如果是在加载内核模块时失败，请检查

    （1）内核模块名是不是 kernel.ko（第三方内核模块不允许为kernel.ko，因为这个名字已经被Linux内核自身使用了）；
    （2）NETLINK_TEST 宏值是否已经被使用了，如果被使用了，请换成一个没有被使用过的（17 很容易被使用，故以下代码改成了 30）。


### 内核模块文件netlink_kernel.c
```c
#include <linux/module.h>
#include <net/sock.h>
#include <linux/netlink.h>
#include <linux/skbuff.h>

#define NETLINK_TEST 30

static struct sock *nl_sk = NULL;

/*
 * Send the data of `data`, whose length is `size`, to the socket whose port is `pid` through the unicast.
 *
 * @param data: the data which will be sent.
 * @param size: the size of `data`.
 * @param pid: the port of the socket to which will be sent.
 * @return: if successfully, return 0; or, return -1.
 */
int test_unicast(void *data, size_t size, __u32 pid)
{
    struct sk_buff *skb_out;
    skb_out = nlmsg_new(size, GFP_ATOMIC);
    if(!skb_out) {
        printk(KERN_ERR "Failed to allocate a new sk_buff\n");
        return -1;
    }

    //struct nlmsghdr* nlmsg_put(struct sk_buff *skb, u32 portid, u32 seq, int type, int len, int flags);
    struct nlmsghdr * nlh;
    nlh = nlmsg_put(skb_out, 0, 0, NLMSG_DONE, size, 0);

    memcpy(nlmsg_data(nlh), data, size);

    // 设置 SKB 的控制块（CB）
    // 控制块是 struct sk_buff 结构特有的，用于每个协议层的控制信息（如：IP层、TCP层）
    // 对于 Netlink 来说，其控制信息是如下结构体：
    // struct netlink_skb_parms {
    //      struct scm_credscreds;  // Skb credentials
    //      __u32portid;            // 发送此SKB的Socket的Port号
    //      __u32dst_group;         // 目的多播组，即接收此消息的多播组
    //      __u32flags;
    //      struct sock*sk;
    // };
    // 对于此结构体，一般只需要设置 portid 和 dst_group 字段。
    // 但对于不同的Linux版本，其结构体会所有变化：早期版本 portid 字段名为 pid。
    //NETLINK_CB(skb_out).pid = pid;
    NETLINK_CB(skb_out).portid = pid;
    NETLINK_CB(skb_out).dst_group = 0;  /* not in mcast group */

    // 单播/多播
    if(nlmsg_unicast(nl_sk, skb_out, pid) < 0) {
        printk(KERN_INFO "Error while sending a msg to userspace\n");
        return -1;
    }

    return 0;
}
EXPORT_SYMBOL(test_unicast);

/*
 * Send the data of `data`, whose length is `size`, to the socket which listens
 * the broadcast group of `group` through the broadcast.
 *
 * @param data: the data which will be sent.
 * @param size: the size of `data`.
 * @param group: the broadcast group which the socket listens, to which will be sent.
 * @return: if successfully, return 0; or, return -1.
 */
int test_broadcast(void *data, size_t size, __u32 group)
{
    struct sk_buff *skb_out;
    skb_out = nlmsg_new(size, GFP_ATOMIC);
    if(!skb_out) {
        printk(KERN_ERR "Failed to allocate a new sk_buff\n");
        return -1;
    }

    //struct nlmsghdr* nlmsg_put(struct sk_buff *skb, u32 portid, u32 seq, int type, int len, int flags);
    struct nlmsghdr * nlh;
    nlh = nlmsg_put(skb_out, 0, 0, NLMSG_DONE, size, 0);

    memcpy(nlmsg_data(nlh), data, size);

    // NETLINK_CB(skb_out).pid = 0;
    NETLINK_CB(skb_out).portid = 0;
    NETLINK_CB(skb_out).dst_group = group;

    // 多播
    // int netlink_broadcast(struct sock *ssk, struct sk_buff *skb, __u32 portid, __u32 group, gfp_t allocation);
    if (netlink_broadcast(nl_sk, skb_out, 0, group, GFP_ATOMIC) < 0) {
        printk(KERN_ERR "Error while sending a msg to userspace\n");
        return -1;
    }

    return 0;
}
EXPORT_SYMBOL(test_broadcast);

static void nl_recv_msg(struct sk_buff *skb)
{
    struct nlmsghdr *nlh = (struct nlmsghdr*)skb->data;
    char *data = "Hello userspace";
    printk(KERN_INFO "==== LEN(%d) TYPE(%d) FLAGS(%d) SEQ(%d) PORTID(%d)\n", nlh->nlmsg_len, nlh->nlmsg_type,
           nlh->nlmsg_flags, nlh->nlmsg_seq, nlh->nlmsg_pid);
    printk("Received %d bytes: %s\n", nlmsg_len(nlh), (char*)nlmsg_data(nlh));
    test_unicast(data, strlen(data), nlh->nlmsg_pid);
}

static int __init test_init(void)
{
    printk("Loading the netlink module\n");

    /*
    // Args:
    //      net:   &init_net
    //      unit:  User-defined Protocol Type
    //      input: the callback function when received the data from the userspace.
    //
    // 3.8 kernel and above
    // struct sock* __netlink_kernel_create(struct net *net, int unit,
    //                                      struct module *module,
    //                                      struct netlink_kernel_cfg *cfg);
    // struct sock* netlink_kernel_create(struct net *net, int unit, struct netlink_kernel_cfg *cfg)
    // {
    //     return __netlink_kernel_create(net, unit, THIS_MODULE, cfg);
    // }
    //
    //
    // 3.6 or 3.7 kernel
    // struct sock* netlink_kernel_create(struct net *net, int unit,
    //                                    struct module *module,
    //                                    struct netlink_kernel_cfg *cfg);
    //
    // 2.6 - 3.5 kernel
    // struct sock *netlink_kernel_create(struct net *net,
    //                                    int unit,
    //                                    unsigned int groups,
    //                                    void (*input)(struct sk_buff *skb),
    //                                    struct mutex *cb_mutex,
    //                                    struct module *module);
    */

    /*
    // This is for the kernels from 2.6.32 to 3.5.
    nl_sk = netlink_kernel_create(&init_net, NETLINK_TEST, 0, nl_recv_msg, NULL, THIS_MODULE);
    if(!nl_sk) {
        printk(KERN_ALERT "Error creating socket.\n");
        return -10;
    }
    */

    //This is for 3.8 kernels and above.
    struct netlink_kernel_cfg cfg = {
        .input = nl_recv_msg,
    };

    nl_sk = netlink_kernel_create(&init_net, NETLINK_TEST, &cfg);
    if(!nl_sk) {
        printk(KERN_ALERT "Error creating socket.\n");
        return -10;
    }

    return 0;
}

static void __exit test_exit(void) {
    printk(KERN_INFO "Unloading the netlink module\n");
    netlink_kernel_release(nl_sk);
}

module_init(test_init);
module_exit(test_exit);
MODULE_LICENSE("GPL");
```

### 用户空间程序文件netlink_user.c
```c
#include <stdint.h>
#include <sys/socket.h>
#include <linux/netlink.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define NETLINK_TEST    30
#define MAX_PAYLOAD     1024    /* maximum payload size*/
#define MAX_NL_BUFSIZ   NLMSG_SPACE(MAX_PAYLOAD)

//int PORTID = getpid();
int PORTID = 1;

int create_nl_socket(uint32_t pid, uint32_t groups)
{
    int fd = socket(PF_NETLINK, SOCK_RAW, NETLINK_TEST);
    if (fd == -1) {
        return -1;
    }

    struct sockaddr_nl addr;
    memset(&addr, 0, sizeof(addr));
    addr.nl_family = AF_NETLINK;
    addr.nl_pid = pid;
    addr.nl_groups = groups;

    if (bind(fd, (struct sockaddr *)&addr, sizeof(addr)) != 0) {
        close(fd);
        return -1;
    }

    return fd;
}

ssize_t nl_recv(int fd)
{
    char nl_tmp_buffer[MAX_NL_BUFSIZ];
    struct nlmsghdr *nlh;
    ssize_t ret;

    // 设置 Netlink 消息缓冲区
    nlh = (struct nlmsghdr *)&nl_tmp_buffer;
    memset(nlh, 0, MAX_NL_BUFSIZ);

    ret = recvfrom(fd, nlh, MAX_NL_BUFSIZ, 0, NULL, NULL);
    if (ret < 0) {
        return ret;
    }

    // // 通过MSG结构体来发送信息
    // struct iovec iov;
    // struct msghdr msg;
    // iov.iov_base = (void *)nlh;
    // iov.iov_len = MAX_NL_BUFSIZ;
    // msg.msg_name = (void *)&addr;
    // msg.msg_namelen = sizeof(*addr);
    // msg.msg_iov = &iov;
    // msg.msg_iovlen = 1;
    // ret = recvmsg(fd, &msg, 0);
    // if (ret < 0) {
    // return ret;
    // }

    printf("==== LEN(%d) TYPE(%d) FLAGS(%d) SEQ(%d) PID(%d)\n\n", nlh->nlmsg_len, nlh->nlmsg_type,
           nlh->nlmsg_flags, nlh->nlmsg_seq, nlh->nlmsg_pid);
    printf("Received data: %s\n", NLMSG_DATA(nlh));
    return ret;
}

int nl_sendto(int fd, void *buffer, size_t size, uint32_t pid, uint32_t groups)
{
    char nl_tmp_buffer[MAX_NL_BUFSIZ];
    struct nlmsghdr *nlh;

    if (NLMSG_SPACE(size) > MAX_NL_BUFSIZ) {
        return -1;
    }

    struct sockaddr_nl addr;
    memset(&addr, 0, sizeof(addr));
    addr.nl_family = AF_NETLINK;
    addr.nl_pid = pid;          /* Send messages to the linux kernel. */
    addr.nl_groups = groups;    /* unicast */

    // 设置 Netlink 消息缓冲区
    nlh = (struct nlmsghdr *)&nl_tmp_buffer;
    memset(nlh, 0, MAX_NL_BUFSIZ);
    nlh->nlmsg_len = NLMSG_LENGTH(size);
    nlh->nlmsg_pid = PORTID;
    memcpy(NLMSG_DATA(nlh), buffer, size);

    return sendto(fd, nlh, NLMSG_LENGTH(size), 0, (struct sockaddr *)&addr, sizeof(addr));

    // // 通过MSG结构体来发送信息
    // struct iovec iov;
    // struct msghdr msg;
    // iov.iov_base = (void *)nlh;
    // iov.iov_len = nlh->nlmsg_len;
    // msg.msg_name = (void *)dst_addr;
    // msg.msg_namelen = sizeof(*dst_addr);
    // msg.msg_iov = &iov;
    // msg.msg_iovlen = 1;
    // return sendmsg(sock_fd, &msg, 0);
}

int main(void)
{
    char data[] = "Hello kernel";
    int sockfd = create_nl_socket(PORTID, 0);
    if (sockfd == -1) {
        return 1;
    }

    int ret;
    ret = nl_sendto(sockfd, data, sizeof(data), 0, 0);
    if (ret < 0) {
        printf("Fail to send\n");
        return 1;
    }
    printf("Sent %d bytes\n", ret);

    ret = nl_recv(sockfd);
    if (ret < 0) {
        printf("Fail to receive\n");
    }
    printf("Received %d bytes\n", ret);

    // while (1) {
    // nl_recv(sockfd);
    // nl_sendto(sockfd, data, sizeof(data), 0, 0);
    // }

    return 0;
}
```

### Makefile文件
```makefile
KBUILD_CFLAGS += -w
obj-m += netlink_kernel.o

all:
    make -w -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```

### 构造方法

#### 编译内核模块
切换到该目录下，直接执行 `make` 即可，如：
```shell
$ make
```

#### 编译用户空间程序
```shell
gcc netlink_user.c -o netlink_user
```

#### 安装内核模块
```shell
sudo insmod ./netlink_kernel.ko
```

#### 启动用户空间程序
```shell
./netlink_user
```


