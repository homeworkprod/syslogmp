# -*- coding: utf-8 -*-

"""
syslogmp.stream
~~~~~~~~~~~~~~~

Treat character data as a stream and provide methods to read from it.


:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from itertools import islice, takewhile


class Stream(object):

    def __init__(self, data):
        self.iterator = iter(data)

    def read(self, n):
        """Return the next `n` characters."""
        return ''.join(islice(self.iterator, n))

    def read_until(self, stop_character):
        """Return characters until the first occurrence of the stop
        character.

        The stop character is not returned, but silently dropped from
        the remaining stream data.
        """
        predicate = lambda c: c != stop_character
        return ''.join(takewhile(predicate, self.iterator))

    def read_until_inclusive(self, stop_character):
        """Return characters until, and including, the first occurrence
        of the stop character.
        """
        def inner():
            predicate = lambda c: c != stop_character
            for x in self.iterator:
                yield x
                if not predicate(x):
                    return

        return ''.join(inner())

    def read_remainder(self):
        """Return all remaining characters."""
        return ''.join(self.iterator)
