#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals, print_function, division

import sys
import os.path

if sys.version_info[0] < 3:
    PY3, Unicode, Bytes = False, unicode, str
else:
    PY3, Unicode, Bytes = True, str, bytes


def to_bytes(v, encoding="utf-8", **kwargs):
    if isinstance(v, Bytes):
        return v
    elif isinstance(v, Unicode):
        return v.encode(encoding)
    return to_bytes(str(v), encoding=encoding)


def to_unicode(v, encoding="utf-8", **kwargs):
    if isinstance(v, Bytes):
        return v.decode(encoding)
    elif isinstance(v, Unicode):
        return v
    return to_unicode(str(v), encoding=encoding)

to_str = to_unicode if PY3 else to_bytes
is_bytes = lambda s: isinstance(s, Bytes)
is_unicode = lambda s: isinstance(s, Unicode)
is_string = lambda s: isinstance(s, (Bytes, Unicode))


class ObjectDict(dict):
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            m = "'%s' object has no attribute '%s'" % (self.__class__.__name__, name)
            raise AttributeError(m)


# Execute and return a python module for Python3.
def execpyfile(filename, *args):
    if not os.path.exists(filename):
        raise RuntimeError("'{}' does not exist".format(filename))
    if args:
        globals = args[0]
        if "__file__" not in globals:
            globals["__file__"] = filename
        if "__builtins__" not in globals:
            globals["__builtins__"] = __builtins__
        if "__name__" not in globals:
            globals["__name__"] = "__exec__"
    else:
        args = ({
            "__file__": filename,
            "__builtins__": __builtins__,
            "__name__": "__exec__",
        },)
    code = compile(open(filename, 'rb').read(), filename, 'exec')
    return exec(code, *args)


###############################################################################
from socket import inet_aton, inet_ntoa
from struct import pack as struct_pack, unpack as struct_unpack

_ALL_IP_MASK = 2 ** 32 - 1
_IP_MASK_CACHES = {}
for i in range(0, 33):
    _IP_MASK_CACHES[i] = (_ALL_IP_MASK >> i) ^ _ALL_IP_MASK


def normalize_ip_subnet(ip, fmt=to_str("!I")):
    ip, mask = ip.split("/")
    ip = struct_unpack(fmt, inet_aton(ip))[0] & _IP_MASK_CACHES[int(mask)]
    return "{}/{}".format(inet_ntoa(struct_pack(fmt, ip)), mask)


###############################################################################
def readn(reader, size=-1):
    if size < 0:
        return to_unicode(reader.read())

    tmp = []
    while size > 0:
        data = reader.read(size)
        tmp.append(data)
        size -= len(data)
    return to_unicode(b"".join(tmp))


import requests


def send_http_json(method, url, exc=True, headers=None, **kwargs):
    """Send the HTTP request.

    See: http://www.python-requests.org/en/master/api/#requests.Session.request
    """

    if headers:
        headers["Accept"] = "application/json"
    else:
        headers = {"Accept": "application/json"}

    resp = getattr(requests, method)(url, headers=headers, **kwargs)
    if exc:
        resp.raise_for_status()

    data = resp.content
    if resp.status_code == 200:
        if resp.content:
            data = resp.json()
    return resp.status_code, data
