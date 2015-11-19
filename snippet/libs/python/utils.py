#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
import sys
import traceback
import subprocess

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


if getattr(subprocess, "check_output", None):
    check_output = subprocess.check_output
else:
    def check_output(*popenargs, **kwargs):
        r"""Run command with arguments and return its output as a byte string.

        If the exit code was non-zero it raises a CalledProcessError.  The
        CalledProcessError object will have the return code in the returncode
        attribute and output in the output attribute.

        The arguments are the same as for the Popen constructor.  Example:

        >>> check_output(["ls", "-l", "/dev/null"])
        'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'

        The stdout argument is not allowed as it is used internally.
        To capture standard error in the result, use stderr=STDOUT.

        >>> check_output(["/bin/sh", "-c",
        ...               "ls -l non_existent_file ; exit 0"],
        ...              stderr=STDOUT)
        'ls: non_existent_file: No such file or directory\n'
        """
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd, output=output)
        return output

    subprocess.check_output = check_output
