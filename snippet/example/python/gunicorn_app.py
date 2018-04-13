#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from multiprocessing import cpu_count
from gunicorn.util import import_app
from gunicorn.config import Setting, validate_string, validate_bool
from gunicorn.app.base import Application as _Application


def add_app_version(version, name=None, help=None):
    class AppVersion(Setting):
        validator = validate_bool
        desc = "Print app's version and exit."

        def add_option(self, parser):
            parser.add_argument(name or "--app-version", action="version",
                                version=version + "\n", help=help or self.desc)

    return AppVersion


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
        "bind": "0.0.0.0:8888",
        "workers": cpu_count() * 2,
        "worker_class": "gevent",
        "worker_connections": 10000,
    }

    def __init__(self, app=None, app_name=None, app_conf=None, load_app=None,
                 config_options=None, usage=None, prog=None):

        self._app = app
        self._app_name = app_name
        self._load_app = load_app
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

        if not self._app and not self._load_app:
            raise RuntimeError("no app")

        if not self._app_name and self._app:
            self._app_name = self._app if isinstance(self._app, str) else \
                             self._app.__class__.__name__

        if self._app_name:
            self.cfg.set("default_proc_name", self._app_name)

        return self._config_options

    def load(self):
        if self._app:
            app = self._app
            if isinstance(app, str):
                app = import_app(self._app)
        else:
            app = self._load_app()

        if hasattr(app, "load_conf"):
            app.load_conf(self._app_conf)

        return app


def main():
    AppManager().run()


if __name__ == "__main__":
    main()
