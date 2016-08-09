`SO_REUSEADDR` and `SO_REUSEPORT`
=================================

Welcome to the wonderful world of portability... or rather the lack of it. Before we start analyzing these two options in detail and take a deeper look how different operating systems handle them, it should be noted that the BSD socket implementation is the mother of all socket implementations. Basically all other systems copied the BSD socket implementation at some point of time (or at least its interfaces) and then started to evolving it on their own. Of course the BSD socket implementation was evolved as well at the same time and thus systems that copied it later got features that were lacking in systems that copied it earlier. Understanding the BSD socket implementation is the key to understanding all other socket implementations, so you should read about it even if you don't care to ever write code for a BSD system.

There are a couple of basics you should know before we look at these two options. A TCP/UDP connection is identified by a tuple of five values:
```
{<protocol>, <src addr>, <src port>, <dest addr>, <dest port>}
```

Any unique combination of these values identifies a connection. As a result, no two connections can have the same five values, otherwise the system would not be able to distinguish these connections any longer.

The protocol of a socket is set when a socket is created with the `socket()` function. The source address and port are set with the `bind()` function. The destination address and port are set with the `connect()` function. Since UDP is a connectionless protocol, UDP sockets can be used without connecting them. Yet it is allowed to connect them and in some cases very advantageous for your code and general application design. In connectionless mode, UDP sockets that were not explicitly bound when data is sent over them for the first time are usually automatically bound by the system, as an unbound UDP socket cannot receive any (reply) data. Same is true for an unbound TCP socket, it is automatically bound before it will be connected.

If you explicitly bind a socket, it is possible to bind it to port 0, which means "any port". Since a socket cannot really be bound to all existing ports, the system will have to choose a specific port itself in that case (usually from a predefined, OS specific range of source ports). A similar wildcard exists for the source address, which can be "any address" (`0.0.0.0` in case of IPv4 and `::` in case of IPv6). Unlike in case of ports, a socket can really be bound to "any address" which means "all source IP addresses of all local interfaces". If the socket is connected later on, the system has to choose a specific source IP address, since a socket cannot be connected and at the same time be bound to any local IP address. Depending on the destination address and the content of the routing table, the system will pick an appropriate source address and replace the "any" binding with a binding to the chosen source IP address.

By default, no two sockets can be bound to the same combination of source address and source port. As long as the source port is different, the source address is actually irrelevant. Binding `socketA` to `A:X` and `socketB` to `B:Y`, where `A` and `B` are addresses and `X` and `Y` are ports, is always possible as long as `X != Y` holds true. However, even if `X == Y`, the binding is still possible as long as `A != B` holds true. E.g. `socketA` belongs to a FTP server program and is bound to `192.168.0.1:21` and `socketB` belongs to another FTP server program and is bound to `10.0.0.1:21`, both bindings will succeed. Keep in mind, though, that a socket may be locally bound to "any address". If a socket is bound to `0.0.0.0:21`, it is bound to all existing local addresses at the same time and in that case no other socket can be bound to port `21`, regardless which specific IP address it tries to bind to, as `0.0.0.0` conflicts with all existing local IP addresses.

Anything said so far is pretty much equal for all major operating system. Things start to get OS specific when address reuse comes into play. We start with BSD, since as I said above, it is the mother of all socket implementations.

## BSD

### SO_REUSEADDR

If `SO_REUSEADDR` is enabled on a socket prior to binding it, the socket can be successfully bound unless there is a conflict with another socket bound to **`exactly`** the same combination of source address and port. Now you may wonder how is that any different than before? The keyword is "exactly". `SO_REUSEADDR` mainly changes the way how wildcard addresses ("any IP address") are treated when searching for conflicts.

Without `SO_REUSEADDR`, binding `socketA` to `0.0.0.0:21` and then binding `socketB` to `192.168.0.1:21` will fail (with error `EADDRINUSE`), since `0.0.0.0` means "any local IP address", thus all local IP addresses are considered in use by this socket and this includes `192.168.0.1`, too. With `SO_REUSEADDR` it will succeed, since `0.0.0.0` and `192.168.0.1` are **`not exactly`** the same address, one is a wildcard for all local addresses and the other one is a very specific local address. Note that the statement above is true regardless in which order `socketA` and `socketB` are bound; without `SO_REUSEADDR` it will always fail, with `SO_REUSEADDR` it will always succeed.

To give you a better overview, let's make a table here and list all possible combinations:
```
SO_REUSEADDR       socketA        socketB       Result
---------------------------------------------------------------------
  ON/OFF       192.168.0.1:21   192.168.0.1:21    Error (EADDRINUSE)
  ON/OFF       192.168.0.1:21      10.0.0.1:21    OK
  ON/OFF          10.0.0.1:21   192.168.0.1:21    OK
   OFF             0.0.0.0:21   192.168.1.0:21    Error (EADDRINUSE)
   OFF         192.168.1.0:21       0.0.0.0:21    Error (EADDRINUSE)
   ON              0.0.0.0:21   192.168.1.0:21    OK
   ON          192.168.1.0:21       0.0.0.0:21    OK
  ON/OFF           0.0.0.0:21       0.0.0.0:21    Error (EADDRINUSE)
```

The table above assumes that `socketA` has already been successfully bound to the address given for `socketA`, then `socketB` is created, either gets `SO_REUSEADDR` set or not, and finally is bound to the address given for `socketB`. `Result` is the result of the bind operation for `socketB`. If the first column says `ON/OFF`, the value of `SO_REUSEADDR` is irrelevant to the result.

Okay, `SO_REUSEADDR` has an effect on wildcard addresses, good to know. Yet that isn't it's only effect it has. There is another well known effect which is also the reason why most people use `SO_REUSEADDR` in server programs in the first place. For the other important use of this option we have to take a deeper look on how the TCP protocol works.

A socket has a send buffer and if a call to the `send()` function succeeds, it does not mean that the requested data has actually really been sent out, it only means the data has been added to the send buffer. For UDP sockets, the data is usually sent pretty soon, if not immediately, but for TCP sockets, there can be a relatively long delay between adding data to the send buffer and having the TCP implementation really send that data. As a result, when you close a TCP socket, there may still be pending data in the send buffer, which has not been sent yet but your code considers it as sent, since the `send()` call succeeded. If the TCP implementation was closing the socket immediately on your request, all of this data would be lost and your code wouldn't even know about that. TCP is said to be a reliable protocol and losing data just like that is not very reliable. That's why a socket that still has data to send will go into a state called `TIME_WAIT` when you close it. In that state it will wait until all pending data has been successfully sent or until a timeout is hit, in which case the socket is closed forcefully.

The amount of time the kernel will wait before it closes the socket, regardless if it still has pending send data or not, is called the `Linger Time`. The `Linger Time` is globally configurable on most systems and by default rather long (two minutes is a common value you will find on many systems). It is also configurable per socket using the socket option `SO_LINGER` which can be used to make the timeout shorter or longer, and even to disable it completely. Disabling it completely is a very bad idea, though, since closing a TCP socket gracefully is a slightly complex process and involves sending forth and back a couple of packets (as well as resending those packets in case they got lost) and this whole close process is also limited by the `Linger Time`. If you disable lingering, your socket may not only lose pending data, it is also always closed forcefully instead of gracefully, which is usually not recommended. The details about how a TCP connection is closed gracefully are beyond the scope of this answer, if you want to learn more about, I recommend you have a look at [this page](http://www.freesoft.org/CIE/Course/Section4/11.htm). And even if you disabled lingering with `SO_LINGER`, if your process dies without explicitly closing the socket, BSD (and possibly other systems) will linger nonetheless, ignoring what you have configured. This will happen for example if your code just calls `exit()` (pretty common for tiny, simple server programs) or the process is killed by a signal (which includes the possibility that it simply crashes because of an illegal memory access). So there is nothing you can do to make sure a socket will never linger under all circumstances.

The question is, how does the system treat a socket in state `TIME_WAIT`? If `SO_REUSEADDR` is not set, a socket in state `TIME_WAIT` is considered to still be bound to the source address and port and any attempt to bind a new socket to the same address and port will fail until the socket has really been closed, which may take as long as the configured `Linger Time`. So don't expect that you can rebind the source address of a socket immediately after closing it. In most cases this will fail. However, if `SO_REUSEADDR` is set for the socket you are trying to bind, another socket bound to the same address and port in state `TIME_WAIT` is simply ignored, after all its already "half dead", and your socket can bind to exactly the same address without any problem. In that case it plays no role that the other socket may have exactly the same address and port. Note that binding a socket to exactly the same address and port as a dying socket in `TIME_WAIT` state can have unexpected, and usually undesired, side effects in case the other socket is still "at work", but that is beyond the scope of this answer and fortunately those side effects are rather rare in practice.

There is one final thing you should know about `SO_REUSEADDR`. Everything written above will work as long as the socket you want to bind to has address reuse enabled. It is not necessary that the other socket, the one which is already bound or is in a `TIME_WAIT` state, also had this flag set when it was bound. The code that decides if the bind will succeed or fail only inspects the `SO_REUSEADDR` flag of the socket fed into the `bind()` call, for all other sockets inspected, this flag is not even looked at.

### SO_REUSEPORT

`SO_REUSEPORT` is what most people would expect `SO_REUSEADDR` to be. Basically, `SO_REUSEPORT` allows you to bind an arbitrary number of sockets to **`exactly`** the same source address and port as long as **`all`** prior bound sockets also had `SO_REUSEPORT` set before they were bound. If the first socket that is bound to an address and port does not have `SO_REUSEPORT` set, no other socket can be bound to exactly the same address and port, regardless if this other socket has `SO_REUSEPORT` set or not, until the first socket releases its binding again. Unlike in case of `SO_REUESADDR` the code handling `SO_REUSEPORT` will not only verify that the currently bound socket has `SO_REUSEPORT` set but it will also verify that the socket with a conflicting address and port had `SO_REUSEADDR` set when it was bound.

`SO_REUSEPORT` does not imply `SO_REUSEADDR`. This means if a socket did not have `SO_REUSEPORT` set when it was bound and another socket has `SO_REUSEPORT` set when it is bound to exactly the same address and port, the bind fails, which is expected, but it also fails if the other socket is already dying and is in `TIME_WAIT` state. To be able bind a socket to the same addresses and port as another socket in `TIME_WAIT` state requires either `SO_REUSEADDR` to be set on that socket or `SO_REUSEPORT` must have been set **`on both`** sockets prior to binding them. Of course it is allowed to set both, `SO_REUSEPORT` and `SO_REUSEADDR`, on a socket.

There is not much more to say about `SO_REUSEPORT` other than that it was added later than `SO_REUSEADDR`, that's why you will not find it in many socket implementations of other systems, which "forked" the BSD code before this option was added, and that there was no way to bind two sockets to exactly the same socket address in BSD prior to this option.

### `Connect()` Returning `EADDRINUSE`?

Most people know that `bind()` may fail with the error `EADDRINUSE`, however, when you start playing around with address reuse, you may run into the strange situation that `connect()` fails with that error as well. How can this be? How can a remote address, after all that's what connect adds to a socket, be already in use? Connecting multiple sockets to exactly the same remote address has never been a problem before, so what's going wrong here?

As I said on the very top of my reply, a connection is defined by a tuple of five values, remember? And I also said, that these five values must be unique otherwise the system cannot distinguish two connections any longer, right? Well, with address reuse, you can bind two sockets of the same protocol to the same source address and port. That means three of those five values are already the same for these two sockets. If you now try to connect both of these sockets also to the same destination address and port, you would create two connected sockets, whose tuples are absolutely identical. This cannot work, at least not for TCP connections (UDP connections are no real connections anyway). If data arrived for either one of the two connections, the system could not tell which connection the data belongs to. At least the destination address or destination port must be different for either connection, so that the system has no problem to identify to which connection incoming data belongs to.

So if you bind two sockets of the same protocol to the same source address and port and try to connect them both to the same destination address and port, `connect()` will actually fail with the error `EADDRINUSE` for the second socket you try to connect, which means that a socket with an identical tuple of five values is already connected.

### Multicast Addresses

Most people ignore the fact that multicast addresses exist, but they do exist. While unicast addresses are used for one-to-one communication, multicast addresses are used for one-to-many communication. Most people got aware of multicast addresses when they learned about IPv6 but multicast addresses also existed in IPv4, even though this feature was never widely used on the public Internet.

The meaning of `SO_REUSEADDR` changes for multicast addresses as it allows multiple sockets to be bound to exactly the same combination of source multicast address and port. In other words, for multicast addresses `SO_REUSEADDR` behaves exactly as `SO_REUSEPORT` for unicast addresses. Actually the code treats `SO_REUSEADDR` and `SO_REUSEPORT` identically for multicast addresses, that means you could say that `SO_REUSEADDR` implies `SO_REUSEPORT` for all multicast addresses and the other way round.


## FreeBSD/OpenBSD/NetBSD

All these are rather late forks of the original BSD code, that's why they all three offer the same options as BSD and they also behave the same way as in BSD.


## MacOS X

At its very core, MacOS X is simply a BSD-style UNIX, based on a rather late fork of the BSD code, which was even synchronized with FreeBSD 5 for the Mac OS 10.3 release. That's why MacOS X offers the same options as BSD and they also behave the same way as in BSD.


## iOS

iOS is just modified MacOS X at its core, so everything that applies to MacOS X also applies to iOS.


## Linux

Prior to `Linux 3.9`, only the option `SO_REUSEADDR` existed. This option behaves generally the same as in BSD with two important exceptions. One exception is that if a listening (server) TCP socket is already bound to a wildcard IP address and a specific port, no other TCP socket can be bound to the same port, regardless whether either one or both sockets have this flag set. Not even if it would use a more specific address (as is allowed in case of BSD). This restriction does not apply to non-listening (client) TCP sockets and it is also possible to first bind a listening TCP socket to a specific IP address and port combination and later on bind another one to a wildcard IP address and the same port. The second exception is that for UDP sockets this option behaves exactly like `SO_REUSEPORT` in BSD, so two UDP sockets can be bound to exactly the same address and port combination as long as both had this flag set before they were bound.

`Linux 3.9` added the option `SO_REUSEPORT` to Linux as well. This option allows two (or more) sockets, TCP or UDP, listening (server) or non-listening (client), to be bound to exactly the same address and port combination as long as all sockets (including the very first one) had this flag set prior to binding them. To prevent "port hijacking", there is one special limitation, though: All sockets that want to share the same address and port combination must belong to processes that share the same effective user ID! So one user cannot "steal" ports of another user. Additionally the kernel performs some "special magic" for `SO_REUSEPORT` sockets that isn't found in any other operating system so far: For UDP sockets, it tries to distribute datagrams evenly, for TCP listening sockets, it tries to distribute incoming connect requests (those accepted by calling `accept()`) evenly across all the sockets that share the same address and port combination. That means while it is more or less random which socket receives a datagram or connect request in other operating systems that allow full address reuse, Linux tries to optimize distribution so that, for example, multiple instances of a simple server process can easily use `SO_REUSEPORT` sockets to achieve a kind of simple load balancing and that absolutely for free as the kernel is doing "all the hard work" for them.


## Android

Even though the whole Android system is somewhat different from most Linux distributions, at its core works a slightly modified Linux kernel, thus everything that applies to Linux applies to Android as well.


## Windows

Windows only knows the `SO_REUSEADDR` option, there is no `SO_REUSEPORT`. Setting `SO_REUSEADDR` on a socket in Windows behaves like setting `SO_REUSEPORT` and `SO_REUSEADDR` on a socket in BSD, with one exception: A socket with `SO_REUSEADDR` can always bind to exactly the same source address and port as an already bound socket, **even if the other socket did not have this option set when it was bound**. This behavior is somewhat dangerous because it allows an application "to steal" the connected port of another application. Needless to say, this can have major security implications. Microsoft realized that this might be a problem and thus added another socket option `SO_EXCLUSIVEADDRUSE`. Setting `SO_EXCLUSIVEADDRUSE` on a socket makes sure that if the binding succeeds, the combination of source address and port is owned exclusively by this socket and no other socket can bind to them, not even if it has `SO_REUSEADDR` set.


## Solaris

Solaris is the successor of SunOS. SunOS was originally based on a fork of BSD, SunOS 5 and later was based on a fork of SVR4, however SVR4 is a merge of BSD, System V, and Xenix, so up to some degree Solaris is also a BSD fork, and a rather early one. As a result Solaris only knows `SO_REUSEADDR`, there is no `SO_REUSEPORT`. The `SO_REUSEADDR` behaves pretty much the same as it does in BSD. As far as I know there is no way to get the same behavior as `SO_REUSEPORT` in Solaris, that means it is not possible to bind two sockets to exactly the same address and port.

Similar to Windows, Solaris has an option to give a socket an exclusive binding. This option is named `SO_EXCLBIND`. If this option is set on a socket prior to binding it, setting `SO_REUSEADDR` on another socket has no effect if the two sockets are tested for an address conflict. E.g. if `socketA` is bound to a wildcard address and `socketB` has `SO_REUSEADDR` enabled and is bound to a non-wildcard address and the same port as `socketA`, this bind will normally succeed, unless `socketA` had `SO_EXCLBIND` enabled, in which case it will fail regardless the `SO_REUSEADDR` flag of `socketB`.

------

From: http://stackoverflow.com/questions/14388706/socket-options-so-reuseaddr-and-so-reuseport-how-do-they-differ-do-they-mean-t

Reference:
- [SO_REUSEPORT学习笔记](http://www.blogjava.net/yongboy/archive/2015/02/12/422893.html)
