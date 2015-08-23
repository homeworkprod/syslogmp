# -*- coding: utf-8 -*-

"""
syslogmp.parser
~~~~~~~~~~~~~~~

For more information, see `RFC 3164`_, "The BSD syslog Protocol".

Please note that there is `RFC 5424`_, "The Syslog Protocol", which
obsoletes `RFC 3164`_. This package, however, only implements the
latter.

.. _RFC 3164: http://tools.ietf.org/html/rfc3164
.. _RFC 5424: http://tools.ietf.org/html/rfc5424


:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from datetime import datetime
from itertools import islice, takewhile

from .facility import Facility
from .message import Message
from .severity import Severity


class Parser(object):
    """Parse syslog messages."""

    @classmethod
    def parse(cls, data):
        parser = cls(data)

        facility_id, severity_id = parser._parse_pri_part()
        facility = Facility(facility_id)
        severity = Severity(severity_id)
        timestamp = parser._parse_timestamp()
        hostname = parser._parse_hostname()
        message = ''.join(parser.iterator.take_remainder())

        return Message(facility, severity, timestamp, hostname, message)

    def __init__(self, data):
        max_bytes = 1024  # as stated by the RFC
        self.iterator = DataIterator(data[:max_bytes])

    def _parse_pri_part(self):
        """Extract facility and severity IDs from the PRI part."""
        pri_part = self.iterator.take_until_inclusive('>')

        ensure(len(pri_part) in {3, 4, 5},
               'PRI part must have 3, 4, or 5 characters.')

        ensure(pri_part.startswith('<'),
               'PRI part must start with an opening angle bracket (`<`).')

        ensure(pri_part.endswith('>'),
               'PRI part must end with a closing angle bracket (`>`).')

        priority_value = pri_part[1:-1]

        try:
            priority_value_number = int(priority_value)
        except ValueError:
            raise MessageFormatError(
                "Priority value must be a number, but is '{}'."
                    .format(priority_value))

        facility_id, severity_id = divmod(priority_value_number, 8)
        return facility_id, severity_id

    def _parse_timestamp(self):
        """Parse timestamp into a `datetime` instance."""
        timestamp_str = self.iterator.take(15)

        nothing = self.iterator.take_until(' ')  # Advance to next part.
        ensure(nothing == '',
               'Timestamp must be followed by a space character.')

        timestamp = datetime.strptime(timestamp_str, '%b %d %H:%M:%S')
        timestamp = timestamp.replace(year=datetime.today().year)
        return timestamp

    def _parse_hostname(self):
        return self.iterator.take_until(' ')


class DataIterator(object):

    def __init__(self, data):
        self.iterator = iter(data)

    def take_until(self, stop_character):
        """Return characters until the first occurrence of the stop
        character.
        """
        predicate = lambda c: c != stop_character
        return ''.join(takewhile(predicate, self.iterator))

    def take_until_inclusive(self, stop_character):
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

    def take(self, n):
        """Return the next `n` characters."""
        return ''.join(islice(self.iterator, n))

    def take_remainder(self):
        """Return all remaining characters."""
        return self.iterator


class MessageFormatError(ValueError):
    """Raised when data does not match the expected message structure."""

    def __init__(self, message):
        self.message = message


def ensure(expression, error_message):
    """Raise exception if the expression evaluates to `False`."""
    if not expression:
        raise MessageFormatError(error_message)
