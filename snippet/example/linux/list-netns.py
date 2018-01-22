#!/usr/bin/python
#
# List all Namespaces (works for Ubuntu 12.04 and higher)
#
# (C) Ralf Trezeciak    2013-2014
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import print_function

import os
import fnmatch

if os.geteuid() != 0:
    print("This script must be run as root\nBye")
    exit(1)


def getinode(pid, type):
    link = '/proc/' + pid + '/ns/' + type
    ret = ''
    try:
        ret = os.readlink(link)
    except OSError:
        ret = ''
    return ret


#
# get the running command
def getcmd(p):
    try:
        cmd = open(os.path.join('/proc', p, 'cmdline'), 'rb').read()
        if cmd == '':
            cmd = open(os.path.join('/proc', p, 'comm'), 'rb').read()
        cmd = cmd.replace('\x00', ' ')
        cmd = cmd.replace('\n', ' ')
        return cmd
    except Exception:
        return ''


#
# look for docker parents
def getpcmd(p):
    try:
        f = '/proc/' + p + '/stat'
        arr = open(f, 'rb').read().split()
        cmd = getcmd(arr[3])
        if cmd.startswith('/usr/bin/docker'):
            return 'docker'
    except Exception:
        pass
    return ''


#
# get the namespaces of PID=1
# assumption: these are the namespaces supported by the system
#
nslist = os.listdir('/proc/1/ns/')
if not nslist:
    print('No Namespaces found for PID=1')
    exit(1)

#print nslist
#
# get the inodes used for PID=1
#
baseinode = []
for x in nslist:
    baseinode.append(getinode('1', x))
#print "Default namespaces: " , baseinode
err = 0
ns = []
ipnlist = []

#
# loop over the network namespaces created using "ip"
#
try:
    netns = os.listdir('/var/run/netns/')
    for p in netns:
        fd = os.open('/var/run/netns/' + p, os.O_RDONLY)
        info = os.fstat(fd)
        os.close(fd)
        ns.append('-- net:[' + str(info.st_ino) + '] created by ip netns add ' + p)
        ipnlist.append('net:[' + str(info.st_ino) + ']')
except Exception:
    # might fail if no network namespaces are existing
    pass

#
# walk through all pids and list diffs
#
pidlist = fnmatch.filter(os.listdir('/proc/'), '[0123456789]*')
#print pidlist
for p in pidlist:
    try:
        pnslist = os.listdir('/proc/' + p + '/ns/')
        for x in pnslist:
            i = getinode(p, x)
            if i != '' and i not in baseinode:
                cmd = getcmd(p)
                pcmd = getpcmd(p)
                if pcmd != '':
                    cmd = '[' + pcmd + '] ' + cmd
                tag = ''
                if i in ipnlist:
                    tag = '**'
                ns.append(p + ' ' + i + tag + ' ' + cmd)
    except Exception:
        # might happen if a pid is destroyed during list processing
        pass

#
# print the stuff
#
print('{0:>10}  {1:20}  {2}'.format('PID', 'Namespace', 'Thread/Command'))
for e in ns:
    x = e.split(' ', 2)
    print('{0:>10}  {1:20}  {2}'.format(x[0], x[1], x[2][:60]))
