#!/usr/bin/env python
# encoding: utf-8
"""
author:haoning
create time:2015.8.1
"""
import hashlib
import os
import time
import datetime
import traceback
import sys
import random
import json
import socket
import threading
from hashlib import sha1  # 进行hash加密
from random import randint
from struct import unpack
from socket import inet_ntoa
from threading import Timer, Thread
from time import sleep
from collections import deque
from Queue import Queue

import MySQLdb as mdb  # 数据库连接器

import metautils
import downloadTorrent
from bencode import bencode, bdecode
import pygeoip

DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASS = 'root'

BOOTSTRAP_NODES = (
    ("67.215.246.10", 6881),
    ("82.221.103.244", 6881),
    ("23.21.224.150", 6881)
)
RATE = 1  # 调控速率
TID_LENGTH = 2
RE_JOIN_DHT_INTERVAL = 3
TOKEN_LENGTH = 2
INFO_HASH_LEN = 500000  # 50w数据很小，限制内存不至于消耗太大
CACHE_LEN = 100  # 更新数据库缓存
WAIT_DOWNLOAD = 80


geoip = pygeoip.GeoIP('GeoIP.dat')


def is_ip_allowed(ip):
    country = geoip.country_code_by_addr(ip)
    if country in ('CN', 'TW', 'JP', 'HK', 'KR'):
        return True
    return False


def entropy(length):
    return "".join(chr(randint(0, 255)) for _ in xrange(length))


def random_id():
    h = sha1()
    h.update(entropy(20))
    return h.digest()


def decode_nodes(nodes):
    n = []
    length = len(nodes)
    if (length % 26) != 0:
        return n

    for i in range(0, length, 26):
        nid = nodes[i:i + 20]
        ip = inet_ntoa(nodes[i + 20:i + 24])
        port = unpack("!H", nodes[i + 24:i + 26])[0]
        n.append((nid, ip, port))

    return n


def timer(t, f):
    Timer(t, f).start()


def get_neighbor(target, nid, end=10):
    return target[:end] + nid[end:]


class KNode(object):

    def __init__(self, nid, ip, port):
        self.nid = nid
        self.ip = ip
        self.port = port


class DHTClient(Thread):

    def __init__(self, max_node_qsize):
        Thread.__init__(self)
        self.setDaemon(True)
        self.max_node_qsize = max_node_qsize
        self.nid = random_id()
        self.nodes = deque(maxlen=max_node_qsize)

    def send_krpc(self, msg, address):
        try:
            self.ufd.sendto(bencode(msg), address)
        except Exception:
            pass

    def send_find_node(self, address, nid=None):
        nid = get_neighbor(nid, self.nid) if nid else self.nid
        tid = entropy(TID_LENGTH)
        msg = {
            "t": tid,
            "y": "q",
            "q": "find_node",
            "a": {
                "id": nid,
                "target": random_id()
            }
        }
        self.send_krpc(msg, address)

    def join_DHT(self):
        for address in BOOTSTRAP_NODES:
            self.send_find_node(address)

    def re_join_DHT(self):
        if len(self.nodes) == 0:
            self.join_DHT()
        timer(RE_JOIN_DHT_INTERVAL, self.re_join_DHT)

    def auto_send_find_node(self):
        wait = 1.0 / self.max_node_qsize
        while True:
            try:
                node = self.nodes.popleft()
                self.send_find_node((node.ip, node.port), node.nid)
            except IndexError:
                pass
            try:
                sleep(wait)
            except KeyboardInterrupt:
                os._exit(0)

    def process_find_node_response(self, msg, address):
        nodes = decode_nodes(msg["r"]["nodes"])
        for node in nodes:
            (nid, ip, port) = node
            if len(nid) != 20:
                continue
            if ip == self.bind_ip:
                continue
            n = KNode(nid, ip, port)
            self.nodes.append(n)


class DHTServer(DHTClient):  # 获得info_hash

    def __init__(self, master, bind_ip, bind_port, max_node_qsize):
        DHTClient.__init__(self, max_node_qsize)

        self.master = master
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.speed = 0

        self.process_request_actions = {
            "get_peers": self.on_get_peers_request,
            "announce_peer": self.on_announce_peer_request,
        }

        self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.ufd.bind((self.bind_ip, self.bind_port))

        timer(RE_JOIN_DHT_INTERVAL, self.re_join_DHT)

    def run(self):
        self.re_join_DHT()
        while True:
            try:
                (data, address) = self.ufd.recvfrom(65536)
                msg = bdecode(data)
                self.on_message(msg, address)
            except Exception:
                pass

    def on_message(self, msg, address):
        global RATE  # 设为全局量
        try:
            if msg["y"] == "r":
                if "nodes" in msg["r"]:
                    self.process_find_node_response(msg, address)  # 发现节点
            elif msg["y"] == "q":
                try:
                    self.speed += 1
                    if self.speed % 10000 == 0:
                        RATE = random.randint(1, 3)
                        if RATE == 2:
                            RATE = 1
                        if RATE == 3:
                            RATE = 10
                        if self.speed > 100000:
                            self.speed = 0
                    if self.speed % RATE == 0:  # 数据过多，占用cpu太多，划分限速,1,1,10
                        self.process_request_actions[msg["q"]](msg, address)  # 处理其他节点的请求，这个过程获取info_hash
                    #self.process_request_actions[msg["q"]](msg, address) #处理其他节点的请求，这个过程获取info_hash
                except KeyError:
                    self.play_dead(msg, address)
        except KeyError:
            pass

    def on_get_peers_request(self, msg, address):
        try:
            infohash = msg["a"]["info_hash"]
            tid = msg["t"]
            nid = msg["a"]["id"]
            token = infohash[:TOKEN_LENGTH]
            msg = {
                "t": tid,
                "y": "r",
                "r": {
                    "id": get_neighbor(infohash, self.nid),
                    "nodes": "",
                    "token": token
                }
            }
            self.master.log(infohash, address)
            self.send_krpc(msg, address)
        except KeyError:
            pass

    def on_announce_peer_request(self, msg, address):
        try:
            infohash = msg["a"]["info_hash"]
            token = msg["a"]["token"]
            nid = msg["a"]["id"]
            tid = msg["t"]

            if infohash[:TOKEN_LENGTH] == token:
                if msg["a"].get("implied_port", 0) != 0:
                    port = address[1]
                else:
                    port = msg["a"]["port"]
                self.master.log_announce(infohash, (address[0], port))
        except Exception:
            pass
        finally:
            self.ok(msg, address)

    def play_dead(self, msg, address):
        try:
            tid = msg["t"]
            msg = {
                "t": tid,
                "y": "e",
                "e": [202, "Server Error"]
            }
            self.send_krpc(msg, address)
        except KeyError:
            pass

    def ok(self, msg, address):
        try:
            tid = msg["t"]
            nid = msg["a"]["id"]
            msg = {
                "t": tid,
                "y": "r",
                "r": {
                    "id": get_neighbor(nid, self.nid)
                }
            }
            self.send_krpc(msg, address)
        except KeyError:
            pass


class Master(Thread):  # 解析info_hash

    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.queue = Queue()
        self.cache = Queue()
        self.count = 0
        self.mutex = threading.RLock()  # 可重入锁，使单线程可以再次获得已经获得的?
        self.waitDownload = Queue()
        self.metadata_queue = Queue()
        self.dbconn = mdb.connect(DB_HOST, DB_USER, DB_PASS, 'oksousou', charset='utf8')
        self.dbconn.autocommit(False)
        self.dbcurr = self.dbconn.cursor()
        self.dbcurr.execute('SET NAMES utf8')
        self.visited = set()

    def lock(self):  # 加锁
        self.mutex.acquire()

    def unlock(self):  # 解锁
        self.mutex.release()

    def work(self, item):
        while True:
            self.prepare_download_metadata()
            self.lock()
            self.download_metadata()
            self.unlock()

            self.lock()
            self.got_torrent()
            self.unlock()

    def start_work(self, max):

        for item in xrange(max):
            t = threading.Thread(target=self.work, args=(item,))
            t.setDaemon(True)
            t.start()

    #入队的种子效率更高
    def log_announce(self, binhash, address=None):
        if self.queue.qsize() < INFO_HASH_LEN:  # 大于INFO_HASH_LEN就不要入队，否则后面来不及处理
            if is_ip_allowed(address[0]):
                self.queue.put([address, binhash])  # 获得info_hash

    def log(self, infohash, address=None):
        if self.queue.qsize() < INFO_HASH_LEN:  # 大于INFO_HASH_LEN/2就不要入队，否则后面来不及处理
            if is_ip_allowed(address[0]):
                self.queue.put([address, infohash])

    def prepare_download_metadata(self):

        if self.queue.qsize() == 0:
            sleep(2)
        #从queue中获得info_hash用来下载
        address, binhash = self.queue.get()
        if binhash in self.visited:
            return
        if len(self.visited) > 100000:  # 大于100000重置队列,认为已经访问过了
            self.visited = set()
        self.visited.add(binhash)
        #跟新已经访问过的info_hash
        info_hash = binhash.encode('hex')
        utcnow = datetime.datetime.utcnow()

        self.cache.put((address, binhash, utcnow))  # 装入缓存队列

    def download_metadata(self):

        if self.cache.qsize() > CACHE_LEN / 2:  # 出队更新下载
            while self.cache.qsize() > 0:  # 排空队列
                address, binhash, utcnow = self.cache.get()
                info_hash = binhash.encode('hex')
                self.dbcurr.execute('SELECT id FROM search_hash WHERE info_hash=%s', (info_hash,))
                y = self.dbcurr.fetchone()
                if y:
                    # 更新最近发现时间，请求数
                    self.dbcurr.execute('UPDATE search_hash SET last_seen=%s, requests=requests+1 WHERE info_hash=%s', (utcnow, info_hash))
                else:
                    self.waitDownload.put((address, binhash))
            self.dbconn.commit()
            if self.waitDownload.qsize() > WAIT_DOWNLOAD:
                while self.waitDownload.qsize() > 0:
                    address, binhash = self.waitDownload.get()
                    t = threading.Thread(target=downloadTorrent.download_metadata, args=(address, binhash, self.metadata_queue))
                    t.setDaemon(True)
                    t.start()

    def decode(self, s):
        if type(s) is list:
            s = ';'.join(s)
        u = s
        for x in (self.encoding, 'utf8', 'gbk', 'big5'):
            try:
                u = s.decode(x)
                return u
            except:
                pass
        return s.decode(self.encoding, 'ignore')

    def decode_utf8(self, d, i):
        if i+'.utf-8' in d:
            return d[i+'.utf-8'].decode('utf8')
        return self.decode(d[i])

    def parse_metadata(self, data): #解析种子
        info = {}
        self.encoding = 'utf8'
        try:
            torrent = bdecode(data) #编码后解析
            if not torrent.get('name'):
                return None
        except:
            return None
        detail = torrent
        info['name'] = self.decode_utf8(detail, 'name')
        if 'files' in detail:
            info['files'] = []
            for x in detail['files']:
                if 'path.utf-8' in x:
                    v = {'path': self.decode('/'.join(x['path.utf-8'])), 'length': x['length']}
                else:
                    v = {'path': self.decode('/'.join(x['path'])), 'length': x['length']}
                if 'filehash' in x:
                    v['filehash'] = x['filehash'].encode('hex')
                info['files'].append(v)
            info['length'] = sum([x['length'] for x in info['files']])
        else:
            info['length'] = detail['length']
        info['data_hash'] = hashlib.md5(detail['pieces']).hexdigest()
        return info

    def got_torrent(self):
        if self.metadata_queue.qsize() == 0:
            return
        binhash, address, data,start_time = self.metadata_queue.get()
        if not data:
            return
        try:
            info = self.parse_metadata(data)
            if not info:
                return
        except:
            traceback.print_exc()
            return

        temp = time.time()
        x = time.localtime(float(temp))
        utcnow = time.strftime("%Y-%m-%d %H:%M:%S",x) # get time now

        info_hash = binhash.encode('hex') #磁力
        info['info_hash'] = info_hash
        # need to build tags
        info['tagged'] = False
        info['classified'] = False
        info['requests'] = 1
        info['last_seen'] = utcnow
        info['create_time'] = utcnow
        info['source_ip'] = address[0]

        if info.get('files'):
            files = [z for z in info['files'] if not z['path'].startswith('_')]
            if not files:
                files = info['files']
        else:
            files = [{'path': info['name'], 'length': info['length']}]
        files.sort(key=lambda z:z['length'], reverse=True)
        bigfname = files[0]['path']
        info['extension'] = metautils.get_extension(bigfname).lower()
        info['category'] = metautils.get_category(info['extension'])

        try:
            try:
                print '\n', 'Saved', info['info_hash'], info['name'], (time.time()-start_time), 's', address[0]
            except:
                print '\n', 'Saved', info['info_hash']
            ret = self.dbcurr.execute('INSERT INTO search_hash(info_hash,category,data_hash,name,extension,classified,source_ip,tagged,' +
                'length,create_time,last_seen,requests) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (info['info_hash'], info['category'], info['data_hash'], info['name'], info['extension'], info['classified'],
                info['source_ip'], info['tagged'], info['length'], info['create_time'], info['last_seen'], info['requests']))
            if self.count % 50 == 0 :
                self.dbconn.commit()
                if self.count > 100000:
                    self.count = 0
        except:
            print self.name, 'save error', self.name, info
            traceback.print_exc()
            return

if __name__ == "__main__":

    #启动客户端
    master = Master()
    master.start_work(150)

    #启动服务器
    dht = DHTServer(master, "0.0.0.0", 6881, max_node_qsize=200)
    dht.start()
    dht.auto_send_find_node()
