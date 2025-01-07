"""
syslogmp.stream
~~~~~~~~~~~~~~~

Treat binary data as a stream and provide methods to read from it.


:Copyright: 2007-2025 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from itertools import islice, takewhile
from typing import Callable, Iterator


class Stream:
    def __init__(self, data: bytes) -> None:
        self.iterator = iter(data)

    def read(self, n: int) -> bytes:
        """Return the next `n` bytes."""
        return bytes(islice(self.iterator, n))

    def read_until(self, stop_byte: bytes) -> bytes:
        """Return bytes until the first occurrence of the stop byte.

        The stop byte is not returned, but silently dropped from the
        remaining stream data.
        """
        predicate = create_match_predicate(stop_byte)
        return bytes(takewhile(predicate, self.iterator))

    def read_until_inclusive(self, stop_byte: bytes) -> bytes:
        """Return bytes until, and including, the first occurrence of
        the stop byte.
        """

        def inner() -> Iterator[int]:
            predicate = create_match_predicate(stop_byte)
            for code_point in self.iterator:
                yield code_point
                if not predicate(code_point):
                    return

        return bytes(inner())

    def read_remainder(self) -> bytes:
        """Return all remaining bytes."""
        return bytes(self.iterator)


def create_match_predicate(value_to_match: bytes) -> Callable[[int], bool]:
    code_point = ord(value_to_match)
    return lambda cp: cp != code_point
