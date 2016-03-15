# coding: utf-8
"""
Use the library 'oslo.log' to configure the logging.

Applications should use oslo.log’s configuration functions to register
logging-related configuration options and configure the root and other default
loggers.

(1) Call register_options() before parsing command line options.
(2) Call set_defaults() before configuring logging.
(3) Call setup() to configure logging for the application.

## Example

import sys
from oslo_log import log


def set_log(conf, project, args=None, version="unknown", default_log_levels=None,
            logging_config_file=None):
    # Register the command line and configuration options used by oslo.log.
    log.register_options(conf)

    # Set default values for the configuration options used by oslo.log.
    log.set_defaults(default_log_levels=default_log_levels)

    # Parse the command line options.
    args = args if args else sys.argv[1:]
    conf(args, project=project, version=version)

    # Setup logging for the current application.
    if logging_config_file:
        log._load_log_config(logging_config_file)
    else:
        log.setup(conf, project, version)

"""
