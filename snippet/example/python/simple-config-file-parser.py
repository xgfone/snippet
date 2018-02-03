#!/usr/bin/env python3


# @Author: xgfone
# @Email: xgfone@126.com
class Configuration(object):
    class Group(object):
        def __init__(self, group_name):
            self.__name = group_name

        def __repr__(self):
            return "Group(name={}, vars={})".format(self.__name, vars(self))

        def __contains__(self, name):
            return hasattr(self, name)

        def __getattr__(self, name):
            raise AttributeError("The group '{}' has no the option '{}'".format(self.__name, name))

        def __setitem__(self, name, value):
            setattr(self, name, value)

        def __getitem__(self, name):
            try:
                return getattr(self, name)
            except AttributeError:
                raise KeyError("The group '{}' has no the option '{}'".format(self.__name, name))

    __slots__ = ["_default_group_name", "_default_group", "_allow_empty",
                 "_encoding", "_parsed", "_caches", "_opts", "_bool_true",
                 "_bool_false", "_py2"]

    def __init__(self, allow_empty=True, default_group="DEFAULT", encoding="utf-8"):
        """A simple configuration file parser based on the format INI.

        When an configuration option does not exist, for getting one default
        value, not raising an exception, please use the method of get(), or the
        builtin function of getattr().
        """

        self._parsed = False
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
        return self._caches.get(name, None) or getattr(self._default_group, name)

    def __getitem__(self, name):
        if not self._parsed:
            raise Exception("Not parsed")

        name = self._uniformize(name)
        return self._caches.get(name, None) or self._default_group[name]

    def _register(self, name, parser, default=None, group=None):
        if self._parsed:
            raise Exception("Have been parsed")

        name = self._uniformize(name)
        group = self._uniformize(group if group else self._default_group_name)
        self._opts.setdefault(group, {})

        if name in self._opts[group]:
            raise KeyError("The option {} has been regisetered".format(name))

        self._opts[group][name] = (parser, default)
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
        raise ValueError("invalid bool value '{}'".format(value))

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

        # Set the default value
        for gname, opts in self._opts.items():
            group = self._caches[gname]
            for name, opt in opts.items():
                if name not in group and opt[1] is not None:
                    setattr(group, name, opt[1])
                    continue

                if not self._allow_empty:
                    msg = "The option {} in the group {} doesn't have a value."
                    raise ValueError(msg.format(name, gname))

    def _parse_file(self, filename):
        filename = str(filename)
        with open(filename) as f:
            lines = f.readlines()

        gname = self._default_group_name
        group = self._caches[gname]
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
                group = self._caches[gname]
                continue

            # Group Option Values
            items = line.split("=", 1)
            if len(items) != 2:
                raise ValueError("the format is wrong, must contain =: %s", line)

            name, value = self._uniformize(items[0].strip()), items[1].strip()
            if name in group:
                m = "The option {} in the group {} has been parsed"
                raise ValueError(m.format(name, gname))

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
                setattr(group, name, opt[0](value))

    def register_bool(self, name, default=None, group=None, help=None):
        """Register the bool option.

        The value of this option will be parsed to the type of bool.
        """
        self._register(name, self._parse_bool, default=default, group=group)

    def register_int(self, name, default=None, group=None, help=None):
        """Register the int option.

        The value of this option will be parsed to the type of int.
        """
        self._register(name, self._parse_int, default=default, group=group)

    def register_float(self, name, default=None, group=None, help=None):
        """Register the float option.

        The value of this option will be parsed to the type of float.
        """
        self._register(name, self._parse_float, default=default, group=group)

    def register_str(self, name, default=None, group=None, help=None):
        """Register the str option.

        The value of this option will be parsed to the type of str.
        """
        self._register(name, self._parse_string, default=default, group=group)

    def register_int_list(self, name, default=None, group=None, help=None):
        """Register the int list option.

        The value of this option will be parsed to the type of int list.
        """
        self._register(name, self._parse_ints, default=default, group=group)

    def register_str_list(self, name, default=None, group=None, help=None):
        """Register the string list option.

        The value of this option will be parsed to the type of string list.
        """
        self._register(name, self._parse_strings, default=default, group=group)


if __name__ == "__main__":
    conf = Configuration()
    conf.register_str("attr", default="abc")
    conf.parse("test.conf")
    print("conf.attr = {}".format(conf.attr))
    print('conf["attr"] = {}'.format(conf["attr"]))
