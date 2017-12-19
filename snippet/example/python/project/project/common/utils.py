# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals, division

import pbr.version

from six import text_type as unicode_type
from six import string_types as basestring_type
from six import binary_type as bytes_type

_BYTES_TYPES = (bytes_type, type(None))
_UNICODE_TYPES = (unicode_type, type(None))
_BASESTRING_TYPES = (basestring_type, type(None))


def get_version(project, version=None):
    if version:
        return version
    return pbr.version.VersionInfo(project).version_string()


def to_bytes(obj, encoding="utf-8"):
    """Converts a string argument to a bytes string.

    If the argument is already a bytes string or None, it is returned
    unchanged.  Otherwise it must be a unicode string and is decoded as
    the argument of encoding."""
    if isinstance(obj, _BYTES_TYPES):
        return obj
    elif isinstance(obj, unicode_type):
        return obj.encode(encoding)
    raise TypeError("Expected bytes, unicode, or None; got %r" % type(obj))


def to_unicode(obj, decoding="utf-8"):
    """Converts a string argument to a unicode string.

    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as
    the argument of encoding.
    """
    if isinstance(obj, _UNICODE_TYPES):
        return obj
    elif isinstance(obj, bytes_type):
        return obj.decode(decoding)
    raise TypeError("Expected bytes, unicode, or None; got %r" % type(obj))


def to_basestring(value, encoding="utf-8"):
    """Converts a string argument to a subclass of basestring.

    In python2, byte and unicode strings are mostly interchangeable,
    so functions that deal with a user-supplied argument in combination
    with ascii string constants can use either and should return the type
    the user supplied.  In python3, the two types are not interchangeable,
    so this method is needed to convert byte strings to unicode.
    """
    if isinstance(value, _BASESTRING_TYPES):
        return value
    if not isinstance(value, bytes):
        return value.decode(encoding)
    raise TypeError("Expected bytes, unicode, or None; got %r" % type(value))


# When dealing with the standard library across python 2 and 3 it is
# sometimes useful to have a direct conversion to the native string type
if str is unicode_type:
    to_str = native_str = to_unicode
else:
    to_str = native_str = to_bytes
