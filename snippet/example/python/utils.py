#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals, print_function, division

import sys
import os.path

if sys.version_info[0] < 3:
    import builtins
    PY3, Unicode, Bytes = False, unicode, str
else:
    import __builtin__ as builtins
    PY3, Unicode, Bytes = True, str, bytes


# to_bytes = lambda v, e="utf-8": v.encode(e) if isinstance(v, Unicode) else v
# to_unicode = lambda v, e="utf-8": v.decode(e) if isinstance(v, Bytes) else v
# to_str = to_unicode if PY3 else to_bytes


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


def set_builtin(name, value, force=False):
    exist = getattr(builtins, name, None)
    if exist and force:
        return False
    setattr(builtins, name, value)
    return True


to_str = to_unicode if PY3 else to_bytes
set_builtin("str", to_unicode, force=True)


class ObjectDict(dict):
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" % (
                                 self.__class__.__name__, name))


# Execute and return a python module for Python3.
def execpyfile(filename, *args):
    if not os.path.exists(filename):
        raise RuntimeError("'{}' does not exist".format(filename))
    code = compile(open(filename, 'rb').read(), filename, 'exec')
    return exec(code, *args)
