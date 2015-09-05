# -*- coding: utf-8 -*-

"""
syslogmp.parser
~~~~~~~~~~~~~~~

A message consists of three parts:

- PRI (facility, severity)
- HEADER (timestamp, hostname/IP address)
- MSG (additional information, text)

For more information, see `RFC 3164`_, "The BSD syslog Protocol".

Please note that there is `RFC 5424`_, "The Syslog Protocol", which
obsoletes `RFC 3164`_. This package, however, only implements the
latter.

.. _RFC 3164: http://tools.ietf.org/html/rfc3164
.. _RFC 5424: http://tools.ietf.org/html/rfc5424


:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from collections import namedtuple
from datetime import datetime

from .facility import Facility
from .message import Message
from .severity import Severity
from .stream import Stream


class Parser(object):
    """Parse syslog messages."""

    @classmethod
    def parse(cls, data):
        parser = cls(data)

        priority_value = parser._parse_pri_part()
        timestamp, hostname = parser._parse_header_part()
        message = parser._parse_msg_part()

        return Message(priority_value.facility, priority_value.severity,
                       timestamp, hostname, message)

    def __init__(self, data):
        max_bytes = 1024  # as stated by the RFC
        self.stream = Stream(data[:max_bytes])

    def _parse_pri_part(self):
        """Extract facility and severity from the PRI part."""
        pri_part = self.stream.read_until_inclusive('>')

        return PriorityValue.from_pri_part(pri_part)

    def _parse_header_part(self):
        """Extract timestamp and hostname from the HEADER part."""
        timestamp = self._parse_timestamp()
        hostname = self._parse_hostname()
        return timestamp, hostname

    def _parse_timestamp(self):
        """Parse timestamp into a `datetime` instance."""
        timestamp_str = self.stream.read(15)

        nothing = self.stream.read_until(' ')  # Advance to next part.
        ensure(nothing == '',
               'Timestamp must be followed by a space character.')

        timestamp = datetime.strptime(timestamp_str, '%b %d %H:%M:%S')
        timestamp = timestamp.replace(year=datetime.today().year)
        return timestamp

    def _parse_hostname(self):
        return self.stream.read_until(' ')

    def _parse_msg_part(self):
        return self.stream.read_remainder()


class MessageFormatError(ValueError):
    """Raised when data does not match the expected message structure."""

    def __init__(self, message):
        self.message = message


def ensure(expression, error_message):
    """Raise exception if the expression evaluates to `False`."""
    if not expression:
        raise MessageFormatError(error_message)


class PriorityValue(namedtuple('PriorityValue', 'facility severity')):

    @classmethod
    def from_pri_part(cls, pri_part):
        """Create instance from PRI part."""
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

        facility = Facility(facility_id)
        severity = Severity(severity_id)

        return cls(facility, severity)
