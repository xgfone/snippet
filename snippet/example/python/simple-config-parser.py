#!/usr/bin/env python
# ecoding: utf-8
from __future__ import print_function, absolute_import, unicode_literals, division

import sys


# @Author: xgfone
# @Email: xgfone@126.com
class Configuration(object):

    class __Option(object):
        INT_TYPE = int
        STR_TYPE = str
        BOOL_TYPE = bool
        FLOAT_TYPE = float
        STR2TYPE = {
            "str": STR_TYPE,
            "int": INT_TYPE,
            "bool": BOOL_TYPE,
            "float": FLOAT_TYPE,
        }

        BOOL_TRUE = ["t", "1", "T", "on", "On", "ON", "true", "True", "TRUE"]
        BOOL_FALSE = ["f", "0", "F", "off", "Off", "OFF", "false", "False", "FALSE"]

        def __init__(self, _type, name, short=None, default=None, nargs=1,
                     help=None, ignore_empty=False):
            self.name = name
            self.type = self.STR2TYPE.get(_type, _type)
            if self.type is self.BOOL_TYPE:
                self.default = bool(default)
            else:
                self.default = default
            self.ignore_empty = ignore_empty
            self.short = short
            self.nargs = nargs
            self.help = help
            self._value = None

        @classmethod
        def fix_py2(cls):
            if sys.version_info[0] == 2:
                cls.STR_TYPE = unicode
                cls.STR2TYPE["str"] = cls.STR_TYPE

        @property
        def is_bool(self):
            return self.type is self.BOOL_TYPE

        def get_value(self, value):
            if isinstance(value, (self.BOOL_TYPE, self.INT_TYPE, self.FLOAT_TYPE)):
                return value

            if isinstance(value, list) and len(value) > 0:
                value = value[0]

            value = value.strip()
            if self.type is self.BOOL_TYPE:
                value = self.STR_TYPE(value).lower()
                if value in self.BOOL_TRUE:
                    return True
                elif value in self.BOOL_FALSE:
                    return False
                else:
                    m = "{0} is invalid! Only t, true, f, false, 1, 0 are valid"
                    raise ValueError(m.format(value))

            try:
                return self.type(value)
            except Exception:
                m = "{0} can not be converted to {1}".format(value, self.type)
                raise ValueError(m)

    __Option.fix_py2()
    __DEFAULT_OPTION = __Option("str", "default")

    def __init__(self, description="", filenames=None, config_opt="config-file",
                 strict=False, use_hyphen=True, ignore_empty=True):
        """A simple configuration parser, including the file and CLI.

        We only support to parse the types of integer, bool, string, not list.
        And we don't support the group or section. It is just used in one simple
        script, not a big project. If it's the case, please use the package,
        oslo.config.

        When parsing the file or CLI, you can get the configuration option by
        the attribution or the dict key, such as conf.option or conf["option"].
        If the option does not exist, they will raise AttributeError or KeyError
        respectively.

        When an configuration option does not exist, for getting one default
        value, not raising an exception, please use the method of get(), or the
        builtin function of getattr().

        Notice: In principle, This class should support Python 2.6, 2.7 and 3.X.
        And it should not have any dependencies. In Python 2.X, the str type is
        unicode; In 3.X, it's str.

        @param description(string): A brief description about this program.
        @param filename(string):    The path of the configuration file.
        @param config_opt(string):  The CLI option name of the configuration
                                    file. Use it if @filename is not given.
        @param strict(bool):        If True, not parse the options, which are
                                    not registered, or whose value don't have
                                    the symbol of "=". This param only affects
                                    those options in the configuration file.
        """
        if not filenames:
            filenames = []
        if not isinstance(filenames, (list, tuple)):
            filenames = [filenames]

        self.__filenames = filenames
        self.__description = description
        self.__config_opt = config_opt
        self.__use_hyphen = use_hyphen
        self.__ignore_empty = ignore_empty
        self.__strict = strict
        self.__caches = {}
        self.__opts = {}
        self.__parsed = False

        self.__init_opts()

    def __init_opts(self):
        r1 = Configuration.__Option("str", self.__config_opt, ignore_empty=True,
                                    help="The path of the configuration file")
        r2 = Configuration.__Option("bool", "strict", default=False,
                                    help="If true, enable the strict mode.")
        self.__register(r1)
        self.__register(r2)

    def __uniformize(self, name):
        return name.strip().replace("-", "_")

    def __hyphen(self, name):
        return name.strip().replace("_", "-")

    def __get_value(self, name, value):
        opt = self.__opts.get(name, self.__DEFAULT_OPTION)
        return opt.get_value(value)

    def __parse(self, argv=None):
        if self.__parsed:
            raise Exception("Have been parsed")

        # Parse the CLI options
        clis = self.__parse_cli(argv=argv)

        if self.__strict is None:
            strict = getattr(clis, "strict", False)
            self.__strict = strict

        # Calculate and parse all the configuration files
        # filenames = [].extend(self.__filenames)
        filenames = self.__filenames
        _filenames = getattr(clis, self.__uniformize(self.__config_opt), None)
        if _filenames:
            if not isinstance(_filenames, (list, tuple)):
                _filenames = [_filenames]
            for filename in _filenames:
                for file in filename.split(","):
                    file = file.strip()
                    if file:
                        filenames.append(file)
        self.__parse_files(filenames)

        # Place the CLI options into the parsed cache.
        # We do it after parsing configuration file, because the priority of CLI
        # is higher than the configurations file.
        for name, value in vars(clis).items():
            name = self.__uniformize(name)
            if value is None and name not in self.__caches:
                value = self.__opts[name].default
            if value is None:
                continue
            self.__caches[name] = self.__get_value(name, value)

        self.__check_empty()
        self.__parsed = True

    def __check_empty(self):
        if self.__ignore_empty:
            return

        # Check whether the empty value options exists.
        for name, opt in self.__opts.items():
            if not opt.ignore_empty and name not in self.__caches:
                m = "The option {0} does not have a value.".format(name)
                raise ValueError(m)

    def __parse_cli(self, argv=None):
        try:
            import argparse
            Parser = argparse.ArgumentParser
            add_option = Parser.add_argument
            get_args = lambda parser: parser.parse_args(args=argv)
        except ImportError:
            import optparse
            Parser = optparse.OptionParser
            add_option = Parser.add_option
            get_args = lambda parser: parser.parse_args(args=argv)[0]

        parser = Parser(description=self.__description)
        for opt in self.__opts.values():
            kwargs = {}
            if opt.help is not None:
                kwargs["help"] = opt.help

            _default = opt.default
            if opt.is_bool:
                if _default:
                    kwargs["action"] = "store_false"
                else:
                    kwargs["action"] = "store_true"
            else:
                kwargs["nargs"] = opt.nargs

            names = []
            short = opt.short
            if short is not None and len(short) > 0:
                if short[0] != "-":
                    short = "-" + short
                names.append(short)
            name = self.__hyphen(opt.name) if self.__use_hyphen else opt.name
            names.append("--" + name)

            add_option(parser, *names, **kwargs)
        args = get_args(parser)
        return args

    def __parse_files(self, filenames):
        for filename in filenames:
            self.__parse_file(filename)

    def __parse_file(self, filename):
        filename = str(filename)
        with open(filename) as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or line[0] in ("#", "=", ";"):
                continue

            items = line.split("=", 1)
            if len(items) != 2:
                if self.__strict:
                    continue
                else:
                    items.append("")

            name, value = self.__uniformize(items[0]), items[1].strip()
            if name not in self.__opts and self.__strict:
                continue
            if name in self.__caches:
                raise ValueError("The option {0} has been parsed".format(name))
            self.__caches[name] = self.__get_value(name, value)

    def __getattr__(self, name):
        if not self.__parsed:
            msg = "Not parsed, can not get the value of the option of {0}"
            raise Exception(msg.format(name))

        try:
            return self.__caches[name]
        except KeyError:
            raise AttributeError(name)

    def __getitem__(self, name):
        if not self.__parsed:
            raise Exception("Not parsed")

        try:
            name = name.replace("-", "_")
            return self.__caches[name]
        except KeyError:
            raise IndexError(name)

    def get(self, name, default=None):
        """Get the value of the configuration option of name.

        If there is not this option, return default, which is None by default.
        """
        return getattr(self, name, default)

    def __register(self, opt):
        name = self.__uniformize(opt.name)
        if name in self.__opts:
            raise KeyError("The option {0} has been regisetered".format(name))
        self.__opts[name] = opt

    def register_float(self, name, short=None, default=None, help=None):
        """Register the float option.

        The value of this option will be parsed to the type of float.
        """
        opt = Configuration.__Option("float", name, short=short, default=default,
                                     help=help)
        self.__register(opt)

    def register_bool(self, name, short=None, default=None, help=None):
        """Register the bool option.

        The value of this option will be parsed to the type of bool.
        """
        opt = Configuration.__Option("bool", name, short=short, default=default,
                                     help=help)
        self.__register(opt)

    def register_int(self, name, short=None, default=None, help=None):
        """Register the int option.

        The value of this option will be parsed to the type of int.
        """
        opt = Configuration.__Option("int", name, short=short, default=default,
                                     help=help)
        self.__register(opt)

    def register_str(self, name, short=None, default=None, nargs=1, help=None):
        """Register the str option.

        The value of this option will be parsed to the type of str.
        """
        opt = Configuration.__Option("str", name, short=short, default=default,
                                     help=help)
        self.__register(opt)

    def parse(self, argv=None):
        """Parse the configuration file and CLI.

        It will raise an execption if having been parsed.
        """
        self.__parse(argv)

    def parsed(self):
        """Return True if it has been parsed, or False."""
        return self.__parsed


def main():
    conf = Configuration()
    conf.register_bool("a1", short='a')
    conf.register_int("a2", short='A', default=111)
    conf.register_str("a3", default="a3-value")
    conf.parse()
    print("a1", type(conf.a1), conf.a1)
    print("a2", type(getattr(conf, "a2")), conf.a2)
    print("a3", type(conf["a3"]), conf["a3"])


if __name__ == "__main__":
    main()
