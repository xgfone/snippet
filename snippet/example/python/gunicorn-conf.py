#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Notice: This config file is a Python module file.

import os
import multiprocessing
import gunicorn.glogging


# [Gunicorn Setting Section]
appname = "{APPNAME}"
bind = "0.0.0.0:8000"
pidfile = "/var/run/{appname}.pid".format(appname=appname)
logfile = "/log/{appname}/{appname}.log".format(appname=appname)

# Create the necessary directories.
os.makedirs("/log/{appname}".format(appname=appname), exist_ok=True)

# Configure Base
daemon = True
proc_name = appname
raw_env = "APP_CONFIG={0}".format(__file__)

# Configure Worker
worker_connections = 10000
workers = multiprocessing.cpu_count() * 2
try:
    import eventlet as _
    worker_class = "eventlet"
except ImportError:
    import gevent as _
    worker_class = "gevent"

# Configure Logging
filehandler = {
    "class": "logging.handlers.RotatingFileHandler",
    "formatter": "generic",
    "filename": logfile,
    "maxBytes": 1024 ** 3,  # 1GB
    "backupCount": 30,
}
logconfig_dict = gunicorn.glogging.CONFIG_DEFAULTS.copy()
logconfig_dict["handlers"]["console"] = filehandler
logconfig_dict["handlers"]["error_console"] = filehandler


# [App Setting]
