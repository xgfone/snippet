#!/usr/bin/python
# encoding: utf8
from __future__ import absolute_import, print_function, unicode_literals

import eventlet

from oslo_config import cfg
from oslo_log import log

# from {PROJECT}.db import api

CONF = cfg.CONF
__VERSION__ = "0.1"

project_opts = [
    cfg.StrOpt("logging_config_file", default="",
               help="The configuration file of logging for the {PROJECT}"),
]
CONF.register_cli_options(project_opts, group="{PROJECT}")


def main(project="example"):
    log.register_options(CONF)
    # log.set_defaults(default_log_levels=None)
    CONF(project=project, version=__VERSION__)

    # (TODO) Daemon

    eventlet.monkey_patch(all=True)
    if CONF.{PROJECT}.logging_config_file:
        log._load_log_config(CONF.{PROJECT}.logging_config_file)
    else:
        log.setup(CONF, project, __VERSION__)

    # (TODO)
    pass


if __name__ == '__main__':
    main()
