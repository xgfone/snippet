# encoding: utf-8

import sys


class _const(object):
    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError, "Can't change const.{0}".format(name)

        if not name.isupper():
            raise self.ConstCaseError, 'const name "{0}" is not all uppercase'.format(name)

        self.__dict__[name] = value


sys.modules[__name__.title()] = _const
sys.modules[__name__] = _const()
