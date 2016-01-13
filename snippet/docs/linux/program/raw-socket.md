
Raw Socket 接收和发送数据包
=========================

## 前言
对于网络层IP数据包的接收、发送，RAW SOCKET 接口是通用的，具有可移植性。

但对于数据链路层数据帧的接收、发送，不同的系统有不同的机制，不具有可移植性。

对于数据包的接收（即捕获），Raw Socket 并干扰内核协议栈，换句话说就是，Raw Socket 捕获到的数据是内核协议栈中数据包的一份拷贝，内核协议栈还会按照原先的决策继续处理该数据包。


## 方法
SOCK_RAW 原始套接字编程可以接收到本机网卡上的数据帧或者数据包，对与监听网络的流量和分析是很有作用的。

一共可以有 `3` 种方式创建这种socket：
```c
socket(AF_INET, SOCK_RAW, IPPROTO_XXX)           // 发送、接收网络层IP数据包
socket(PF_PACKET, SOCK_RAW, htons(ETH_P_XXX))    // 发送、接收数据链路层数据帧（目前只有Linux支持）
socket(AF_INET, SOCK_PACKET, htons(ETH_P_XXX))   // 过时了
```


## SOCK_RAW｀接收｀数据包的原理
### 1. 网卡对该数据帧进行硬过滤（数据链路层过滤）———— 二层
首先进行数据链路层校验和处理，如果校验和出错，直接仍掉；然后根据网卡的模式不同会有不同的动作：如果设置了promisc混杂模式的话，则不做任何过滤直接交给下一层输入例程，否则非本机mac或者广播mac会被直接丢弃。

### 2. 向用户层递交数据链路层数据帧 ———— SOCK_RAW捕获数据链路层数据帧
在进入网络层之前，系统会检查系统中是否有通过`socket(AF_PACKET, SOCK_RAW, ...)`创建的套接字；如果有并且与指定的协议相符的话，系统就给每个这样的socket接收缓冲区发送一个数据帧拷贝。然后进入网络层。

### 3. 进入网络层（IP层过滤）———— 三层
IP层会对该数据包进行软过滤————就是检查校验或者丢弃非本机IP或者广播IP的数据包等。

### 4. 向用户层递交网络层数据包 ———— SOCK_RAW捕获网络层IP数据包
在进入运输层（如TCP、UDP例程）之前，系统会检查系统中是否有通过`socket(AF_INET, SOCK_RAW, ...)`创建的套接字；如果有的话并且协议相符，系统就给每个这样的socket接收缓冲区发送一个数据包拷贝（不管在任何情况下，永远都包含IP数据包头）。然后进入运输层。

### 5. 进入运输层（如TCP、UDP等例程）———— 四层
这一步由系统内核来处理运输层的协议，用户层无法干涉。处理完之后，如果合法，将向用户层递交数据，进而进入用户层处理。

### 6. 进入用户层（如HTTP、FTP等）
这一层在用户态，由用户应用程序来完成。

**注：**

A. **`如果校验和出错的话，内核会直接丢弃该数据包的；而不会拷贝给sock_raw套接字`**，因为校验和都出错了，数据肯定有问题的，其包括所有信息都没有意义了。所以，sock_raw不需要关心数据链路层和IP层的校验和问题。

B. **`在没有递交给其他协议处理器（内核协议处理器）之前，先递交给所有的 Raw Socket，换句话说，就是 Raw Socket 优先处理`**。


## 进一步分析他们的能力
### 第一种
```c
socket(AF_INET, SOCK_RAW, IPPROTO_XXX)
```
其中，`IPPROTO_XXX` 是`/etc/protocols`文件中描述的protocol，指明要接收的包含在IP数据包中的协议包。

#### 接收
这个SOCKET接收的数据是包含IP头的IP数据包（不管protocol是任何协议），并且是已经重组好的IP包。

##### 能
协议类型为IPPROTO_XXX且发往本机的IP数据包。

##### 不能
非发往本地IP的数据包（在网络层会被过滤掉）和从本机发送出去的数据包。

##### 注
    (1) UDP和TCP数据包从不传送给一个原始套接字raw socket。
    (2) 在将一个IP数据包传送给 raw socket 之前，内核需要选择匹配的原始套接字：
        A. 数据包的协议域必须与接收原始套接字指定的协议类型匹配。
        B. 如果原始套接字调用了 bind 函数来绑定本机 IP 地址，则到达的 IP 数据包的源 IP 地址必须和绑定的 IP 相匹配。
           这条笔者没明白是什么意思，感觉有点像捕获从本地发送出去的数据包，又有点不像。
        C. 如果原始套接字调用了 connect 函数来指定对方的 IP 地址，则到达的 IP 数据包的源 IP 地址必须和指定的相匹配。
    (3) 一般来说，原始套接字可以接收到：
        A. 任何对内核来说是未知的上层协议的IP数据报，
        B. 大部分类型的ICMP报文，
        C. 所有的IGMP报文。

#### 发送
默认情况下，发送的数据是不包含IP头的IP数据包负载部分（如TCP或UDP包），网络层会自动添加IP头；如果使用`setsocketopt`函数设置了`IP_HDRINCL`选项后，写入的数据就必须包含IP头，即IP头在用户层由使用者自己构建。例子：
```c
int on = 1;
if (setsockopt(sockfd, IPPROTO_IP, IP_HDRINCL, &on, sizeof(on)) < 0) {
    printf("Set IP_HDRINCL failed\n");
}
```

**注：**

（1）如果protocol是`IPPROTO_RAW(255)`，这时候，这个socket只能用来发送IP包，而不能接收任何的数据。发送的数据需要自己填充IP包头，并且自己计算校验和。

（2）对于protocol为0（`IPPROTO_IP`)的raw socket。用于接收任何的IP数据包。其中的校验和和协议分析由程序自己完成。

（3）如果protocol既不是0也不是255，那么sock_raw既可以接收数据包，也可以发送数据包。
另一种说法：对于domain为`AF_INET`，type为`SOCK_RAW`的socket来说，protocol不能为0（即`IPPROTO_IP`）。
经过在Go语言下测试（通过系统调用syscall.Socket），对protocol参数使用0时，报错：`protocol not supported`。

（4）如果protocol为 `IPPROTO_RAW`，则默认设置 `IP_HDRINCL` 选项。

（5）Receiving of all IP protocols via `IPPROTO_RAW` is not possible using raw sockets.（man 7 raw）

（6）虽然设置 `IP_HDRINCL` 选项，可以由使用者自行指定IP头，但 `IP_HDRINCL` 选项还是会修改使用者指定的IP头，规则如下：

    A. IP 头校验和（CheckSum）：总是填充。换句话说就是，使用者在指定IP头，不需要处理IP校验和。
    B. 源IP地址：如果为 0，则被自动填充为本机的 IP 地址。
    C. 包ID（packet ID）：如果为 0，则被自动填充。
    D. IP包的总长度：总是被填充。换句话说就是，IP头部的关于IP数据包总长度字段不需要使用者来处理。

（7）如果 raw socket 没有使用 connect 函数绑定对方地址时，则应使用 `sendto` 或 `sendmsg` 函数来发送数据包，在函数参数中指定对方地址。如果使用了 connect 函数，则可以直接使用 `send`、`write` 或 `writev` 函数来发送数据包。

（8）如果 raw socket 调用了 `bind` 函数，则发送数据包的源 IP 地址将是 `bind` 函数指定的地址。否则，内核将以发接口的主 IP 地址填充；如果设置了 `IP_HDRINCL` 选项，则必须手工填充每个发送数据包的源 IP 地址。

这种套接字用来写个ping程序比较适合。

### 第二种
```c
socket(PF_PACKET, SOCK_RAW, htons(ETH_P_XXX))
```
这种套接字可以监听网卡上的所有数据帧；最后以太网CRC从来都不算进来的，因为内核已经判断过了，对程序来说没有任何意义了。

#### 接收

    A. 发往本地mac的数据帧
    B. 从本机发送出去的数据帧(第3个参数需要设置为 ETH_P_ALL)
    C. 非发往本地mac的数据帧(网卡需要设置为 promisc 混杂模式)

    协议类型一共有四个
        ETH_P_IP   0x800     只接收发往本机mac的IP类型的数据帧
        ETH_P_ARP  0x806     只接收发往本机mac的ARP类型的数据帧
        ETH_P_ARP  0x8035    只接收发往本机mac的RARP类型的数据帧
        ETH_P_ALL  0x3       接收发往本机mac的所有类型（IP、ARP、RARP）的数据帧，并接收从本机发出的所有类型的数据帧
                            （混杂模式打开的情况下，会接收到非发往本地mac的数据帧）

#### 发送
需要自己组织整个以太网数据帧，所有相关的地址使用`struct sockaddr_ll` 而不是 `struct sockaddr_in`（因为协议簇是 `PF_PACKET` 不是 AF_INET 了————应该称 `PF_INET`，具体地见“`备注`”）。

这种socket大小通吃，下面是一段相关的代码:
```c
    int sockfd = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    struct sockaddr_ll sll;
    memset( &sll, 0, sizeof(sll) );
    sll.sll_family = AF_PACKET;
    struct ifreq ifstruct;
    strcpy(ifstruct.ifr_name, "eth0");
    ioctl(sockfd, SIOCGIFINDEX, &ifstruct);
    sll.sll_ifindex = ifstruct.ifr_ifindex;
    sll.sll_protocol = htons(ETH_P_ALL);
    if(bind(fd, (struct sockaddr *) &sll, sizeof(sll)) == -1 )
        perror("bind()");

    int set_promisc(char *interface, int fd) {
        struct ifreq ifr;
        strcpy(ifr.ifr_name, interface);
        if(ioctl(fd, SIOCGIFFLAGS, &ifr) == -1) {
            perror("iotcl()");
            return -1;
        }
        ifr.ifr_flags |= IFF_PROMISC;
        if(ioctl(fd, SIOCSIFFLAGS, &ifr) == -1) {
            perror("iotcl()");
            return -1;
        }
        return 0;
    }

    int unset_promisc(char *interface, int fd) {
        struct ifreq ifr;
        strcpy(ifr.ifr_name, interface);
        if(ioctl(fd, SIOCGIFFLAGS, &ifr) == -1) {
            perror("iotcl()");
            return -1;
        }
        ifr.ifr_flags &= ~IFF_PROMISC;
        if(ioctl(fd, SIOCSIFFLAGS, &ifr) == -1) {
            perror("iotcl()");
            return -1;
        }
        return 0;
    }
```

### 第三种
```c
socket(AF_INET, SOCK_PACKET, htons(ETH_P_ALL))     // 这个过时了，最好不要用
```

总结使用方法:

    1. 如果只想收到发往本机某种协议的IP数据包的话，用第一种就足够了。
    2. 更多的详细的内容请使用第二种，包括ETH_P_ALL参数和混杂模式都可以使它的能力不断的加强。


## 关于 RAW SOCKET 的一点其他说明

1、**·校验和不用转换成网络序·**。另外如果这个函数写得不正确的话，通常得不到对方的发回包，很难调试。

2、数据转化成网络序的一个原则是：**·一般协议头部的short和int/long型的数据通常要转换成网络序·**。

运载的数据部分，如果在对方要处理的，类型为short/int/long型数据的也要转换成网络序；如果对方不做处理，直接返回的数据部分，可以不转换成网络序。

3、**raw tcp的程序为什么只写发SYN包？**

因为你发了SYN包，对方发回来SYN/ACK包，你的操作系统内核先于你的程序接收到这个包，它检查内核里的socket，发现没有一个socket对应于这个包（因为raw tcp socket没有保存ip和端口等信息，所以内核不能识别这个包），所以发了一个RST包给对方，于是对方的tcp socket关闭了。你的raw tcp socket最终收到这个SYN/ACK包，你的程序做了处理后，再发ACK包给对方时，对方的tcp socket已经关闭，所以对方就发了一个RST回来。要写一个SYN flooder就只能用raw raw socket，因为raw tcp不能自己控制IP头，所以不能写SYN flooder，除非用了IP_HDRINCL选项和自己构造IP头部。本人对其他人使用这些程序所做的事情不负任何责任，仅为技术交流而发布。

4、关于各种协议头的检验和产生方法

    IP：  只包含IP头的检验和，不包括数据部分。
    ICMP: 包括ICMP头和数据。
    TCP:  包括一个伪协议头部、TCP头和数据。
    UDP:  包括一个伪协议头部、UDP头和数据。

5、raw socket发送数据和返回数据的形式

    IPPROTO_ICMP   不用构建IP头部分，只发送ICMP头和数据。返回包括IP头、ICMP头和数据。
    IPPROTO_UDP    不用构建IP头部分，只发送UDP头和数据。返回包括IP头、UDP头和数据。
    IPPROTO_TCP    不用构建IP头部分，只发送TCP头和数据。返回包括IP头、TCP头和数据。
    IPPROTO_RAW    要构建IP头部和要发送的各种协议的头部和数据。返回包括IP头、相应的协议头和数据。

注：由于以前没有 `IP_HDRINCL` 选项，`IPPROTO_RAW` 提供应用程序自行指定IP头部的功能。


## 一个ping程序样例
```c
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

#include "unistd.h"
#include "sys/types.h"
#include "sys/socket.h"
#include "netinet/in.h"
#include "netinet/ip.h"
#include "netinet/ip_icmp.h"
#include "netdb.h"
#include "errno.h"
#include "arpa/inet.h"
#include "signal.h"
#include "sys/time.h"

extern int errno;

int sockfd;
struct sockaddr_in addr; //peer addr
char straddr[128];       //peer addr ip(char*)
char sendbuf[2048];
char recvbuf[2048];
int sendnum;
int recvnum;
int datalen = 30;


unsigned short my_cksum(unsigned short *data, int len) {
    int result = 0;
    for(int i=0; i<len/2; i++) {
        result += *data;
        data++;
    }
    while(result >> 16)result = (result&0xffff) + (result>>16);
    return ~result;
}
void tv_sub(struct timeval* recvtime, const struct timeval* sendtime) {
    int sec = recvtime->tv_sec - sendtime->tv_sec;
    int usec = recvtime->tv_usec - sendtime->tv_usec;
    if(usec >= 0) {
        recvtime->tv_sec = sec;
        recvtime->tv_usec = usec;
    } else {
        recvtime->tv_sec = sec-1;
        recvtime->tv_usec = -usec;
    }
}

void send_icmp() {
    struct icmp* icmp = (struct icmp*)sendbuf;
    icmp->icmp_type = ICMP_ECHO;
    icmp->icmp_code = 0;
    icmp->icmp_cksum = 0;

    // needn't use htons() call, because peer networking kernel didn't handle
    // this data and won't make different meanings(bigdian litteldian)
    icmp->icmp_id = getpid();
    icmp->icmp_seq = ++sendnum;   //needn't use hotns() call too.
    gettimeofday((struct timeval*)icmp->icmp_data, NULL);
    int len = 8+datalen;
    icmp->icmp_cksum = my_cksum((unsigned short*)icmp, len);
    int retval = sendto(sockfd, sendbuf, len, 0, (struct sockaddr*)&addr, sizeof(addr));
    if(retval == -1){
        perror("sendto()");
        exit(-1);
    }
}

void recv_icmp() {
    struct timeval *sendtime;
    struct timeval recvtime;

    for(;;) {
        int n = recvfrom(sockfd, recvbuf, sizeof(recvbuf), 0, 0, 0);
        if(n == -1) {
            if(errno == EINTR)continue;
            else {
                perror("recvfrom()");
                exit(-1);
            }
        } else {
            gettimeofday(&recvtime, NULL);
            struct ip *ip = (struct ip*)recvbuf;
            if(ip->ip_src.s_addr != addr.sin_addr.s_addr) {
                continue;
            }
            struct icmp *icmp = (struct icmp*)(recvbuf + ((ip->ip_hl)<<2));
            if(icmp->icmp_id != getpid()) {
                continue;
            }
            recvnum++;
            sendtime = (struct timeval*)icmp->icmp_data;
            tv_sub(&recvtime, sendtime);
            printf("imcp echo from %s(%dbytes)\tttl=%d\tseq=%d\ttime=%d.%06d s\n",
                   straddr, n, ip->ip_ttl, icmp->icmp_seq, recvtime.tv_sec, recvtime.tv_usec);
        }
    }
}

void catch_sigalrm(int signum) {
    send_icmp();
    alarm(1);
}

void catch_sigint(int signum) {
    printf("\nPing statics:send %d packets, recv %d packets, %d%% lost...\n",
           sendnum, recvnum, (int)((float)(sendnum-recvnum)/sendnum)*100);
    exit(0);
}

int main(int argc, char **argv) {
    if(argc != 2) {
        printf("please use format: ping hostname\n");
        exit(-1);
    }

    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if(sockfd == -1) {
        perror("socket()");
        return -1;
    }

    /*
    int sendbufsize = 180;
    socklen_t sendbufsizelen = sizeof(sendbufsize);
    if(setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &sendbufsize, sendbufsizelen) == -1)
        perror("setsockopt()");
    int recvbufsize;
    socklen_t recvbufsizelen;
    if(getsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &recvbufsize, &recvbufsizelen) == -1)
        perror("getsockopt()");
    */

    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    int retval = inet_pton(AF_INET, argv[1], &addr.sin_addr);
    if(retval == -1 || retval == 0) {
        struct hostent* host = gethostbyname(argv[1]);
        if(host == NULL) {
            fprintf(stderr, "gethostbyname(%s):%s\n", argv[1], strerror(errno));
            exit(-1);
        }

        /*
        if(host->h_name != NULL)printf("hostent.h_name:%s\n", host->h_name);
        if(host->h_aliases != NULL && *(host->h_aliases) != NULL)
            printf("hostent.h_aliases:%s\n", *(host->h_aliases));
        printf("hostent.h_addrtype:%d\n", host->h_addrtype);
        printf("hostent.h_length:%d\n", host->h_length);
        */

        if(host->h_addr_list != NULL && *(host->h_addr_list) != NULL) {
            strncpy((char*)&addr.sin_addr, *(host->h_addr_list), 4);
            inet_ntop(AF_INET, *(host->h_addr_list), straddr, sizeof(straddr));
        }
        printf("Ping address:%s(%s)\n\n", host->h_name, straddr);
    } else {
        strcpy(straddr, argv[1]);
        printf("Ping address:%s(%s)\n\n", straddr, straddr);
    }

    struct sigaction sa1;
    memset(&sa1, 0, sizeof(sa1));
    sa1.sa_handler = catch_sigalrm;
    sigemptyset(&sa1.sa_mask);
    sa1.sa_flags = 0;
    if(sigaction(SIGALRM, &sa1, NULL) == -1)
        perror("sigaction()");

    struct sigaction sa2;
    memset(&sa2, 0, sizeof(sa2));
    sa2.sa_handler = catch_sigint;
    sigemptyset(&sa2.sa_mask);
    sa2.sa_flags = 0;
    if(sigaction(SIGINT, &sa2, NULL) == -1)
        perror("sigaction()");

    alarm(1);
    recv_icmp();

    return 0;
}
```

## 备注

### 1、协议簇和地址簇、AF_PACKET和PF_PACKET
协议簇指代底层进行数据传递时的协议，每种协议都相应的有一种地址格式，这样才能将数据由一个地方传递到另外一个地方。在早期，有人提出一种协议簇可能对应多种地址格式，因此将协议簇和地址簇区分开来，换句话说就是，协议簇与地址簇是一对多的关系；但到目前为止，每种协议簇都只对应一种地址簇，好像还没有哪种协议簇对应多个地址簇。

**`协议簇以 PF_ 开头，地址簇以 AF_ 开头`**。由于目前的协议簇和地址簇都是一一对应的，因此，相对应的协议簇和地址簇除了开头不同，其他部分都是相同的，如：PF_INET 和 AF_INET、PF_PACKET 和 AF_PACKET。

**`理论上来说，对于 socket 函数的第一个参数 domain 应该使用地址簇，而不是使用协议簇`**，因为一个协议簇可以对应多个地址簇，而 socket 在绑定bind及传递数据时，是要根据不同的地址簇来区分不同类型的地址参数的。但是，到目前为止，协议簇和地址簇是一一对应的，还没有哪个协议簇对应多个地址簇，而且相对应的协议簇和地址簇的值在定义上是相同的，因此，对于 domain 参数，既可以使用协议簇，也可以使用地址簇。不过，最好还是使用地址簇最好，即最好使用以 AF_ 开关的宏或常量。

因此，上述讨论 `socket(PF_PACKET, SOCK_RAW, htons(ETH_P_XXX))`` 中的 `PF_PACKET`，也可以换成 `AF_PACKET`。


## 关于Go语言对 Raw Socket 的说明

（1）Go标准库 `net` 是使用Socket的通用包，但它返回的数据只是负载部分，比如：TCP、UDP等协议返回的是负载数据（不包括TCP、UDP等协议头），这和其他语言一样；但对于 IP 协议包，net包返回的也是 IP 负载部分（如：TCP、UDP、ICMP等协议包），不包含IP协议头。另外，和其他语言不一样的是，net 包对 IP 协议包和TCP、UDP等协议一样，也分别 Dial（相当于客户端）和 Listen（相当于服务端）。举个例子：使用 Dial 来连接到 本机的 127.0.0.1 地址上，然后 Ping 127.0.0.1，结果会发现，Dial 接收到数据只有请求回显包（即ICMP的类型为 0x08），而没有回显应答包（即ICMP的类型为 0x00）；如果使用 Linux C SOCK_RAW 接收的话，这两种包都会捕获到。

（2）除了 `net` 包，GO还提供了 `syscall` 系统调用包，其封装了各个系统中的系统调用，对于不同的系统，其中封装的函数会有所不同。在Linux平台上，其封装了 Socket、Bind、Listen、Accept、Connect、Read、Write、Recvfrom、Sendto等跟 Socket 有关的系统调用，其可以执行底层的系统调用。但是又有个小问题：_**Go 封装的这些系统调用无法捕获数据链路层数据帧，最大限度只能指定某一种 `IPPROTO_XXX` 协议来捕获包含该协议的 IP 包**_，这和 Linux C 中的功能一样。另外，在 GO 中，_**一个 SOCK_RAW 只能指定一种 `IPPROTO_XXX` 协议来捕获一种 IP 包**_，并不能指定 IPPROTO_IP（其protocol号为0）来捕获所有的 IP 包，在 Linux C 中，好像也是一样的，据某些文献资料所说，对于RAW SOCKET，protocol 不能为 IPPROTO_IP，0 号协议只能用于 AF_INET 或 AF_INET6 等地址簇中，然后 AF_INET 或 AF_INET6 地址簇会挑选一个默认 protocol，比如：对于 SOCK_STREAM 类型的 socket，其默认 protocol 是 TCP，而 SOCK_DGRAM 类型的 socket 的默认协议是 UDP。


## 参考文档
man 7 SOCK_RAW 手册页

http://blog.csdn.net/baixue6269/article/details/6863408

http://blog.chinaunix.net/uid-21237130-id-159816.html
