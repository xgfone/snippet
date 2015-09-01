# coding: utf-8
"""
Use the library 'oslo.log' to configure the logging.

Applications should use oslo.log’s configuration functions to register
logging-related configuration options and configure the root and other default
loggers.

(1) Call register_options() before parsing command line options.
(2) Call set_defaults() before configuring logging.
(3) Call setup() to configure logging for the application.
"""
import sys
from oslo_log.log import BaseLoggerAdapter, KeywordArgumentAdapter, LogConfigError
from oslo_log.log import getLogger, register_options, set_defaults, setup
from oslo_log.formatters import ContextFormatter, JSONFormatter
from oslo_log.handlers import NullHandler, ColorHandler, RFCSysLogHandler
try:
    from oslo_log.handlers import OSSysLogHandler
except ImportError:
    OSSysLogHandler = NullHandler


def set_log(conf, project, args=None, version="unknown", default_log_levels=None):
    """Initialize and set the logging.

    Parameter:
    @conf(ConfigOpt): the configuration option.
    @project(string): the name of this project.
    @version(string): the version of this project.
    @default_log_levels(Int): the default level of the logging.

    Notice:
    If using the fileConfig of the logging to configure the logging, you only
    use the option 'conf', and set the option 'log_config_append' with the path
    of the configuration file of the logging.
    """

    # Register the command line and configuration options used by oslo.log.
    register_options(conf)

    # Parse the command line options.
    args = args if args else sys.argv[1:]
    conf(args, project=project, version=version)

    # Set default values for the configuration options used by oslo.log.
    set_defaults(default_log_levels=default_log_levels)

    # Setup logging for the current application.
    setup(conf, project, version)
