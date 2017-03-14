# encoding: utf8

from __future__ import absolute_import, print_function, division, print_function
import logging

LOG = logging.getLogger()


def init_logging(logger=None, level="DEBUG", log_file="", file_config=None, dict_config=None):
    try:
        logging
    except Exception:
        import logging

    # Initialize the argument logger with the arguments, level and log_file.
    if logger:
        fmt = "%(asctime)s - %(pathname)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

        level = getattr(logging, level.upper())
        logger.setLevel(level)

        if log_file:
            from logging.handlers import TimedRotatingFileHandler
            handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=30)
        else:
            handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    # Initialize logging by the configuration file, file_config.
    if file_config:
        logging.config.fileConfig(file_config, disable_existing_loggers=False)

    # Initialize logging by the dict configuration, dict_config.
    if dict_config and hasattr(logging.config, "dictConfig"):
        logging.config.dictConfig(dict_config)


if __name__ == '__main__':
    init_logging(LOG, logging.INFO, log_file="/tmp/test.log")
    LOG.info("test log")
