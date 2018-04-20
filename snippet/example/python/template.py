#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# Support Python 3+
#
# Install:
# $ pip3 install gevent requests sqlalchemy pymysql
#
# Run:
# $ python template.py -h
#

import gevent.pool
import gevent.monkey
gevent.monkey.patch_all(Event=True, sys=True)
taskpool = gevent.pool.Pool(size=1000)
spawn = taskpool.spawn

import sys
import logging

LOG = logging.getLogger()


def to_bytes(v, encoding="utf-8", errors="strict"):
    if isinstance(v, bytes):
        return v
    elif isinstance(v, str):
        return v.encode(encoding, errors)
    return to_bytes(str(v), encoding=encoding, errors=errors)


def to_str(v, encoding="utf-8", errors="strict"):
    if isinstance(v, bytes):
        return v.decode(encoding, errors)
    elif isinstance(v, str):
        return v
    return str(v)


def init_logging(logger=None, level="INFO", file=None, handler_cls=None,
                 max_num=30, propagate=True, file_config=None, dict_config=None):
    # Initialize the argument logger with the arguments, level and log_file.
    if logger:
        fmt = ("%(asctime)s - %(process)d - %(pathname)s - %(funcName)s - "
               "%(lineno)d - %(levelname)s - %(message)s")
        datefmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

        level = getattr(logging, level.upper())

        if file:
            if handler_cls:
                handler = handler_cls(file, max_num)
            else:
                from logging.handlers import TimedRotatingFileHandler
                handler = TimedRotatingFileHandler(file, when="midnight",
                                                   interval=1, backupCount=max_num)
        else:
            handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)

        loggers = logger if isinstance(logger, (list, tuple)) else [logger]
        for logger in loggers:
            logger.propagate = propagate
            logger.setLevel(level)
            logger.addHandler(handler)

    # Initialize logging by the configuration file, file_config.
    if file_config:
        logging.config.fileConfig(file_config, disable_existing_loggers=False)

    # Initialize logging by the dict configuration, dict_config.
    if dict_config and hasattr(logging.config, "dictConfig"):
        logging.config.dictConfig(dict_config)

##############################################################################
# Configuration
from argparse import ArgumentParser


class Configuration(object):
    class Group(object):
        def __init__(self, group_name):
            self.__name = group_name

        def __repr__(self):
            attrs = []
            for key, value in vars(self).items():
                if key != "_Group__name":
                    attrs.append("{0}={1}".format(key, value))
            return "{0}({1})".format(self.__class__.__name__, ", ".join(attrs))

        def __contains__(self, name):
            return hasattr(self, name)

        def __getattr__(self, name):
            e = "The group '{0}' has no the option '{1}'"
            raise AttributeError(e.format(self.__name, name))

        def __setitem__(self, name, value):
            setattr(self, name, value)

        def __getitem__(self, name):
            try:
                return getattr(self, name)
            except AttributeError:
                e = "The group '{0}' has no the option '{1}'"
                raise KeyError(e.format(self.__name, name))

        def items(self):
            d = vars(self)
            d.pop("_Group__name")
            return d.items()

    __slots__ = ["_default_group_name", "_default_group", "_allow_empty",
                 "_encoding", "_parsed", "_caches", "_opts", "_bool_true",
                 "_bool_false", "_description", "_version"]

    def __init__(self, description=None, allow_empty=False, encoding="utf-8",
                 default_group="DEFAULT", version=None):
        """A simple configuration file parser based on the format INI.

        When an configuration option does not exist, for getting one default
        value, not raising an exception, please use the method of get(), or the
        builtin function of getattr().
        """

        self._parsed = False
        self._description = description
        self._default_group_name = default_group
        self._default_group = Configuration.Group(self._default_group_name)
        self._allow_empty = allow_empty
        self._encoding = encoding
        self._version = version if version else "Unknown"

        self._caches = {self._default_group_name: self._default_group}
        self._opts = {}

        self._bool_true = ["t", "1", "on", "true"]
        self._bool_false = ["f", "0", "off", "false"]

    def __getattr__(self, name):
        if not self._parsed:
            raise Exception("Not parsed")

        try:
            return self._caches[name]
        except KeyError:
            pass

        msg = "'{0}' object has no attribute '{1}'"
        raise AttributeError(msg.format(self.__class__.__name__, name))

    def __getitem__(self, name):
        if not self._parsed:
            raise Exception("Not parsed")

        _name = self._uniformize(name)
        try:
            return self._caches[_name]
        except KeyError:
            pass

        msg = "'{0}' has no key '{1}'"
        raise KeyError(msg.format(self.__class__.__name__, name))

    def __repr__(self):
        attrs = ("%s=%s" % (k, v) for k, v in self._caches.items())
        return "{0}({1})".format(self.__class__.__name__, ", ".join(attrs))

    def _set_group_opt(self, group_name, opt_name, opt_value, force=False):
        gname = group_name if group_name else self._default_group_name
        group = self._caches[gname]
        if hasattr(group, opt_name) and not force:
            e = "The group '{0}' has had the option of '{1}'"
            raise ValueError(e.format(gname, opt_name))
        setattr(self._caches[gname], opt_name, opt_value)

    def _register(self, name, parser, default=None, group=None, help=None, short=None):
        if self._parsed:
            raise Exception("Have been parsed")

        name = self._uniformize(name)
        group = self._uniformize(group if group else self._default_group_name)
        self._opts.setdefault(group, {})

        if name in self._opts[group]:
            raise KeyError("The option {0} has been regisetered".format(name))

        self._opts[group][name] = (parser, default, help, short)
        self._caches.setdefault(group, Configuration.Group(group))

    def _parse_int(self, value):
        return int(value)

    def _parse_float(self, value):
        return float(value)

    def _parse_bool(self, value):
        if isinstance(value, bool):
            return value
        elif not isinstance(value, str):
            return bool(value)

        value = value.lower()
        if value in self._bool_true:
            return True
        elif value in self._bool_false:
            return False
        raise ValueError("invalid bool value '{0}'".format(value))

    def _parse_string(self, value):
        return value.decode(self._encoding) if isinstance(value, bytes) else value

    def _parse_ints(self, value):
        return self._parse_list(self._parse_int, value)

    def _parse_strings(self, value):
        return self._parse_list(self._parse_string, value)

    def _parse_list(self, parser, value):
        if isinstance(value, (list, tuple)):
            vs = value
        else:
            vs = (v.strip() for v in value.split(",") if v.strip())
        return tuple((parser(v) for v in vs))

    def _uniformize(self, name):
        return name.replace("-", "_")

    def _unniformize(self, name):
        return name.replace("_", "-")

    def parsed(self):
        """Return True if it has been parsed, or False."""
        return self._parsed

    def parse_files(self, filenames=""):
        """Parse the INI configuration files.

        The argument is either a string standing for the path of the
        configuration file, or a list of them.
        """
        if self._parsed:
            raise Exception("Have been parsed")
        self._parsed = True

        if filenames:
            if not isinstance(filenames, (list, tuple)):
                filenames = self._parse_string(filenames).strip(", ").split(",")

            for filename in filenames:
                self._parse_file(filename)

        self._check_and_fix()

    def _check_and_fix(self):
        for gname, opts in self._opts.items():
            group = self._caches[gname]
            for name, opt in opts.items():
                if name in group:
                    continue
                elif opt[1] is not None or opt[0] == self._parse_bool:
                    self._set_group_opt(gname, name, opt[1])
                    continue

                if not self._allow_empty:
                    msg = "The option '{0}' in the group '{1}' has no value."
                    raise ValueError(msg.format(name, gname))

        # Set the options in the default group into self.
        group = self._caches.pop(self._default_group_name)
        for key, value in group.items():
            if key in self._caches:
                msg = "'{0}' had has the value '{1}'"
                raise ValueError(msg.format(self.__class__.__name__, key))
            self._caches[key] = value

    def _parse_file(self, filename):
        filename = str(filename)
        with open(filename) as f:
            lines = f.readlines()

        gname = self._default_group_name
        index, max_index = 0, len(lines)
        while index < max_index:
            line = self._parse_string(lines[index]).strip()
            index += 1

            # Comment
            if not line or line[0] in ("#", "=", ";"):
                continue

            # Group Section
            if line[0] == "[":
                if line[-1] != "]":
                    m = ("the format of the group is wrong, "
                         "which must start with [ and end with ]")
                    raise ValueError(m)
                _gname = line[1:-1]
                if not _gname:
                    raise ValueError("the group name is empty")
                if _gname not in self._caches:
                    continue
                gname = _gname
                continue

            # Group Option Values
            items = line.split("=", 1)
            if len(items) != 2:
                raise ValueError("the format is wrong, must contain '=': " + line)

            name, value = self._uniformize(items[0].strip()), items[1].strip()

            # Handle the continuation line
            if value[-1:] == "\\":
                values = [value.rstrip("\\").strip()]
                while index < max_index:
                    value = lines[index].strip()
                    values.append(value.rstrip("\\").strip())
                    index += 1
                    if value[-1:] != "\\":
                        break
                value = "\n".join(values)

            opt = self._opts[gname].get(name, None)
            if opt:
                self._set_group_opt(gname, name, opt[0](value))

    def register_bool(self, name, short=None, default=None, group=None, help=None):
        """Register the bool option.

        The value of this option will be parsed to the type of bool.
        """
        self._register(name, self._parse_bool, short=short, default=default,
                       group=group, help=help)

    def register_int(self, name, short=None, default=None, group=None, help=None):
        """Register the int option.

        The value of this option will be parsed to the type of int.
        """
        self._register(name, self._parse_int, short=short, default=default,
                       group=group, help=help)

    def register_float(self, name, short=None, default=None, group=None, help=None):
        """Register the float option.

        The value of this option will be parsed to the type of float.
        """
        self._register(name, self._parse_float, short=short, default=default,
                       group=group, help=help)

    def register_str(self, name, short=None, default=None, group=None, help=None):
        """Register the str option.

        The value of this option will be parsed to the type of str.
        """
        self._register(name, self._parse_string, short=short, default=default,
                       group=group, help=help)

    def register_int_list(self, name, short=None, default=None, group=None, help=None):
        """Register the int list option.

        The value of this option will be parsed to the type of int list.
        """
        self._register(name, self._parse_ints, short=short, default=default,
                       group=group, help=help)

    def register_str_list(self, name, short=None, default=None, group=None, help=None):
        """Register the string list option.

        The value of this option will be parsed to the type of string list.
        """
        self._register(name, self._parse_strings, short=short, default=default,
                       group=group, help=help)

    ###########################################################################
    # Parse CLI
    def parse(self, *args, **kwargs):
        return self.parse_cli(*args, **kwargs)

    def parse_cli(self, args=None, config_file_name="config-file"):
        """Parse the cli options."""
        if self._parsed:
            raise Exception("Have been parsed")
        self._parsed = True

        if args is None:
            args = sys.argv[1:]
        if not args:
            self._check_and_fix()
            return None

        gopts, args = self._parser_cli(args, description=self._description,
                                       config_file_name=config_file_name)
        if getattr(args, "version", False):
            print(self._version)
            sys.exit(0)

        if config_file_name:
            config_file = getattr(args, self._uniformize(config_file_name), "")
            for filename in config_file.split(","):
                filename = filename.strip()
                if filename:
                    self._parse_file(filename)

        for cli_opt, (gname, name) in gopts.items():
            opt = self._opts[gname][name]
            value = getattr(args, cli_opt, None)
            if value is not None:
                value = opt[0](value)
                if value != opt[1]:
                    self._set_group_opt(gname, name, value, force=True)

        self._check_and_fix()
        return args

    def _parser_cli(self, args, description=None, config_file_name=None):
        cli = ArgumentParser(description=description)
        if config_file_name:
            cli.add_argument("--" + config_file_name, default="",
                             help="The config file path.")
        cli.add_argument("--version", action="store_true",
                         help="Print the version and exit.")

        group_opts = {}
        for gname, opts in self._opts.items():
            if gname == self._default_group_name:
                group = cli
            else:
                group = cli.add_argument_group(gname)

            for name, (parser, default, help, short) in opts.items():
                action = None
                if parser == self._parse_bool:
                    action = "store_false" if default else "store_true"
                    default = False if default is None else default

                if gname == self._default_group_name:
                    opt_name = self._unniformize(name)
                    opt_key = self._uniformize(name)
                else:
                    opt_name = self._unniformize("{0}-{1}".format(gname, name))
                    opt_key = self._uniformize(opt_name)
                group_opts[opt_key] = (gname, name)
                short = "-" + short if short and short[0] != "-" else short
                names = [short, "--" + opt_name] if short else ["--" + opt_name]
                group.add_argument(*names, action=action, default=default, help=help)

        return group_opts, cli.parse_args(args=args)
# Configuration End
###############################################################################

###############################################################################
# Common
import requests
from urllib.parse import quote as qs_quote


def send_http_get(url, quote=True, use_key=False, co="?", timeout=5, json=False,
                  raise404=True, has_result=True, headers=None, **ks):
    if ks:
        to = lambda v: qs_quote(v) if quote else v
        ks = {k: to(v() if callable(v) else v) for k, v in ks.items() if v is not None}
        if use_key:
            url = co.join((url, "&".join(("%s=%s" % (k, v) for k, v in ks.items()))))
        else:
            url = url.format(**ks)

    if json:
        if headers:
            headers["Accept"] = "application/json"
        else:
            headers = {"Accept": "application/json"}

    resp = requests.get(url, headers=headers, timeout=timeout)
    status_code = resp.status_code
    if status_code == 404:
        if raise404:
            raise Exception("not found %s" % url)
        return None
    elif status_code == 200:
        if has_result:
            return resp.json() if json else resp.content
        return None
    elif status_code == 204:
        return None
    raise OSError("%s: status_code=%s" % (url, status_code))
# Common End
###############################################################################

###############################################################################
# DB Common
from sqlalchemy import create_engine, text as sql_text
from sqlalchemy.orm import sessionmaker, object_mapper
from sqlalchemy.sql.elements import TextClause


class DB:
    """Manager the DB connection."""

    def __init__(self, write_connection, read_connection=None, autocommit=True,
                 expire_on_commit=False, echo=False, encoding="utf8",
                 poolclass=None, pool=None, min_pool_size=2, max_pool_size=5,
                 pool_timeout=30, idle_timeout=3600, base=None):

        write_connection = self._fix_charset(write_connection, encoding)
        if read_connection:
            read_connection = self._fix_charset(read_connection, encoding)

        kwargs = {
            "echo": echo,
            "encoding": encoding,
            "poolclass": poolclass,
            "pool": pool,
            "pool_size": min_pool_size,
            "pool_timeout": pool_timeout if pool_timeout else None,
            "pool_recycle": idle_timeout,
            "max_overflow": max_pool_size - min_pool_size,
            "convert_unicode": True,
        }

        self._base = base
        self._autocommit = autocommit
        self._expire_on_commit = expire_on_commit

        self._write_engine = self._create_engine(write_connection, kwargs)
        self._write_session_cls = self._get_session_cls(self._write_engine)

        if read_connection:
            self._read_engine = self._create_engine(read_connection, kwargs)
            self._read_session_cls = self._get_session_cls(self._read_engine)
        else:
            self._read_engine = self._write_engine
            self._read_session_cls = self._write_session_cls

    def _fix_charset(self, connection, encoding):
        if "mysql" in connection and "charset=" not in connection:
            if "?" in connection:
                return "%s&charset=%s" % (connection, encoding)
            return "%s?charset=%s" % (connection, encoding)
        return connection

    def _create_engine(self, connection, kwargs):
        if connection.startswith("sqlite:///"):
            kwargs.pop("pool_size", None)
            kwargs.pop("pool_timeout", None)
            kwargs.pop("max_overflow", None)
        return create_engine(connection, **kwargs)

    def _get_session_cls(self, engine):
        return sessionmaker(bind=engine, autocommit=self._autocommit,
                            expire_on_commit=self._expire_on_commit)

    def create_tables(self, base=None):
        (base or self._base).metadata.create_all(self._write_engine)

    def get_write_session(self):
        return self._write_session_cls()

    def get_read_session(self):
        return self._read_session_cls()

    def get_session(self):
        return self.get_write_session()

    def execute(self, sql, session=None, **kwargs):
        if not isinstance(sql, TextClause):
            sql = sql_text(sql)
        return (session or self.get_session()).execute(sql, kwargs)

    def fetchall(self, sql, **kwargs):
        return self.execute(sql, self.get_read_session(), **kwargs).fetchall()

    def fetchone(self, sql, **kwargs):
        return self.execute(sql, self.get_read_session(), **kwargs).fetchone()

    def first(self, sql, **kwargs):
        return self.execute(sql, self.get_read_session(), **kwargs).first()


class ModelBase:
    """Base class for models."""
    __tablename__ = ""
    __table_initialized__ = False

    def save(self, session):
        """Save this object."""

        # NOTE(boris-42): This part of code should be look like:
        #                       session.add(self)
        #                       session.flush()
        #                 But there is a bug in sqlalchemy and eventlet that
        #                 raises NoneType exception if there is no running
        #                 transaction and rollback is called. As long as
        #                 sqlalchemy has this bug we have to create transaction
        #                 explicitly.
        with session.begin(subtransactions=True):
            session.add(self)
            session.flush()

    def __repr__(self):
        attrs = ", ".join(("%s=%s" % (k, v) for k, v in self.items()))
        return "%s(%s)" % (self.__tablename__.title(), attrs)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):
        # Don't use hasattr() because hasattr() catches any exception, not only
        # AttributeError. We want to passthrough SQLAlchemy exceptions
        # (ex: sqlalchemy.orm.exc.DetachedInstanceError).
        try:
            getattr(self, key)
        except AttributeError:
            return False
        else:
            return True

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __iter__(self):
        return ModelIterator(self, iter(dict(object_mapper(self).columns).keys()))

    def update(self, values):
        """Make the model object behave like a dict."""
        for k, v in values.items():
            setattr(self, k, v)

    def _as_dict(self):
        """Make the model object behave like a dict.
        Includes attributes from joins.
        """
        local = dict((key, value) for key, value in self)
        joined = dict([(k, v) for k, v in self.__dict__.items() if not k[0] == '_'])
        local.update(joined)
        return local

    def items(self):
        """Make the model object behave like a dict."""
        return self._as_dict().items()

    def keys(self):
        """Make the model object behave like a dict."""
        return [key for key, value in self.items()]


class ModelIterator:
    def __init__(self, model, columns):
        self.model = model
        self.i = columns

    def __iter__(self):
        return self

    def __next__(self):
        n = next(self.i)
        return n, getattr(self.model, n)

# DB Common End
###############################################################################

###############################################################################
# DB
# from datetime import datetime
# from sqlalchemy import Column, String, Boolean, Integer, DateTime
# from sqlalchemy.sql import func, expression as expr
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class Model(ModelBase, BASE):
    __tablename__ = "table"


class DBAPI(DB):
    pass

# DB End
###############################################################################


def main(version="1.0.0"):
    conf = Configuration(description="", version=version)
    conf.register_str("log_level", default="INFO",
                      help="The level of the log, such as debug, info, etc.")
    conf.register_str("log_file", default="", help="The file path of the log.")
    conf.register_int("thread_num", default=0, help="The size of the coroutine pool.")
    conf.parse()

    if conf.thread_num > 0:
        global taskpool, spawn
        taskpool = gevent.pool.Pool(size=conf.thread_num)
        spawn = taskpool.spawn

    init_logging(LOG, conf.log_level, conf.log_file)

    # TODO:)


if __name__ == "__main__":
    main()
