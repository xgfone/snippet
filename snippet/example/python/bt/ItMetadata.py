#coding: utf8
import threading
import traceback
import random
import time
import os
import socket

import libtorrent as lt

threading.stack_size(200 * 1024)
socket.setdefaulttimeout(30)


def fetch_torrent(session, ih, timeout):
    name = ih.upper()
    url = 'magnet:?xt=urn:btih:%s' % (name,)
    params = {
        'save_path': '/tmp/downloads/',
        'storage_mode': lt.storage_mode_t(2),
        'paused': False,
        'auto_managed': False,
        'duplicate_is_error': True}
    try:
        handle = lt.add_magnet_uri(session, url, params)
    except Exception:
        return None
    handle.set_sequential_download(1)
    meta = None
    down_path = None
    for i in range(0, timeout):
        if handle.has_metadata():
            info = handle.get_torrent_info()
            down_path = '/tmp/downloads/%s' % info.name()
            meta = info.metadata()
            break
        time.sleep(1)
    if down_path and os.path.exists(down_path):
        os.system('rm -rf "%s"' % down_path)
    session.remove_torrent(handle)
    return meta


def download_metadata(address, binhash, metadata_queue, timeout=40):
    metadata = None
    start_time = time.time()
    try:
        session = lt.session()
        r = random.randrange(10000, 50000)
        session.listen_on(r, r + 10)
        session.add_dht_router('router.bittorrent.com', 6881)
        session.add_dht_router('router.utorrent.com', 6881)
        session.add_dht_router('dht.transmission.com', 6881)
        session.add_dht_router('127.0.0.1', 6881)
        session.start_dht()
        metadata = fetch_torrent(session, binhash.encode('hex'), timeout)
        session = None
    except Exception:
        traceback.print_exc()
    finally:
        metadata_queue.put((binhash, address, metadata, 'lt', start_time))
