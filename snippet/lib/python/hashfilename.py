#!/usr/bin/env python
# coding: utf-8
"""
A algorithm of the hashfilename in qemu livebackup, MurmurHashNeutral2,
implemented by Python.
"""


def _MurmurHashNeutral2(key, seed):
    if seed < 0:
        return None
    length = len(key)

    m = 0x5bd1e995
    r = 24
    h = seed ^ length
    UINTMAX = 1 << 32

    while length >= 4:
        k = ord(key[0])
        k |= ord(key[1]) << 8
        k |= ord(key[2]) << 16
        k |= ord(key[3]) << 24

        k *= m
        k %= UINTMAX
        k ^= k >> r
        k *= m
        k %= UINTMAX

        h *= m
        h %= UINTMAX
        h ^= k

        key = key[4:]
        length -= 4

    if length == 3:
        h ^= ord(key[2]) << 16
        h ^= ord(key[1]) << 8
        h ^= ord(key[0])
    elif length == 2:
        h ^= ord(key[1]) << 8
        h ^= ord(key[0])
    elif length == 1:
        h ^= ord(key[0])
    h *= m
    h %= UINTMAX

    h ^= h >> 13
    h *= m
    h %= UINTMAX
    h ^= h >> 15

    return h


def create_hashfilename(vdisk_file):
    hv = _MurmurHashNeutral2(vdisk_file, 0)
    return "{0:x}".format(hv)


if __name__ == "__main__":
    import sys
    print create_hashfilename(sys.argv[1])
