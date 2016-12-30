# encoding: utf8

from __future__ import absolute_import, print_function
import logging

LOG = logging.getLogger()


def init_logging(logger, level, log_file=""):
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


if __main__ == "__name__":
    init_logging(LOG, logging.INFO, log_file="/tmp/test.log")
    LOG.info("test log")
