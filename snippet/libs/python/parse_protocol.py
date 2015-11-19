# coding: utf-8
"""
Parse the TCP/IP.
"""
from __future__ import print_function
import sys
import copy
import socket
import struct


if sys.version_info[0] == 3:
    PY3 = True
    strings = (str, unicode)
else:
    PY3 = False
    strings = (str, bytes)


def inet_ntop(family, packet_ip):
    ntop = getattr(socket, 'inet_ntop', None)
    if ntop:
        return ntop(family, packet_ip)
    return getattr(socket, 'inet_ntoa')(packet_ip)


class ParseProtocol(object):
    _inner_attr = ('next', '_values', '_new_names')

    def __init__(self, data=None, next=True):
        self._values = {}
        self._new_names = {}
        self.next = None
        if data:
            self.parse(data, next)

    def __call__(self, data, next=True):
        return self.parse(data, next)

    def __getattr__(self, name):
        if name in self._values:
            return self._values[name]

        if name in self._new_names:
            return self._values[self._new_names[name]]

        return None

    def __getitem__(self, name):
        if isinstance(name, strings):
            name = name.replace('-', '_')
            return getattr(self, name)
        return None

    def __setattr__(self, name, value):
        if name in self._inner_attr:
            return object.__setattr__(self, name, value)
        self._values[name] = value

    def register(self, old_name, new_name):
        new_name = new_name.replace('-', '_')
        # if old_name not in self._values:
        #     raise ValueError("{0} does not exist".format(old_name))
        self._new_name[new_name] = old_name

    def registers(self, opts):
        if isinstance(opts, dict):
            for k in opts:
                self.register(k, opts[k])
        else:
            for old, new in opts:
                self.register(old, new)

    def to_dict(self):
        tmp = copy.deepcopy(self._values)
        tmp['name'] = self.name
        for name in self._new_names:
            if name in tmp:
                tmp[self._new_names[name]] = tmp.pop(name)
        if self.next:
            tmp['next'] = self.next.to_dict()
        return tmp

    def __str__(self):
        return str(self.to_dict())

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def _parse(self, data, next=True):
        raise NotImplemented("Must be implemented")

    def parse(self, data, next=True):
        try:
            return self._parse(data, next)
        except NotImplemented:
            raise
        except Exception:
            return None


class ParseMAC(ParseProtocol):
    name = 'mac'

    def _parse(self, data, next=True):
        self.dst_mac = [ord(i) for i in data[:6]]
        self.src_mac = [ord(i) for i in data[6:12]]
        self.frame_type = struct.unpack('!H', data[12:14])[0]

        _data = data[14:]
        if next:
            if self.frame_type == 0x0800:  # IPv4
                self.next = ParseIPv4(_data)
            elif self.frame_type == 0x86dd:  # IPv6
                self.next = ParseIPv6(_data)
            elif self.frame_type == 0x0806:  # ARP
                self.next = ParseARP(_data)
            elif self.frame_type == 0x8035:  # RARP
                self.next = ParseARP(_data)
        return _data


class ParseARP(ParseProtocol):
    name = 'arp'

    def _parse(self, data, next=True):
        self.hardware_addr_type = struct.unpack('!H', data[0:2])[0]
        self.protocol_addr_type = struct.unpack('!H', data[2:4])[0]
        self.hardware_addr_len = ord(data[4])
        self.protocol_addr_len = ord(data[5])

        tmp = struct.unpack('!H', data[6:8])[0]
        if tmp == 1:
            self.protocol = 'arp_request'
        elif tmp == 2:
            self.protocol = 'arp_reply'
        elif tmp == 3:
            self.protocol = 'rarp_request'
        elif tmp == 4:
            self.protocol = 'rarp_reply'

        self.src_mac = [ord(i) for i in data[8:14]]
        self.src_ip = inet_ntop(socket.AF_INET, data[14:18])
        self.dst_mac = [ord(i) for i in data[18:24]]
        self.dst_ip = inet_ntop(socket.AF_INET, data[24:28])


class ParseIPv4(ParseProtocol):
    name = 'ipv4'

    def _parse(self, data, next=True):
        ver_headerlen = ord(data[0])
        self.version = ver_headerlen / 16
        self.header_len = (ver_headerlen % 16) * 4
        self.service_type = ord(data[1])
        self.total_len = struct.unpack('!H', data[2:4])[0]
        self.identification = struct.unpack('!H', data[4:6])[0]

        tmp = struct.unpack('!H', data[6:8])[0]
        self.fragment_offset = tmp & 0b0001111111111111
        self.not_fragment = bool(tmp & 0b0100000000000000)
        self.more_fragment = bool(tmp & 0b0010000000000000)
        self.ttl = ord(data[8])
        self.protocol = ord(data[9])
        self.src_ip = inet_ntop(socket.AF_INET, data[12:16])
        self.dst_ip = inet_ntop(socket.AF_INET, data[16:20])

        tmp = self.header_len
        _data = data[tmp:]
        if next:
            if self.protocol == 1:     # ICMP
                self.next = ParseICMP(_data)
            elif self.protocol == 6:   # TCP
                self.next = ParseTCP(_data)
            elif self.protocol == 17:  # UDP
                self.next = ParseUDP(_data)
        return _data


class ParseIPv6(ParseProtocol):
    name = 'ipv6'

    def _parse(self, data, next=True):
        ver_headerlen = ord(data[0])
        self.version = ver_headerlen / 16
        self.ttl = ord(data[7])
        self.src_ip = inet_ntop(socket.AF_INET6, data[8:24])
        self.dst_ip = inet_ntop(socket.AF_INET6, data[24:40])
        self.protocol = ord(data[6])

        tmp = 40
        _data = data[tmp:]
        if next:
            if self.protocol == 1:     # ICMP
                self.next = ParseICMP(_data)
            elif self.protocol == 6:   # TCP
                self.next = ParseTCP(_data)
            elif self.protocol == 17:  # UDP
                self.next = ParseUDP(_data)
        return _data


class ParseICMP(ParseProtocol):
    name = 'icmp'

    def _parse(self, data, next=True):
        self.type = ord(data[0])
        self.code = ord(data[1])
        self.identifier = struct.unpack('!H', data[4:6])[0]
        self.sequence = struct.unpack('!H', data[6:8])[0]


class ParseUDP(ParseProtocol):
    name = 'udp'

    def _parse(self, data, next=True):
        self.src_port = struct.unpack('!H', data[0:2])[0]
        self.dst_port = struct.unpack('!H', data[2:4])[0]
        self.length = struct.unpack('!H', data[4:6])[0]
        return data[8:]


class ParseTCP(ParseProtocol):
    name = 'tcp'

    def _parse(self, data, next=True):
        self.src_port = struct.unpack('!H', data[0:2])[0]
        self.dst_port = struct.unpack('!H', data[2:4])[0]
        self.sequence_number = struct.unpack('!I', data[4:8])[0]
        self.acknowledgment_number = struct.unpack('!I', data[8:12])[0]

        tmp = ord(data[12])
        self.offset = (tmp / 16) * 4

        # TCP Flags
        tmp = ord(data[13])
        self.reduced = bool(tmp & 0b10000000)   # C
        self.ecn_echo = bool(tmp & 0b01000000)  # E
        self.urgent = bool(tmp & 0b00100000)    # U
        self.ack = bool(tmp & 0b00010000)       # A
        self.push = bool(tmp & 0b00001000)      # P
        self.reset = bool(tmp & 0b00000100)     # R
        self.syn = bool(tmp & 0b00000010)       # S
        self.fin = bool(tmp & 0b00000001)       # F
        #####
        self.C = self.reduced
        self.E = self.ecn_echo
        self.U = self.urgent
        self.A = self.ack
        self.P = self.push
        self.R = self.reset
        self.S = self.syn
        self.F = self.fin

        self.window = struct.unpack('!H', data[14:16])[0]

        tmp = self.offset
        return data[tmp:]


def parse_mac(data):
    parse = ParseMAC(data)
    return parse.to_dict()


def pp(data):
    import pprint
    pprint.pprint(parse_mac(data))


if __name__ == "__main__":
    data = sys.argv[1:]
    pp(data)
