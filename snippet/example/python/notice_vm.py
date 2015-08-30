#!/usr/bin/env python
## -*- coding: utf-8 -*-
### notice_vm.py ---
##
## Filename: notice_vm.py
## Description: It's used to write the host IP into VM by kv_agent.
## Author: Gaofeng Xie
##
######################################################################
##
## copyright (C) 2013  DaoliCloud Information Technology(BeiJing)Co.,LTD
##
##    Licensed under the Apache License, Version 2.0 (the "License"); you may
##    not use this file except in compliance with the License. You may obtain
##    a copy of the License at
##
##         http://www.apache.org/licenses/LICENSE-2.0
##
##    Unless required by applicable law or agreed to in writing, software
##    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
##    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
##    License for the specific language governing permissions and limitations
##    under the License.
##
######################################################################
##
### Usage:
##    notice_vm.py [-h] [-m MOUNTPOINT] [-c CONFIGURE] [-i IMG] [-p N]
##                    [-I INTERFACE]
##
##    Write the host IP into VM by kv_agent
##
##    optional arguments:
##      -h, --help            show this help message and exit
##      -m MOUNTPOINT, --mountpoint MOUNTPOINT
##                            the mount point of the VM image
##      -c CONFIGURE, --configure CONFIGURE
##                            the configure file pathname
##      -i IMG, --img IMG     the VM image pathname
##      -p N, --partition N   the Nth partition in the VM image
##      -I INTERFACE, --interface INTERFACE
##                            the interface name, such as "eth0"
##
## Notice:
##    When importing this module, only create an anonymous Notice object
##    using the class Notice, such as Notice(img_path="/root/InnerLB.raw.img")
##
### Code:
##
#from __future__ import print_function
import os
import socket
import fcntl
import struct
import subprocess
import time

_IFNAME = "em1"  # "eth0"
_WORK_DIR = "/tmp"
_FILE_PATH = "/usr/local/haproxy/SocketHAproxy/daoli.conf"
_IMG_PATH = '/tmp/CentOS-6.4.img'
_MOUNT_PARTITION = 2


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tmp = fcntl.ioctl(s.fileno(),
                      0x8915,  # SIOCGIFADDR
                      struct.pack('256s', ifname[:15]))[20:24]
    s.close()
    return socket.inet_ntoa(tmp)


class Notice(object):
    def __init__(self, ifname=_IFNAME, mount_point=_WORK_DIR, file_path=_FILE_PATH,
                 img_path=_IMG_PATH, partition=_MOUNT_PARTITION):
        self.ifname = ifname
        self.file_path = file_path
        self.img_path = img_path
        self.partition = partition
        _mount_point = os.path.join(mount_point, os.path.basename(self.img_path))
        self.mount_point = "{0}.{1}".format(_mount_point, int(time.time()*1000000))

        self.mount = "lomount -diskimage {0} -partition {1} {2}".format(self.img_path,
                                                                        self.partition,
                                                                        self.mount_point)
        self.process()

    def _get_file_path(self, root, _file):
        if not root or not _file:
            return None

        if _file[0] == '/':
            return os.path.join(root, _file[1:])
        else:
            return os.path.join(root, _file)

    def process(self):
        file_path = self._get_file_path(self.mount_point, self.file_path)
        if not file_path:
            return False

        # Create the mount point.
        try:
            os.mkdir(self.mount_point)
        except:
            return False

        # Process the task.
        cmd_modify = "sed -i 's/^agent_host =.*/agent_host = {0}/g' {1}".format(get_ip_address(self.ifname), file_path)
        cmd_umount = "umount {}".format(self.mount_point)
        cmd = "{0} && {1} && {2}".format(self.mount, cmd_modify, cmd_umount)
        rtn = subprocess.call(cmd, shell=True)

        # Remove the mount point.
        if os.path.isdir(self.mount_point):
            try:
                os.rmdir(self.mount_point)
            except:
                return False

        if rtn:
            return False
        else:
            return True


def _get(obj, attr):
    tmp = getattr(obj, attr)
    if isinstance(tmp, (list, tuple)):
        return tmp[0]
    else:
        return tmp


if __name__ == "__main__":
    try:
        import argparse
    except:
        import optparse

        parser = optparse.OptionParser(description="Write the host IP into VM by kv_agent")
        parser.add_option('-m', '--mountpoint', nargs=1, default=_WORK_DIR, help="the mount point of the VM image")
        parser.add_option('-c', '--configure', nargs=1, default=_FILE_PATH, help="the configure file pathname")
        parser.add_option('-i', '--img', nargs=1, default=_IMG_PATH, help="the VM image pathname")
        parser.add_option('-p', '--partition', nargs=1, default=_MOUNT_PARTITION, metavar="N", help="the Nth partition in the VM image")
        parser.add_option('-I', '--interface', nargs=1, default=_IFNAME, help='the interface name, such as "eth0"')
        (args, ignores) = parser.parse_args()
    else:
        parser = argparse.ArgumentParser(description="Write the host IP into VM by kv_agent")
        parser.add_argument('-m', '--mountpoint', nargs=1, default=_WORK_DIR, help="the mount point of the VM image")
        parser.add_argument('-c', '--configure', nargs=1, default=_FILE_PATH, help="the configure file pathname")
        parser.add_argument('-i', '--img', nargs=1, default=_IMG_PATH, help="the VM image pathname")
        parser.add_argument('-p', '--partition', nargs=1, default=_MOUNT_PARTITION, metavar="N", help="the Nth partition in the VM image")
        parser.add_argument('-I', '--interface', nargs=1, default=_IFNAME, help='the interface name, such as "eth0"')
        args = parser.parse_args()

    _IFNAME = _get(args, "interface")
    _WORK_DIR = _get(args, "mountpoint")
    _FILE_PATH = _get(args, "configure")
    _IMG_PATH = _get(args, "img")
    _MOUNT_IMG_PARTITION = _get(args, "partition")

    Notice()

######################################################################
### notice_vm.py ends here
