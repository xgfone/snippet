
DDOS Black Hole
===============

This document is meant as quick braindump. Take it as such.

### Blackhole efect of a victim

Victim of DDoS is acting (and being treated by attacker) as blackhole for IP packets. Many packets are flowing in and a little reply comes out of it. It hold as long as we consider duplex streams only. As multicast streams are not allowed for regular users the assumption should be generaly true. And we can use it to detect a victim.

### Victim detection at leaf gateway

Leaf gateway (where no multipath is in use toward client systems) should do very simple connection tracking of IP it routes. When it routes packet into backbone it creates record for src-dst IP addresses. It allows sending packets for some time T (say 30 secs) without actually geting a reply packet. Once reply packet has been seen the connection is "confirmed" for the same time T. If no reply packet is recieved then forward packets are shaped to rate 1 packet per T until a reply packet is recieved.

The result is that if this would be implemented on as many as possible leaf gateways (or even on larger backbone systems) it would allow victim to mitigate an attack by simply stopping its server and begin to gradualy start service for increasing parts of client IP space.

### Performance of implementation

When implementing this on Gbps link then we need to look whether it is possible with moderate ammount of HW. One conntrack record would need to carry at least

* state - 1 byte
* timestamp - 3 bytes
* IP pair - 8 bytes

Thus we need 8-12 byte records (depending on data structure) per conversation. Probably the best is to use stochastic approach and create hash table with size of 2^24 records which would need 160MByte of dedicated memory. The table would be keyed by last 3 octets of destination IP and acting as 1-way cache.
This way some records are not in table and can go thru. But we need not to kill 100% of data, 99% is good too. This approach should work well for systems with up to tens of thousands client IPs.

This filter can be implemented by fast PC runing some *nix system or dedicated hardware. One can take 2 pieces of 1Gbit chipset, FPGA in $100 range and implement the filter as 3 stage pipeline tied by dualported mems (fetch info for a packet, decide packet's fate, act on the packet and write the info back). With latest Spartan3 from Xilinx I can imagine cheap design with filter rate 10 Mpackets/s (use 133MHz/50ns SDRAM) which would be able to sustain 1Gbit rate. Not bad for under $200 design.

### Calculating safety measure

When implemented by majority of Internet with T=30s and number of attacking machines N=100.000 we get rate r=1500*N/T=50MBit. It is better than approx 5Gbit it could be without this system but still not so good. One could exponentially increase T of records which still sends packets against blackhole. T could reach something like 1hr which would allow victim to mitigate the attach under 1MBit which is likely manageable.

### Possible dangers

If implemented in system where IP spoofing is possible then one could "install" conntrack info for other clients. So ISP implementing this must implement source route validation too.

### Another benefits

The system would allow any host to develop/buy more advanced DDoS detector while blackhole detectors are providing framework doing actual filtering.

No cross-administrative-domain cooperation needed.

Port scanning made much more complex.

devik placeathere cdi placedothere cz

From: http://luxik.cdi.cz/~devik/qos/ddos-blackhole.htm
