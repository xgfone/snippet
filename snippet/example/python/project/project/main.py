#!/usr/bin/python
# encoding: utf8
from __future__ import absolute_import, print_function, unicode_literals, division

import logging

from oslo_log import log
from oslo_config.cfg import CONF

from secure_log._options import global_opts
from secure_log.common.utils import get_version

LOG = logging.getLogger(__name__)
CONF.register_cli_opts(global_opts)


def main(project="example", version=None):
    if not version:
        version = get_version(project)

    # Pasre the configuration, including CLI and the configuration file.
    log.register_options(CONF)
    # log.set_defaults(default_log_levels=None)
    CONF(project=project, version=version)

    # Initilize the logging.
    log.setup(CONF, project, version)

    # TODO


if __name__ == '__main__':
    main()
