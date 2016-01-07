
### Q: I created a GRE port using ovs-vsctl so why can't I send traffic or see the port in the datapath?

A: On Linux kernels before 3.11, the OVS GRE module and Linux GRE module
   cannot be loaded at the same time. It is likely that on your system the
   Linux GRE module is already loaded and blocking OVS (to confirm, check
   dmesg for errors regarding GRE registration). To fix this, unload all
   GRE modules that appear in lsmod as well as the OVS kernel module. You
   can then reload the OVS module following the directions in INSTALL,
   which will ensure that dependencies are satisfied.

### Q: What destination UDP port does the VXLAN implementation in Open vSwitch use?

A: By default, Open vSwitch will use the assigned IANA port for VXLAN, which
   is 4789. However, it is possible to configure the destination UDP port
   manually on a per-VXLAN tunnel basis. An example of this configuration is
   provided below.

      ovs-vsctl add-br br0
      ovs-vsctl add-port br0 vxlan1 -- set interface vxlan1 \
         type=vxlan options:remote_ip=192.168.1.2 options:key=flow \
         options:dst_port=8472
