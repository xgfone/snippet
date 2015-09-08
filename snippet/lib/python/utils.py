#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
import sys
import traceback

# On Python(>=2.7), sys.version_info[0] <==> sys.version_info.major
if sys.version_info[0] == 2:
    PY3 = False
else:
    PY3 = True

if PY3:
    import builtins
else:
    import __builtin__ as builtins

_CACHE_BUILTIN = {}

### Attribute Wrapper
class AttrWrapper(object):
    attrs = []

    def __setattr__(self, name, value):
        if name not in self.attrs:
            raise AttributeError("'%s' is not supported" % name)
        object.__setattr__(self, name, value)

    def __repr__(self):
        attrs = []
        template = "%s=%s"
        for name in self.attrs:
            try:
                attrs.append(template % (name, getattr(self, name)))
            except AttributeError:
                pass

        return "%s(%s)" % (self.__class__.__name__, ", ".join(attrs))


def _map2(func, *iterable):
    """This function is equal to the built-in function, map, in Python2.
    But it returns a iterator, not a list.
    """
    def inner():
        args = []
        num = 0
        for iter in iterable:
            data = next(iter, None)
            if data is None:
                num += 1
            args.append(data)
        return num, args

    iterable = [iter(it) for it in iterable]
    total = len(iterable)
    while True:
        num, args = inner()
        if num == total:
            raise StopIteration
        else:
            yield func(args)


def _map3(func, *iterable):
    """This function is equal to the built-in function, map, in Python3.
    """
    iterable = [iter(it) for it in iterable]
    while True:
        result = []
        for it in iterable:
            result.append(next(it))
        yield func(result)

if PY3:
    map2 = _map2
    map3 = map
else:
    #map2 = map
    map2 = _map2
    map3 = _map3


def set_builtin(name, value, force=False):
    if getattr(builtins, name) and not force:
        raise AttributeError("{0} has already existed".format(name))

    setattr(builtins, name, value)
    global _CACHE_BUILTIN
    _CACHE_BUILTIN[name] = value


def set_builtins(args, force=False):
    if args is None:
        return

    if isinstance(args, dict):
        args = args.items()

    for n, v in args:
        set_builtin(n, v, force)


def builtin_(f=lambda v: v, force=False):
    set_builtin("_", f, force)
    set_builtin("t", f, force)


def builtin_traceback(force=False):
    set_builtin("traceback", traceback.format_exc, force)


def builtin_all(others=None, force=False):
    builtin_(force=force)
    builtin_traceback(force=force)
    if others:
        set_builtins(others, force=force)


def remove_builtins(args):
    if args is None:
        return

    if not isinstance(args, (list, tuple)):
        args = [args]

    for arg in args:
        if arg not in _CACHE_BUILTIN:
            raise AttributeError("{0} doesn't exist".format(arg))
        delattr(builtins, arg)
        _CACHE_BUILTIN.pop(arg)
