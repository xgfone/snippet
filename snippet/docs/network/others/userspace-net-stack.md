
#### [DPDK](http://dpdk.org/)
    DPDK is a set of libraries and drivers for fast packet processing. It was designed to run on any processors.
    The first supported CPU was Intel x86 and it is now extended to IBM Power 8, EZchip TILE-Gx and ARM.
    It runs mostly in Linux userland. A FreeBSD port is available for a subset of DPDK features.

    DPDK is not a networking stack and does not provide functions such as Layer-3 forwarding, IPsec, firewalling, etc.

#### [netmap](https://github.com/luigirizzo/netmap)
    NETMAP is a framework for very fast packet I/O from userspace.
    VALE is an equally fast in-kernel software switch using the netmap API.
    Both are implemented as a single kernel module for FreeBSD, Linux and since summer 2015, also for Windows.

#### [mtcp](https://github.com/eunyoung14/mtcp)
    A Highly Scalable User-level TCP Stack for Multicore Systems
