#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

__VERSION__ = "1.0.0"
if __name__ == "__main__":
    print(__VERSION__)
    import os
    os._exit(0)

import os
import os.path
import logging

from gunicorn._compat import execfile_ as execpyfile

LOG = logging.getLogger("gunicorn.error")


def get_config_file(filename="app_config.py", dir=None):
    _dir = dir if dir else os.path.dirname(dir)
    path = os.path.join(_dir, filename)
    if os.path.exists(path):
        return path
    if not _dir or _dir == "/":
        raise OSError("Cannot find the config file '%s'" % filename)
    return get_config_file(filename=filename, dir=os.path.dirname(_dir))


def load_app_config(name="APP_CONFIG"):
    config_file = os.environ.get(name, None) or get_config_file(name.lower() + ".py")
    if not os.path.exists(config_file):
        raise RuntimeError("'%r' doest't exist" % config_file)
    cfg = {"__builtins__": __builtins__, "__file__": config_file}
    execpyfile(config_file, cfg, cfg)
    return cfg
