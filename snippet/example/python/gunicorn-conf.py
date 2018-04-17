# -*- encoding: utf-8 -*-
# Notice: This config file is a Python module file.

import multiprocessing

appname = "{APPNAME}"

# [Gunicorn Setting]
daemon = True
bind = "0.0.0.0:10100"
errorlog = "/log/{appname}/{appname}.log".format(appname=appname)
pidfile = "/log/{appname}/{appname}.pid".format(appname=appname)
proc_name = appname
worker_class = "gevent"
worker_connections = 10000
workers = multiprocessing.cpu_count() * 2
raw_env = "APP_CONFIG={0}".format(__file__)

# [App Setting]
