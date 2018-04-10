# -*- encoding: utf8 -*-

from __future__ import absolute_import, print_function, unicode_literals, division

try:
    import eventlet
except ImportError:
    eventlet = None

from .pool import ResourcePool
from kazoo import exceptions as zkexc
from kazoo.client import KazooClient


def _get_zk_handler():
    if eventlet:
        from kazoo.handlers.eventlet import SequentialEventletHandler as h
    else:
        from kazoo.handlers.threading import SequentialThreadingHandler as h
    return h()


class ZooKeeper(object):
    def __init__(self, hosts="127.0.0.1:2181", prefix="/"):
        prefix = prefix.rstrip("/")
        if prefix and not prefix.startswith("/"):
            raise ValueError("prefix must start with /")
        self._prefix = prefix
        self._zk = KazooClient(hosts=hosts, handler=_get_zk_handler())
        self._zk.start()

    def __del__(self):
        self.close()

    def _path(self, path):
        if self._prefix:
            return "{0}/{1}".format(self._prefix, path)
        return path

    def close(self):
        if not self._zk:
            return

        try:
            self._zk.stop()
            self._zk.close()
        except Exception:
            pass
        finally:
            self._zk = None

    def create(self, path, value="", makepath=True):
        self._zk.create(self._path(path), value, makepath=makepath)

    def delete(self, path, recursive=True):
        self._zk.delete(self._path(path), recursive=recursive)

    def set(self, path, value, makepath=True):
        path = self._path(path)
        try:
            self._zk.set(path, value)
        except zkexc.NoNodeError:
            if not makepath:
                raise
            self._zk.create(path, value, makepath=True)

    def get(self, path, none=True):
        try:
            return self._zk.get(self._path(path))
        except zkexc.NoNodeError:
            if none:
                return None
            raise

    def ls(self, path, none=True):
        try:
            return self._zk.get_children(self._path(path))
        except zkexc.NoNodeError:
            if none:
                return None
            raise


class ZkPoolProxy(object):
    def __init__(self, hosts, prefix="/", pool_size=10):
        self.__pool = ResourcePool(ZooKeeper, hosts=hosts, prefix=prefix,
                                   capacity=pool_size, autowrap=True)

    def _call(self, zk, method, *args, **kwargs):
        try:
            v = getattr(zk, method)(*args, **kwargs)
        except Exception:
            self.__pool.put_with_close(zk)
            raise
        else:
            self.__pool.put(zk)
            return v

    def close(self):
        self.__pool.close()

    def create(self, path, value="", makepath=True):
        self.__pool.get().create(path, value=value, makepath=makepath)

    def delete(self, path, recursive=True):
        self.__pool.get().delete(path, recursive=recursive)

    def set(self, path, value, makepath=True):
        self.__pool.get().set(path, value, makepath=makepath)

    def get(self, path, none=True):
        return self.__pool.get().get(path, none=none)

    def ls(self, path, none=True):
        return self.__pool.get().ls(path, none=none)
