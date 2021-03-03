"""
syslogmp.stream
~~~~~~~~~~~~~~~

Treat binary data as a stream and provide methods to read from it.


:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from itertools import islice, takewhile


class Stream(object):
    def __init__(self, data):
        self.iterator = iter(data)

    def read(self, n):
        """Return the next `n` bytes."""
        return bytes(islice(self.iterator, n))

    def read_until(self, stop_byte):
        """Return bytes until the first occurrence of the stop byte.

        The stop byte is not returned, but silently dropped from the
        remaining stream data.
        """
        predicate = create_match_predicate(stop_byte)
        return bytes(takewhile(predicate, self.iterator))

    def read_until_inclusive(self, stop_byte):
        """Return bytes until, and including, the first occurrence of
        the stop byte.
        """

        def inner():
            predicate = create_match_predicate(stop_byte)
            for x in self.iterator:
                yield x
                if not predicate(x):
                    return

        return bytes(inner())

    def read_remainder(self):
        """Return all remaining bytes."""
        return bytes(self.iterator)


def create_match_predicate(value_to_match):
    value_to_match = ord(value_to_match)
    return lambda x: x != value_to_match
