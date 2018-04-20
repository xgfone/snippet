# -*- coding: utf-8 -*-

import random


# Default symbols to use for passwords. Avoids visually confusing characters.
# ~6 bits per symbol
DEFAULT_PASSWORD_SYMBOLS = ('23456789',  # Removed: 0,1
                            'ABCDEFGHJKLMNPQRSTUVWXYZ',   # Removed: I, O
                            'abcdefghijkmnopqrstuvwxyz')  # Removed: l


# ~5 bits per symbol
EASIER_PASSWORD_SYMBOLS = ('23456789',  # Removed: 0, 1
                           'ABCDEFGHJKLMNPQRSTUVWXYZ')  # Removed: I, O


def generate_password(length, symbolgroups=DEFAULT_PASSWORD_SYMBOLS):
    """Generate a random password from the supplied symbol groups.

    At least one symbol from each group will be included. Unpredictable
    results if length is less than the number of symbol groups.

    Believed to be reasonably secure (with a reasonable password length!)

    """
    r = random.SystemRandom()

    # NOTE(jerdfelt): Some password policies require at least one character
    # from each group of symbols, so start off with one random character
    # from each symbol group
    password = [r.choice(s) for s in symbolgroups]
    # If length < len(symbolgroups), the leading characters will only
    # be from the first length groups. Try our best to not be predictable
    # by shuffling and then truncating.
    r.shuffle(password)
    password = password[:length]
    length -= len(password)

    # then fill with random characters from all symbol groups
    symbols = ''.join(symbolgroups)
    password.extend([r.choice(symbols) for _i in range(length)])

    # finally shuffle to ensure first x characters aren't from a
    # predictable group
    r.shuffle(password)

    return ''.join(password)
