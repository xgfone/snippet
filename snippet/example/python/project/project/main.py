#!/usr/bin/python
# encoding: utf8
from __future__ import absolute_import, print_function, unicode_literals

import eventlet

from oslo_config import cfg
from oslo_log import log

# from {PROJECT}.db import api

CONF = cfg.CONF
__VERSION__ = "0.1"


def main(project="example"):
    log.register_options(CONF)
    # log.set_defaults(default_log_levels=None)
    CONF(project=project, version=__VERSION__)
    log.setup(CONF, project, __VERSION__)

    eventlet.monkey_patch(all=True)

    # (TODO)
    pass


if __name__ == '__main__':
    main()
