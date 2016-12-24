
#!/usr/bin/env python

from __future__ import print_function, absolute_import, unicode_literals, division


# @Author: xgfone
# @Email: xgfone@126.com
class Configuration(object):

    class __Option(object):
        INT_TYPE = int
        STR_TYPE = str
        BOOL_TYPE = bool
        STR2TYPE = {
            "str": STR_TYPE,
            "int": INT_TYPE,
            "bool": BOOL_TYPE,
        }

        BOOL_TRUE = ["t", "true", "1"]
        BOOL_FALSE = ["f", "false", "0"]

        def __init__(self, _type, default=None, nargs=1, help=None):
            self.type = self.STR2TYPE.get(_type, _type)
            self.default = default
            self.nargs = nargs
            self.help = help
            self._value = None

        @classmethod
        def fix_py2(cls):
            import sys
            if sys.version_info[0] == 2:
                cls.STR_TYPE = unicode
                cls.STR2TYPE["str"] = cls.STR_TYPE

        @property
        def is_bool(self):
            return self.type is self.BOOL_TYPE

        def get_value(self, value):
            if isinstance(value, (self.BOOL_TYPE, self.INT_TYPE)):
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
                    raise ValueError("{0} is invalid! Only t, true, f, false, 1, 0 are valid".format(value))

            try:
                return self.type(value)
            except Exception:
                raise ValueError("{0} can not be converted to {1}".format(value, self.type))

    __Option.fix_py2()
    __DEFAULT_OPTION = __Option("str")

    def __init__(self, description="", filenames=None, config_opt="config_file", strict=False):
        """A simple configuration parser, including the file and CLI.

        We only support to parse the types of integer, bool, string, not list.
        And we don't support the group or section. It is just used in one simple
        script, not a big project. If it's the case, please use the package,
        oslo.config.

        When parsing the file or CLI, you can get the configuration option by
        the attribution or the dict key, such as conf.option or conf["option"].
        If the option does not exist, they will raise AttributeError or KeyError
        respectively.

        When an configuration option does not exist, for getting one default value,
        not raising an exception, please use the method of get(), or the builtin
        function of getattr().

        Notice: In principle, This class should support Python 2.6, 2.7 and 3.X.
        And it should not have any dependencies. In Python 2.X, the str type is
        unicode; In 3.X, it's str.

        @param description(string): A brief description about this program.
        @param filename(string):    The path of the configuration file.
        @param config_opt(string):  The CLI option name of the configuration file.
                                    Use it if @filename is not given.
        @param strict(bool):        If True, not parse the options, which are not
                                    registered, or whose value don't have the
                                    symbol of "=". This param only affects those
                                    options in the configuration file.

        """
        if not filenames:
            filenames = []
        if not isinstance(filenames, (list, tuple)):
            filenames = [filenames]

        self.__filenames = filenames
        self.__description = description
        self.__config_opt = config_opt
        self.__strict = strict
        self.__caches = {}
        self.__opts = {}
        self.__parsed = False

        self.__init_opts()

    def __init_opts(self):
        self.__register(self.__config_opt,
                        Configuration.__Option("str", default="", help="The path of the configuration file"))

    def __get_value(self, name, value):
        opt = self.__opts.get(name, self.__DEFAULT_OPTION)
        return opt.get_value(value)

    def __parse(self, argv=None):
        if self.__parsed:
            raise Exception("Have been parsed")

        # Parse the CLI options
        clis = self.__parse_cli(argv=argv)

        # Calculate and parse all the configuration files
        # filenames = [].extend(self.__filenames)
        filenames = self.__filenames
        _filenames = getattr(clis, self.__config_opt, [])
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
            if value is None:
                continue
            self.__caches[name] = self.__get_value(name, value)

        # Check whether the empty value options exists.
        for name in self.__opts.keys():
            if name not in self.__caches:
                raise ValueError("The option {0} does not have a value.".format(name))

        self.__parsed = True

    def __parse_cli(self, argv=None):
        try:
            import argparse
            Parser = argparse.ArgumentParser
            add_option = Parser.add_argument
            get_args = lambda parser: parser.parse_args(args=argv)
        except ImportError:
            import optparse
            Parser = optparse.OptionParser
            add_option = Parser.agg_option
            get_args = lambda parser: parser.parse_args(args=argv)[0]

        parser = Parser(description=self.__description)
        for name, opt in self.__opts.items():
            kwargs = {}
            if opt.help is not None:
                kwargs["help"] = opt.help

            _default = opt.default
            if opt.is_bool:
                if _default:
                    kwargs["action"] = "store_true"
                else:
                    kwargs["action"] = "store_false"
            else:
                kwargs["nargs"] = opt.nargs
                if _default is not None:
                    kwargs["default"] = _default

            add_option(parser, "--" + name, **kwargs)
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
            if not line or line[0] in ("#", "="):
                continue

            items = line.split("=", 1)
            if len(items) != 2 and self.__strict:
                continue
            else:
                items.append("")  # We don't use it when len(items)==2.

            name, value = items[0].strip(), items[1].strip()
            if name not in self.__opts and self.__strict:
                continue
            if name in self.__caches:
                raise ValueError("The option {0} has been parsed".format(name))
            self.__caches[name] = self.__get_value(name, value)

    def __getattr__(self, name):
        if not self.__parsed:
            raise Exception("Not parsed, can not get the value of the option of {0}".format(name))

        try:
            return self.__caches[name]
        except KeyError:
            raise AttributeError(name)

    def __getitem__(self, name):
        if not self.__parsed:
            raise Exception("Not parsed")

        try:
            return self.__caches[name]
        except KeyError:
            raise IndexError(name)

    def get(self, name, default=None):
        """Get the value of the configuration option of name.

        If there is not this option, return default, which is None by default.
        """
        return getattr(self, name, default)

    def __register(self, name, opt):
        name = name.strip()
        if name in self.__opts:
            raise KeyError("The option {0} has been regisetered".format(name))
        self.__opts[name] = opt

    def register_bool(self, name, default=None, help=None):
        """Register the bool option.

        The value of this option will be parsed to the type of bool.
        """
        opt = Configuration.__Option("bool", default=default, help=help)
        self.__register(name, opt)

    def register_int(self, name, default=None, help=None):
        """Register the int option.

        The value of this option will be parsed to the type of int.
        """
        opt = Configuration.__Option("int", default=default, help=help)
        self.__register(name, opt)

    def register_str(self, name, default=None, nargs=1, help=None):
        """Register the str option.

        The value of this option will be parsed to the type of str.
        """
        opt = Configuration.__Option("str", default=default, help=help)
        self.__register(name, opt)

    def parse(self, argv=None):
        """Parse the configuration file and CLI.

        It will raise an execption if having been parsed.
        """
        self.__parse(argv)

    def parsed(self):
        """Return True if it has been parsed, or False."""
        return self.__parsed


def main():
    strict = False
    filename = "test.conf"
    conf = Configuration(filenames=filename, strict=strict)
    conf.register_bool("a1", default=True)
    conf.register_int("a4")
    conf.parse()
    print(type(conf.a1), conf.a1)
    # print(type(conf.a5), conf.a5)
    print(type(getattr(conf, "a4")), conf.a4)


if __name__ == "__main__":
    main()
