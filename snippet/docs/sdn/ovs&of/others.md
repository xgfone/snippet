
### Q: How do I connect two bridges?
```
A: First, why do you want to do this?  Two connected bridges are not
   much different from a single bridge, so you might as well just have
   a single bridge with all your ports on it.

   If you still want to connect two bridges, you can use a pair of
   patch ports.  The following example creates bridges br0 and br1,
   adds eth0 and tap0 to br0, adds tap1 to br1, and then connects br0
   and br1 with a pair of patch ports.

       ovs-vsctl add-br br0
       ovs-vsctl add-port br0 eth0
       ovs-vsctl add-port br0 tap0
       ovs-vsctl add-br br1
       ovs-vsctl add-port br1 tap1
       ovs-vsctl \
           -- add-port br0 patch0 \
           -- set interface patch0 type=patch options:peer=patch1 \
           -- add-port br1 patch1 \
           -- set interface patch1 type=patch options:peer=patch0

   Bridges connected with patch ports are much like a single bridge.
   For instance, if the example above also added eth1 to br1, and both
   eth0 and eth1 happened to be connected to the same next-hop switch,
   then you could loop your network just as you would if you added
   eth0 and eth1 to the same bridge (see the "Configuration Problems"
   section below for more information).

   If you are using Open vSwitch 1.9 or an earlier version, then you
   need to be using the kernel module bundled with Open vSwitch rather
   than the one that is integrated into Linux 3.3 and later, because
   Open vSwitch 1.9 and earlier versions need kernel support for patch
   ports.  This also means that in Open vSwitch 1.9 and earlier, patch
   ports will not work with the userspace datapath, only with the
   kernel module.
```
