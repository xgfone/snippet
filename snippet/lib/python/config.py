# coding: utf-8

from oslo_config import cfg
from oslo_log import log

CONF = cfg.CONF

_ROOTS = ["root"]
_DEFAULT_LOG_LEVELS = ['root=INFO']
_DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def parse_args(argv, project, version=None, default_config_files=None,
               default_log_format=None, default_log_levels=None):
    if project not in _ROOTS:
        _DEFAULT_LOG_LEVELS.append('%s=INFO' % project)
        _ROOTS.append(project)
    log_fmt = default_log_format if default_log_format else _DEFAULT_LOG_FORMAT
    log_lvl = default_log_levels if default_log_levels else _DEFAULT_LOG_LEVELS

    log.set_defaults(log_fmt, log_lvl)
    log.register_options(CONF)

    # (TODO): Configure the options of the other libraries, which must be called
    # before parsing the configuration file.

    CONF(argv[1:], project=project, version=version,
         default_config_files=default_config_files)
