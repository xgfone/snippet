#!/usr/bin/env python
# encoding: utf8

"""Reset the resolution of a certain display.

REFERENCE: http://blog.csdn.net/smilematch/article/details/50482530
"""

from __future__ import absolute_import, unicode_literals, print_function, division

import sys
from subprocess import Popen, CalledProcessError, PIPE

SUDO = "sudo"


def check_output(*popenargs, **kwargs):
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    kwargs["shell"] = kwargs.get("shell", True)
    process = Popen(stdout=PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd, output=output)
    return output


def show_screen():
    cmd = "{sudo} xrandr".format(sudo=SUDO)
    out = check_output(cmd)
    print(out)


def get_mode(display, width, height):
    cmd = '{sudo} cvt {width} {height} | grep "^Modeline"'
    out = check_output(cmd.format(sudo=SUDO, width=width, height=height))
    items = out.split()
    name = items[1]
    mode = ' '.join(items[1:])
    return name, mode


def new_mode(display, width, height):
    name, mode = get_mode(display, width, height)
    try:
        cmd = '{sudo} xrandr --newmode {mode} 2>&1'.format(sudo=SUDO, mode=mode)
        check_output(cmd)
    except Exception:
        pass

    return name


def add_mode_to_display(display, mode_name):
    try:
        cmd = '{sudo} xrandr --addmode {display} {name} 2>&1'
        check_output(cmd.format(sudo=SUDO, display=display, name=mode_name))
    except Exception:
        pass


def enable_mode(display, mode_name):
    cmd = '{sudo} xrandr --output {display} --mode {name}'
    check_output(cmd.format(sudo=SUDO, display=display, name=mode_name))


def print_usage(app_name):
    print("Usage:")
    print("    {app} show".format(app=app_name))
    print("        Show the display information")
    print()
    print("    {app} set DISPLAY WIDTH HEIGHT".format(app=app_name))
    print("        Set the DISPLAY to WIDTH x HEIGHT")
    print()


def main():
    app = sys.argv[0]
    argv = sys.argv[1:]
    if argv[0] == "show":
        show_screen()
    elif argv[0] == "set":
        try:
            display, width, height = argv[1], int(argv[2]), int(argv[3])
        except Exception:
            print_usage(app)
        else:
            name = new_mode(display, width, height)
            add_mode_to_display(display, name)
            enable_mode(display, name)
    else:
        print_usage(app)


if __name__ == '__main__':
    main()
