# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import traceback
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import packet

try:
    from httplib import HTTPConnection, NotConnected
except Exception:
    from http.client import HTTPConnection, NotConnected

LOG = logging.getLogger(__name__)

_PHY_LOG_IP = {
    # LOG: PHY
    '10.1.1.10': '192.168.10.54',
    '10.1.1.11': '192.168.10.94',
}


def generate_key(tui, sip, dip, sport, dport):
    return sport + 10, dport + 10


def send_key(key):
    addr = '127.0.0.1'
    port = 8901
    method = "POST"
    url = '/ryu_daolicloud/'
    body = json.dumps(key)
    headers = {'Content-Type': 'application/json'}

    try:
        conn = HTTPConnection(addr, port, timeout=3)
        conn.request(method, url, body, headers)
        response = conn.getresponse()
        if response.status != 200:
            return False
    except NotConnected:
        return False
    except Exception:
        conn.close()
        return False
    return True


def get_out_ip(log_ip, src=True):
    return _PHY_LOG_IP.get(log_ip)


class NATSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION,
                    ]

    INET_PROTOCOL = {packet.icmp.icmp: "handle_icmp",
                     packet.tcp.tcp: "handle_tcp",
                     packet.udp.udp: "handle_udp"}

    def __init__(self, *args, **kwargs):
        super(NATSwitch, self).__init__(*args, **kwargs)
        self.tcp_ports = {}
        self.udp_ports = {}
        self.icmp_tcs = {}
        self.ip_fragment = {}

    def get_handler(self, key):
        for p in self.INET_PROTOCOL:
            if p == key or isinstance(key, p):
                method = self.INET_PROTOCOL[p]
                return getattr(self, method)
        return None

    def is_supported(self, protocol):
        if protocol in self.INET_PROTOCOL:
            return True
        elif isinstance(protocol, self.INET_PROTOCOL.keys()):
            return True
        else:
            return False

    def get_in_port(self, msg):
        if hasattr(msg, 'in_port'):
            return msg.in_port
        return msg.match['in_port']

    def _add_flow_arp_10(self, datapath, in_port=None, actions=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        if not actions:
            OFPP_FLOOD = ofproto.OFPP_FLOOD
            actions = [parser.OFPActionOutput(OFPP_FLOOD)]

        if in_port:
            args = {'eth_type': 0x0806, 'in_port': in_port}
        else:
            args = {'eth_type': 0x0806}

        match = parser.OFPMatch(**args)
        mod = parser.OFPFlowMod(datapath=datapath,
                                match=match,
                                command=ofproto.OFPFC_ADD,
                                actions=actions)
        datapath.send_msg(mod)

    def _add_flow_arp_13(self, datapath, in_port=None, actions=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        if not actions:
            OFPP_FLOOD = ofproto.OFPP_FLOOD
            actions = [parser.OFPActionOutput(OFPP_FLOOD)]

        if in_port:
            args = {'eth_type': 0x0806, 'in_port': in_port}
        else:
            args = {'eth_type': 0x0806}

        match = parser.OFPMatch(**args)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, match=match, instructions=inst)
        datapath.send_msg(mod)

    def add_flow_arp(self, datapath, in_port=None, actions=None):
        ofp_version = datapath.ofproto.OFP_VERSION

        if ofp_version == 0x01:  # OpenFlow 1.0
            return self._add_flow_arp_10(datapath, in_port, actions)

        if ofp_version == 0x03:  # OpenFlow 1.2
            return self._add_flow_arp_13(datapath, in_port, actions)

        if ofp_version == 0x04:  # OpenFlow 1.3
            return self._add_flow_arp_13(datapath, in_port, actions)

    def _add_flow_tui_10(self, tui, datapath, in_port, sip, dip, sport, dport, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        if tui == "tcp":
            args = {
                #'in_port': in_port,
                'eth_type': 0x0800,
                'ipv4_src': sip,
                'ipv4_dst': dip,
                'ip_proto': 6,
                'tcp_src': sport,
                'tcp_dst': dport,
            }
        elif tui == 'udp':
            args = {
                #'in_port': in_port,
                'eth_type': 0x0800,
                'ipv4_src': sip,
                'ipv4_dst': dip,
                'ip_proto': 17,
                'udp_src': sport,
                'udp_dst': dport,
            }
        elif tui == 'icmp':
            args = {
                #'in_port': in_port,
                'eth_type': 0x0800,
                'ipv4_src': sip,
                'ipv4_dst': dip,
                'ip_proto': 1,
                # 'icmpv4_type': sport,
                # 'icmpv4_code': dport,
            }
        else:
            return

        match = parser.OFPMatch(**args)

        # OpenFlow 1.0
        mod = parser.OFPFlowMod(datapath=datapath,
                                match=match,
                                command=ofproto.OFPFC_ADD,
                                actions=actions)

        datapath.send_msg(mod)

    def _add_flow_tui_13(self, tui, datapath, in_port, sip, dip, sport, dport, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        if tui == "tcp":
            args = {
                #'in_port': in_port,
                'eth_type': 0x0800,
                'ipv4_src': sip,
                'ipv4_dst': dip,
                'ip_proto': 6,
                'tcp_src': sport,
                'tcp_dst': dport,
            }
        elif tui == 'udp':
            args = {
                #'in_port': in_port,
                'eth_type': 0x0800,
                'ipv4_src': sip,
                'ipv4_dst': dip,
                'ip_proto': 17,
                'udp_src': sport,
                'udp_dst': dport,
            }
        elif tui == 'icmp':
            args = {
                #'in_port': in_port,
                'eth_type': 0x0800,
                'ipv4_src': sip,
                'ipv4_dst': dip,
                'ip_proto': 1,
                # 'icmpv4_type': sport,
                # 'icmpv4_code': dport,
            }
        else:
            return

        match = datapath.ofproto_parser.OFPMatch(**args)

        # OpenFlow 1.2, 1.3
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, match=match, instructions=inst)

        datapath.send_msg(mod)

    def add_flow_tui(self, tui, datapath, in_port, sip, dip, sport, dport, actions):
        ofp_version = datapath.ofproto.OFP_VERSION

        if ofp_version == 0x01:  # OpenFlow 1.0
            return self._add_flow_tui_10(tui, datapath, in_port, sip, dip, sport, dport, actions)

        if ofp_version == 0x03:  # OpenFlow 1.2
            return self._add_flow_tui_13(tui, datapath, in_port, sip, dip, sport, dport, actions)

        if ofp_version == 0x04:  # OpenFlow 1.3
            return self._add_flow_tui_13(tui, datapath, in_port, sip, dip, sport, dport, actions)

    def add_flow_tcp(self, datapath, in_port, sip, dip, sport, dport, actions):
        self.add_flow_tui('tcp', datapath, in_port, sip, dip, sport, dport, actions)

    def add_flow_udp(self, datapath, in_port, sip, dip, sport, dport, actions):
        self.add_flow_tui('udp', datapath, in_port, sip, dip, sport, dport, actions)

    def add_flow_icmp(self, datapath, in_port, sip, dip, actions):
        self.add_flow_tui('icmp', datapath, in_port, sip, dip, None, None, actions)

    def send_flood(self, datapath, msg):
        OFPP_FLOOD = datapath.ofproto.OFPP_FLOOD
        actions = [datapath.ofproto_parser.OFPActionOutput(OFPP_FLOOD)]

        args = {
            'datapath': datapath,
            'buffer_id': msg.buffer_id,
            'in_port': self.get_in_port(msg),
            'actions': actions,
        }
        out = datapath.ofproto_parser.OFPPacketOut(**args)
        datapath.send_msg(out)

    def send_normal(self, datapath, msg):
        OFPP_NORMAL = datapath.ofproto.OFPP_NORMAL
        actions = [datapath.ofproto_parser.OFPActionOutput(OFPP_NORMAL)]

        args = {
            'datapath': datapath,
            'buffer_id': msg.buffer_id,
            'in_port': self.get_in_port(msg),
            'actions': actions,
        }
        out = datapath.ofproto_parser.OFPPacketOut(**args)
        datapath.send_msg(out)

    def send_table(self, datapath, msg):
        OFPP_IN_PORT = datapath.ofproto.OFPP_TABLE
        actions = [datapath.ofproto_parser.OFPActionOutput(OFPP_IN_PORT)]

        args = {
            'datapath': datapath,
            'buffer_id': msg.buffer_id,
            'in_port': self.get_in_port(msg),
            'actions': actions,
        }
        out = datapath.ofproto_parser.OFPPacketOut(**args)
        datapath.send_msg(out)

    def send_out_port(self, datapath, msg, out_port):
        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        args = {
            'datapath': datapath,
            'buffer_id': msg.buffer_id,
            'in_port': self.get_in_port(msg),
            'actions': actions,
        }
        out = datapath.ofproto_parser.OFPPacketOut(**args)
        datapath.send_msg(out)

    # def _handle_tu(self, tu, msg, eth, ipv4, tu_obj, data):
    #     datapath = msg.datapath
    #     in_port = self.get_in_port(msg)
    #     ofproto = datapath.ofproto
    #     ofp_parser = datapath.ofproto_parser

    #     # Extract SIP, DIP, SPort, DPort
    #     sip = ipv4.src
    #     dip = ipv4.dst
    #     sport = tu_obj.src_port
    #     dport = tu_obj.dst_port

    #     ##################   Hast (SIP, DIP, SPort, DPort)   ###################
    #     # ip_pair = (sip, dip)
    #     # key = (sport, dport)
    #     # if tu == 'tcp':  # TCP
    #     #     if ip_pair in self.tcp_ports and key in self.tcp_ports[ip_pair]:  # This is a response
    #     #         info = self.tcp_ports[ip_pair][key]
    #     #         sport_action = {'tcp_src': info[2]}
    #     #         dport_actoin = {'tcp_dst': info[3]}
    #     #     else:  # This is a request
    #     #         key = generate_key(tu, sip, dip, sport, dport)
    #     #         sport_action = {'tcp_src': key[0]}
    #     #         dport_actoin = {'tcp_dst': key[1]}
    #     #         self.tcp_ports.setdefault(ip_pair, {})
    #     #         self.tcp_ports[ip_pair][key] = (sip, dip, sport, dport)
    #     # else:    # UDP
    #     #     if ip_pair in self.udp_ports and key in self.udp_ports[ip_pair]:  # This is a response
    #     #         info = self.udp_ports[ip_pair][key]
    #     #         sport_action = {'udp_src': info[2]}
    #     #         dport_actoin = {'udp_dst': info[3]}
    #     #     else:  # This is a request
    #     #         sport_action = {'udp_src': key[0]}
    #     #         dport_actoin = {'udp_dst': key[1]}
    #     #         self.udp_ports.setdefault(ip_pair, {})
    #     #         self.udp_ports[ip_pair][key] = (sip, dip, sport, dport)
    #     #
    #     # action1 = ofp_parser.OFPActionSetField(**sport_action)
    #     # action2 = ofp_parser.OFPActionSetField(**dport_actoin)
    #     # action3 = ofp_parser.OFPActionOutput(ofproto.OFPP_NORMAL)  # Output to a port
    #     # actions = [action1, action2, action3]
    #     # --------------------------------------------------------------

    #     sip_out = get_out_ip(sip)
    #     dip_out = get_out_ip(dip, False)

    #     key = generate_key(tu, sip, dip, sport, dport)
    #     #key = generate_key(tu, dip, sip, dport, sport, False)

    #     # Send the reversed flow table to the agent
    #     match = {'sip': sip_out,
    #              'dip': dip_out,
    #              'sport': key[0],
    #              'dport': key[1]}

    #     action = {'sip': sip,
    #               'dip': dip,
    #               'sport': sport,
    #               'dport': dport,
    #               'output': 'normal'}

    #     _info = {'type': tu,
    #              'datapath': dip_out,
    #              'match': match,
    #              'action': action,
    #              'method': 'passkey'}

    #     if not send_key(_info):
    #         return

    #     # Send the flow table to the switch about $datapath
    #     if tu == "tcp":  # TCP
    #         sport_action = {'tcp_src': key[0]}
    #         dport_action = {'tcp_dst': key[1]}
    #     else:            # UDP
    #         sport_action = {'udp_src': key[0]}
    #         dport_action = {'udp_dst': key[1]}

    #     action1 = ofp_parser.OFPActionSetField(ipv4_src=sip_out)
    #     action2 = ofp_parser.OFPActionSetField(ipv4_dst=dip_out)
    #     action3 = ofp_parser.OFPActionSetField(**sport_action)
    #     action4 = ofp_parser.OFPActionSetField(**dport_action)
    #     action5 = ofp_parser.OFPActionOutput(ofproto.OFPP_NORMAL)  # Output to a port
    #     actions = [action1, action2, action3, action4, action5]
    #     ########################################################################

    #     # actions = [ofp_parser.OFPActionOutput(ofproto.OFPP_NORMAL)]
    #     self.add_flow_tui(tu, datapath, in_port, sip, dip, sport, dport, actions)

    #     # Send the ethernet frame to the switch again.
    #     self.send_table(datapath, msg)

    def enqueue(self, msg, eth, ipv4, udp):
        sip = ipv4.src
        dip = ipv4.dst
        ip_id = ipv4.identification
        ip_key = (sip, dip, ip_id)
        value = (msg, eth, ipv4, udp)

        left_offset = (ipv4.flags & 0x1f) << 8
        offset = ipv4.offset + left_offset

        for index in self.ip_fragment[ip_key]:
            m, e, i, u = self.ip_fragment[ip_key][index]
            _lo = (i.flags & 0x1f) << 8
            _offset = i.offset + _lo
            if _offset < offset:
                self.ip_fragment[ip_key].insert(index, value)
                return

        self.ip_fragment[ip_key].append(value)

    def ip_is_comletion(self, msg, eth, ipv4, udp):
        sip = ipv4.src
        dip = ipv4.dst
        ip_id = ipv4.identification
        ip_key = (sip, dip, ip_id)

        last_ipv4 = self.ip_fragment[ip_key]
        if last_ipv4.frags & 0x20:
            return False

        # Judge whether there is the missing fragment.
        # TODO:)

    def _handle_udp_fragment(self, msg, eth, ipv4, udp, data):
        # datapath = msg.datapath
        # in_port = self.get_in_port(msg)
        # ofproto = datapath.ofproto
        # ofp_parser = datapath.ofproto_parser

        ip_id = ipv4.identification
        sip = ipv4.src
        dip = ipv4.dst
        # sport = udp.src_port
        # dport = udp.dst_port

        frag_key = (sip, dip, ip_id)
        if frag_key not in self.ip_fragment:  # cache
            self.ip_fragment[frag_key] = [(msg, eth, ipv4, udp)]
            return
        else:
            self.enqueue(msg, eth, ipv4, udp)

        # Judge whether the ip packet is completion
        if not self.ip_is_comletion(msg, eth, ipv4, udp):
            return

        # Handle the packet queue
        # (1) Issue the forword flow table
        # (2) Send the backword flow table
        # (3) Send the each fragment packet to the switch
        # TODO:)
        pass

    def _handle_tu_no_frags(self, tu, msg, eth, ipv4, tu_obj, data):
        datapath = msg.datapath
        in_port = self.get_in_port(msg)
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        # Extract SIP, DIP, SPort, DPort
        sip, dip = ipv4.src, ipv4.dst
        sport, dport = tu_obj.src_port, tu_obj.dst_port

        sip_out = get_out_ip(sip)
        dip_out = get_out_ip(dip, False)
        if not sip_out or not dip_out:
            return

        key = generate_key(tu, sip, dip, sport, dport)

        # Send the reversed flow table to the agent
        match = {'sip': sip_out,
                 'dip': dip_out,
                 'sport': key[0],
                 'dport': key[1]}

        action = {'sip': sip,
                  'dip': dip,
                  'sport': sport,
                  'dport': dport,
                  'output': 'normal'}

        _info = {'type': tu,
                 'datapath': dip_out,
                 'match': match,
                 'action': action,
                 'method': 'passkey'}

        if not send_key(_info):
            return

        # Send the flow table to the switch about $datapath
        if tu == "tcp":  # TCP
            sport_action = {'tcp_src': key[0]}
            dport_action = {'tcp_dst': key[1]}
        else:            # UDP
            sport_action = {'udp_src': key[0]}
            dport_action = {'udp_dst': key[1]}

        action1 = ofp_parser.OFPActionSetField(ipv4_src=sip_out)
        action2 = ofp_parser.OFPActionSetField(ipv4_dst=dip_out)
        action3 = ofp_parser.OFPActionSetField(**sport_action)
        action4 = ofp_parser.OFPActionSetField(**dport_action)
        action5 = ofp_parser.OFPActionOutput(ofproto.OFPP_NORMAL)  # Output to a port
        actions = [action1, action2, action3, action4, action5]

        self.add_flow_tui(tu, datapath, in_port, sip, dip, sport, dport, actions)

        # Send the ethernet frame to the switch again.
        self.send_table(datapath, msg)

    def handle_udp(self, msg, eth, ipv4, udp, data):
        fragment = ipv4.flags
        offset = ipv4.offset

        # don't permit to fragment, but fragment
        if fragment & 0x40 and ((fragment & 0x20) or offset):
            return
        elif not (fragment & 0x60) and not offset:  # not fragment
            self._handle_tu_no_frags("udp", msg, eth, ipv4, udp, data)
        else:                                       # fragment
            ### Don't handle Now.
            self.logger.info("Receive a UDP packet with fragment...... Discard!!!")
            return
            self._handle_udp_fragment(msg, eth, ipv4, udp, data)

    def handle_tcp(self, msg, eth, ipv4, tcp, data):
        self._handle_tu_no_frags("tcp", msg, eth, ipv4, tcp, data)

    def handle_icmp(self, msg, eth, ipv4, icmp, data):
        datapath = msg.datapath
        in_port = self.get_in_port(msg)
        ofproto, ofp_parser = datapath.ofproto, datapath.ofproto_parser

        # Extract SIP, DIP
        sip, dip = ipv4.src, ipv4.dst
        actions = [ofp_parser.OFPActionOutput(ofproto.OFPP_NORMAL)]
        self.add_flow_icmp(datapath, in_port, sip, dip, actions)
        self.send_table(datapath, msg)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath

        try:
            pkt = packet.packet.Packet(msg.data)
            eth, ip = pkt[0], pkt[1]
        except Exception:
            self.logger.info("%s", traceback.format_exc())
            return

        # Handle the ARP protocol
        if hasattr(ip, 'protocol_name') and ip.protocol_name == "arp":
            self.add_flow_arp(datapath)
            self.send_flood(datapath, msg)
            return

        # If not IPv4, not handle
        if not hasattr(ip, 'protocol_name') or ip.protocol_name != "ipv4":
            return
        else:
            tui = pkt[2]
            if len(pkt) > 3:
                data = pkt[3]
            else:
                data = None

        # If not tcp, udp, or icmp, not handle
        handler = self.get_handler(tui)
        if not handler:
            return

        # proto, n_proto_cls, n_data = n_proto_cls.parser(n_data)
        handler(msg, eth, ip, tui, data)

    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def _port_status_handler(self, ev):
        msg = ev.msg
        reason = msg.reason
        port_no = msg.desc.port_no

        ofproto = msg.datapath.ofproto
        if reason == ofproto.OFPPR_ADD:
            self.logger.info("port added %s", port_no)
        elif reason == ofproto.OFPPR_DELETE:
            self.logger.info("port deleted %s", port_no)
        elif reason == ofproto.OFPPR_MODIFY:
            self.logger.info("port modified %s", port_no)
        else:
            self.logger.info("Illeagal port state %s %s", port_no, reason)
