#!/usr/bin/python
# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals, division

try:
    import gevent.monkey
    gevent.monkey.patch_all(httplib=True, sys=True, Event=True)
except ImportError:
    pass

import logging

from oslo_config.cfg import CONF
from {PROJECT}._option import global_opts
from {PROJECT}.common.logging import init_logging
from {PROJECT}.common import utils

LOG = logging.getLogger(__name__)
CONF.register_cli_opts(global_opts)


def main(project="example", version=None):
    CONF(project=project, version=get_version(project, version))

    init_logging(logging.getLogger(project), level=CONF.log_level,
                 log_file=CONF.log_file)

    # TODO


if __name__ == '__main__':
    main()
