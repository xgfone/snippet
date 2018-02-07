#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals, print_function, division

import sys

if sys.version_info[0] < 3:
    PY3, Unicode, Bytes = False, unicode, str
else:
    PY3, Unicode, Bytes = True, str, bytes

to_bytes = lambda v, e="utf-8": v.encode(e) if isinstance(v, Unicode) else v
to_unicode = lambda v, e="utf-8": v.decode(e) if isinstance(v, Bytes) else v
to_str = to_unicode if PY3 else to_bytes


class ObjectDict(dict):
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" % (
                                 self.__class__.__name__, name))
