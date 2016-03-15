# encoding: utf-8
import sys

from oslo_config import cfg

_ROOTS = ["root"]
_DEFAULT_LOG_LEVELS = ['root=INFO']
_DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s"


def parse_args_with_log(project, argv=None, version=None, conf=None, log=True,
                        default_config_files=None, default_log_format=None,
                        default_log_levels=None):

    conf = conf if conf else cfg.CONF
    argv = argv if argv else sys.argv[1:]

    if not log:
        conf(argv, project=project, version=version,
             default_config_files=default_config_files)
        return

    from oslo_log import log

    if project not in _ROOTS:
        _DEFAULT_LOG_LEVELS.append('%s=INFO' % project)
        _ROOTS.append(project)
    log_fmt = default_log_format if default_log_format else _DEFAULT_LOG_FORMAT
    log_lvl = default_log_levels if default_log_levels else _DEFAULT_LOG_LEVELS

    log.set_defaults(log_fmt, log_lvl)
    log.register_options(conf)

    # (TODO): Configure the options of the other libraries, which must be called
    # before parsing the configuration file.

    conf(argv, project=project, version=version,
         default_config_files=default_config_files)

    log.setup(conf, project, version)
