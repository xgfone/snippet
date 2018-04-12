#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys

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


class AppManager(_Application):
    _DEFAULT_OPTIONS = {
        "bind": "0.0.0.0:8000",
        "workers": cpu_count() * 2,
        "worker_class": "gevent",
        "worker_connections": 10000,
    }

    def __init__(self, app=None, app_name=None, app_conf=None,
                 config_options=None, usage=None, prog=None):

        self._app = app
        self._app_name = app_name
        self._app_conf = app_conf or {}

        self._config_options = self._DEFAULT_OPTIONS.copy()
        self._config_options.update(config_options or {})

        super(AppManager, self).__init__(usage=usage, prog=prog)

    def load_app_config(self, filepath):
        """Consider the config file as a python module to load."""

        if filepath[0] == "/":
            cfg = self.get_config_from_filename(filepath)
        else:
            cfg = self.get_config_from_module_name(filepath)
        self._app_conf.update(cfg)

    def init(self, parser, opts, args):
        if opts.app_config:
            self.load_app_config(opts.app_conf)

        if args:
            self._app = args[0]
            if not self._app_name:
                self._app_name = args[0]

        if not self._app:
            raise RuntimeError("not app")

        if self._app_name:
            self.cfg.set("default_proc_name", self._app_name)

        return self._config_options

    def load(self):
        sys.path.insert(0, self.cfg.chdir)
        app = self._app
        if isinstance(app, str):
            app = import_app(self._app)
        app.conf = self._app_conf
        return app


def main():
    AppManager().run()


if __name__ == "__main__":
    main()
