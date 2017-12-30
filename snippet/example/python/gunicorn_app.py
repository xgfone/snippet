#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys

from os.path import split as split_path
from multiprocessing import cpu_count
from gunicorn.util import import_app
from gunicorn.config import Setting, validate_string
from gunicorn.app.base import Application as _Application


class AppConfigFile(Setting):
    name = "app_config"
    section = "App Config File"
    cli = ["--app-config"]
    meta = "CONFIG"
    validator = validate_string
    default = None
    desc = """\
        The App config file.

        If it ends with ".py", it will be parsed as the python module,
        or as the INI configuration file.
        """


class Application(_Application):
    _DEFAULT_OPTIONS = {
        "bind": "0.0.0.0:80",
        "workers": cpu_count() * 2,
        "worker_class": "eventlet",
        "worker_connections": 10000,
    }

    def __init__(self, app=None, app_name=None, app_conf=None,
                 load_app_config=None, workers=None, options=None):

        self._app = app
        self._app_name = app_name
        self._app_conf = app_conf or {}

        self._load_app_config = self._load_app_config_default
        if load_app_config:
            self._load_app_config = load_app_config

        self._options = self._DEFAULT_OPTIONS.copy()
        self._options.update(options or {})
        if workers is not None:
            self._options["workers"] = workers

        super(Application, self).__init__()

    def _load_app_config_default(self, filepath):
        """Consider the config file as a python module to load."""

        if filepath[0] != "/":
            return self.get_config_from_module_name(filepath)

        filedir, filename = split_path(filepath)
        sys.path.append(filedir)
        conf = self.get_config_from_module_name(filename[:-3])
        sys.path.remove(filedir)
        return conf

    def init(self, parser, opts, args):
        if opts.app_config:
            self._app_conf.update(self._load_app_config(opts.app_conf))

        if args > 0:
            self._app = args[0]
            if not self._app_name:
                self._app_name = args[0]

        if not self._app:
            raise RuntimeError("not app")

        if self._app_name:
            self.cfg.set("default_proc_name", self._app_name)

        return self._options

    def load(self):
        sys.path.insert(0, self.cfg.chdir)
        app = import_app(self._app)
        app.conf = self._app_conf
        return app


def main():
    Application().run()

if __name__ == "__main__":
    main()
