# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals, division

from oslo_config import cfg

CONF = cfg.CONF

global_opts = [
    cfg.StrOpt("log_file", default="", help="The path of the log file."),
    cfg.StrOpt("log_level", default="DEBUG", help="The log level, such as DEBUG, INFO, etc."),
]
