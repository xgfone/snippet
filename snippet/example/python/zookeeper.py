#!/usr/bin/env python
# encoding: utf8
from __future__ import absolute_import, print_function, unicode_literals, division

import zookeeper


def refactor_path(f):
    def wrapper(*args, **kwargs):
        _refactor = kwargs.pop("refactor", True)
        if _refactor:
            path = kwargs.get("path", None)
            if path is not None:
                kwargs["path"] = args[0]._path(path)  # args[0] is an instance of ZooKeeper
        return f(*args, **kwargs)

    return wrapper


class ZooKeeper(object):
    DEFAULT_ACL = [{"perms": 0x1f, "scheme": "world", "id": "anyone"}]

    def __init__(self, connector, root="/", acl=None, flags=0):
        self.root = root.rstrip("/")
        if not self.root:
            self.root = "/"
        self.zk = zookeeper.init(connector)
        self.acl = acl if acl else self.DEFAULT_ACL
        self.flags = flags

    def _path(self, path):
        path = path.strip("/")
        if path:
            path = "/".join((self.root, path))
        else:
            path = self.root
        return path

    @refactor_path
    def create(self, path="", value=""):
        try:
            zookeeper.create(self.zk, path, value, self.acl, self.flags)
        except zookeeper.NodeExistsException:
            pass
        except zookeeper.NoNodeException:
            self.create(path=path.rsplit("/", 1)[0], refactor=False)
            self.create(path=path, value=value, refactor=False)

    @refactor_path
    def delete(self, path="", recursion=True):
        try:
            zookeeper.delete(self.zk, path)
        except zookeeper.NoNodeException:
            pass
        except zookeeper.NotEmptyException:
            if recursion:
                for subpath in self.ls(path=path, refactor=False):
                    self.delete(path="/".join((path, subpath)), recursion=recursion, refactor=False)
                self.delete(path=path, recursion=recursion, refactor=False)
            else:
                raise

    @refactor_path
    def set(self, path="", value=""):
        try:
            zookeeper.set(self.zk, path, value)
        except zookeeper.NoNodeException:
            self.create(path=path, value=value, refactor=False)
            self.set(path=path, value=value, refactor=False)

    @refactor_path
    def get(self, path=""):
        return zookeeper.get(self.zk, path)

    @refactor_path
    def ls(self, path=""):
        return zookeeper.get_children(self.zk, path)

    def close(self):
        zookeeper.close(self.zk)
