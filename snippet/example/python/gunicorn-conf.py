# -*- encoding: utf-8 -*-
# Notice: This config file is a Python module file.

import multiprocessing

appname = "sgapi"

# [Gunicorn Setting]
daemon = True
bind = "0.0.0.0:10100"
errorlog = "/log/sgapi/{}.log".format(appname)
pidfile = "/log/sgapi/{}.pid".format(appname)
proc_name = appname
worker_class = "gevent"
worker_connections = 10000
workers = multiprocessing.cpu_count() * 2
raw_env = "APP_CONFIG={}".format(__file__)

# [App Setting]
