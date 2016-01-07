
### Q: How do I assign the OpenFlow Port to a fixed port number?

A: Use 'ofport_request'.

    ovs-vsctl add-port br0 port_name -- set Interface port_name ofport_request=port_number
    ovs-ofctl mod-port br0 port_name up

### Q: How can I figure out the OpenFlow port number for a given port?
```
A: The OFPT_FEATURES_REQUEST message requests an OpenFlow switch to
   respond with an OFPT_FEATURES_REPLY that, among other information,
   includes a mapping between OpenFlow port names and numbers.  From a
   command prompt, "ovs-ofctl show br0" makes such a request and
   prints the response for switch br0.

   The Interface table in the Open vSwitch database also maps OpenFlow
   port names to numbers.  To print the OpenFlow port number
   associated with interface eth0, run:

       ovs-vsctl get Interface eth0 ofport

   You can print the entire mapping with:

       ovs-vsctl -- --columns=name,ofport list Interface

   but the output mixes together interfaces from all bridges in the
   database, so it may be confusing if more than one bridge exists.

   In the Open vSwitch database, ofport value -1 means that the
   interface could not be created due to an error.  (The Open vSwitch
   log should indicate the reason.)  ofport value [] (the empty set)
   means that the interface hasn't been created yet.  The latter is
   normally an intermittent condition (unless ovs-vswitchd is not
   running).
```
