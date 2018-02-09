#!/usr/bin/env python3

import sys

if sys.version_info[0] < 3:
    import __builtin__ as builtins
    PY3, Unicode, Bytes = False, unicode, str
else:
    import builtins
    PY3, Unicode, Bytes = True, str, bytes

# to_bytes = lambda v, e="utf-8": v.encode(e) if isinstance(v, Unicode) else v
# to_unicode = lambda v, e="utf-8": v.decode(e) if isinstance(v, Bytes) else v
# to_str = to_unicode if PY3 else to_bytes


def to_bytes(v, encoding="utf-8", **kwargs):
    if isinstance(v, Bytes):
        return v
    elif isinstance(v, Unicode):
        return v.encode(encoding)
    return to_bytes(str(v), encoding=encoding)


def to_unicode(v, encoding="utf-8", **kwargs):
    if isinstance(v, Bytes):
        return v.decode(encoding)
    elif isinstance(v, Unicode):
        return v
    return to_unicode(str(v), encoding=encoding)


def set_builtin(name, value, force=False):
    exist = getattr(builtins, name, None)
    if exist and force:
        return False
    setattr(builtins, name, value)
    return True


is_string = lambda s: True if isinstance(s, (Bytes, Unicode)) else False
to_str = to_unicode if PY3 else to_bytes
set_builtin("str", to_unicode, force=True)
# Patch End
##############################################################################


##############################################################################
# Python 2.6 Patch
try:
    from argparse import ArgumentParser
except ImportError:
    from optparse import OptionParser

    class OptionParserGroupProxy(object):
        def __init__(self, group):
            self.__group = group

        def __repr__(self):
            return str(self.__group)

        def __getattr__(self, name):
            return getattr(self.__group, name)

        def add_argument(self, *args, **kwargs):
            return self.__group.add_option(*args, **kwargs)

    class ArgumentParser(OptionParser):
        def add_argument_group(self, *args, **kwargs):
            group = self.add_option_group(*args, **kwargs)
            return OptionParserGroupProxy(group)

        def add_argument(self, *args, **kwargs):
            return self.add_option(*args, **kwargs)

# Python 2.6 Patch End
##############################################################################


# @Author: xgfone
# @Email: xgfone@126.com
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
            raise AttributeError("The group '{0}' has no the option '{1}'".format(self.__name, name))

        def __setitem__(self, name, value):
            setattr(self, name, value)

        def __getitem__(self, name):
            try:
                return getattr(self, name)
            except AttributeError:
                raise KeyError("The group '{0}' has no the option '{1}'".format(self.__name, name))

        def items(self):
            d = vars(self)
            d.pop("_Group__name")
            return d.items()

    __slots__ = ["_default_group_name", "_default_group", "_allow_empty",
                 "_encoding", "_parsed", "_caches", "_opts", "_bool_true",
                 "_bool_false", "_py2", "_description"]

    def __init__(self, description=None, allow_empty=False, encoding="utf-8",
                 default_group="DEFAULT"):
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

        self._caches = {self._default_group_name: self._default_group}
        self._opts = {}

        self._bool_true = ["t", "1", "T", "on", "On", "ON", "true", "True", "TRUE"]
        self._bool_false = ["f", "0", "F", "off", "Off", "OFF", "false", "False", "FALSE"]

        try:
            "".decode()
        except AttributeError:
            self._py2 = False
        else:
            self._py2 = True

    def __getattr__(self, name):
        if not self._parsed:
            raise Exception("Not parsed")

        try:
            return self._caches[name]
        except KeyError:
            pass

        msg = "'{0}' object has no attribute '{1}"
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
        attrs = []
        for key, value in self._caches.items():
            attrs.append("{0}={1}".format(key, value))
        return "{0}({1})".format(self.__class__.__name__, ", ".join(attrs))

    def _set_group_opt(self, group_name, opt_name, opt_value, force=False):
        gname = group_name if group_name else self._default_group_name
        group = self._caches[gname]
        if hasattr(group, opt_name) and not force:
            raise ValueError("The group '{0}' has had the value of '{1}'".format(gname, opt_name))
        setattr(self._caches[gname], opt_name, opt_value)

    def _register(self, name, parser, default=None, group=None, help=None):
        if self._parsed:
            raise Exception("Have been parsed")

        name = self._uniformize(name)
        group = self._uniformize(group if group else self._default_group_name)
        self._opts.setdefault(group, {})

        if name in self._opts[group]:
            raise KeyError("The option {0} has been regisetered".format(name))

        self._opts[group][name] = (parser, default, help)
        self._caches.setdefault(group, Configuration.Group(group))

    def _parse_int(self, value):
        return int(value)

    def _parse_float(self, value):
        return float(value)

    def _parse_bool(self, value):
        if value in self._bool_true:
            return True
        elif value in self._bool_false:
            return False
        raise ValueError("invalid bool value '{0}'".format(value))

    def _parse_string(self, value):
        if self._py2:
            if isinstance(value, str):
                value.decode(self._encoding)
        else:
            if not isinstance(value, str):
                return value.decode(self._encoding)
        return value

    def _parse_ints(self, value):
        return self._parse_list(self._parse_int, value)

    def _parse_strings(self, value):
        return self._parse_list(self._parse_string, value)

    def _parse_list(self, parser, value):
        vs = []
        for v in value.strip(",").split(","):
            v = v.strip()
            if not v:
                continue
            vs.append(parser(v))
        return vs

    def _uniformize(self, name):
        return name.replace("-", "_")

    def _unniformize(self, name):
        return name.replace("_", "-")

    def parsed(self):
        """Return True if it has been parsed, or False."""
        return self._parsed

    def parse(self, filenames=""):
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
                elif opt[1] is not None:
                    setattr(group, name, opt[1])
                    continue

                if not self._allow_empty:
                    msg = "The option '{0}' in the group '{1}' doesn't have a value."
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
            line = lines[index].strip()
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

    def register_bool(self, name, default=None, group=None, help=None):
        """Register the bool option.

        The value of this option will be parsed to the type of bool.
        """
        self._register(name, self._parse_bool, default=default, group=group, help=help)

    def register_int(self, name, default=None, group=None, help=None):
        """Register the int option.

        The value of this option will be parsed to the type of int.
        """
        self._register(name, self._parse_int, default=default, group=group, help=help)

    def register_float(self, name, default=None, group=None, help=None):
        """Register the float option.

        The value of this option will be parsed to the type of float.
        """
        self._register(name, self._parse_float, default=default, group=group, help=help)

    def register_str(self, name, default=None, group=None, help=None):
        """Register the str option.

        The value of this option will be parsed to the type of str.
        """
        self._register(name, self._parse_string, default=default, group=group, help=help)

    def register_int_list(self, name, default=None, group=None, help=None):
        """Register the int list option.

        The value of this option will be parsed to the type of int list.
        """
        self._register(name, self._parse_ints, default=default, group=group, help=help)

    def register_str_list(self, name, default=None, group=None, help=None):
        """Register the string list option.

        The value of this option will be parsed to the type of string list.
        """
        self._register(name, self._parse_strings, default=default, group=group, help=help)

    ###########################################################################
    # Parse CLI
    def parse_cli(self, args=None, config_file_name="config-file"):
        """Parse the cli options."""
        if self._parsed:
            raise Exception("Have been parsed")
        self._parsed = True

        if args is None:
            args = sys.argv[1:]
        if not args:
            self._check_and_set_default()
            return

        gopts, args = self._parser_cli(args, description=self._description,
                                       config_file_name=config_file_name)

        if config_file_name:
            config_file = getattr(args, self._uniformize(config_file_name), "")
            for filename in config_file.split(","):
                filename = filename.strip()
                if filename:
                    self._parse_file(filename)

        for cli_opt, (gname, name) in gopts.items():
            default = self._opts[gname][name][1]
            value = getattr(args, cli_opt, None)
            if value is not None and value != default:
                self._set_group_opt(gname, name, value, force=True)

        self._check_and_fix()
        return args

    def _parser_cli(self, args, description=None, config_file_name=None):
        cli = ArgumentParser(description=description)
        if config_file_name:
            cli.add_argument("--" + config_file_name, default="", help="The config file path.")

        group_opts = {}
        for gname, opts in self._opts.items():
            group = cli if gname == self._default_group_name else cli.add_argument_group(gname)
            for name, (parser, default, help) in opts.items():
                action = None
                if parser is self._parse_bool:
                    action = "store_false" if default else "store_true"

                if gname == self._default_group_name:
                    opt_name = self._unniformize(name)
                    opt_key = self._uniformize(name)
                else:
                    opt_name = self._unniformize("{0}-{1}".format(gname, name))
                    opt_key = self._uniformize(opt_name)
                group_opts[opt_key] = (gname, name)
                group.add_argument("--" + opt_name, action=action, default=default, help=help)

        return group_opts, cli.parse_args(args=args)


if __name__ == "__main__":
    conf = Configuration()
    conf.register_str("attr", default="abc", help="opt test")
    conf.register_int("attr", default=None, group="group", help="group test")
    conf.parse_cli(["--group-attr", "456"])
    print("conf.attr = {0}".format(conf.attr))
    print('conf["attr"] = {0}'.format(conf["attr"]))
    print("conf.group.attr = {0}".format(conf.group.attr))
