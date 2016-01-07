
### Q: I hear OVS has a couple of kinds of flows.  Can you tell me about them?

A: Open vSwitch uses different kinds of flows for different purposes:

      - OpenFlow flows are the most important kind of flow.  OpenFlow
        controllers use these flows to define a switch's policy.
        OpenFlow flows support wildcards, priorities, and multiple
        tables.

        When in-band control is in use, Open vSwitch sets up a few
        "hidden" flows, with priority higher than a controller or the
        user can configure, that are not visible via OpenFlow.  (See
        the "Controller" section of the FAQ for more information
        about hidden flows.)

      - The Open vSwitch software switch implementation uses a second
        kind of flow internally.  These flows, called "datapath" or
        "kernel" flows, do not support priorities and comprise only a
        single table, which makes them suitable for caching.  (Like
        OpenFlow flows, datapath flows do support wildcarding, in Open
        vSwitch 1.11 and later.)  OpenFlow flows and datapath flows
        also support different actions and number ports differently.

        Datapath flows are an implementation detail that is subject to
        change in future versions of Open vSwitch.  Even with the
        current version of Open vSwitch, hardware switch
        implementations do not necessarily use this architecture.

   Users and controllers directly control only the OpenFlow flow
   table.  Open vSwitch manages the datapath flow table itself, so
   users should not normally be concerned with it.

### Q: Why are there so many different ways to dump flows?

A: Open vSwitch has two kinds of flows (see the previous question), so
   it has commands with different purposes for dumping each kind of
   flow:

      - "ovs-ofctl dump-flows <br>" dumps OpenFlow flows, excluding
        hidden flows.  This is the most commonly useful form of flow
        dump.  (Unlike the other commands, this should work with any
        OpenFlow switch, not just Open vSwitch.)

      - "ovs-appctl bridge/dump-flows <br>" dumps OpenFlow flows,
        including hidden flows.  This is occasionally useful for
        troubleshooting suspected issues with in-band control.

      - "ovs-dpctl dump-flows [dp]" dumps the datapath flow table
        entries for a Linux kernel-based datapath.  In Open vSwitch
        1.10 and later, ovs-vswitchd merges multiple switches into a
        single datapath, so it will show all the flows on all your
        kernel-based switches.  This command can occasionally be
        useful for debugging.

      - "ovs-appctl dpif/dump-flows <br>", new in Open vSwitch 1.10,
        dumps datapath flows for only the specified bridge, regardless
        of the type.
