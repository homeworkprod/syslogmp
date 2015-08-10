# -*- coding: utf-8 -*-

"""
syslogmp.parser
~~~~~~~~~~~~~~~

For more information, see `RFC 3164`_, "The BSD syslog Protocol".

Please note that there is `RFC 5424`_, "The Syslog Protocol", which
obsoletes `RFC 3164`_. syslog2IRC, however, only implements the latter.

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

        facility_id, severity_id = parser._parse_priority_value()
        facility = Facility(facility_id)
        severity = Severity(severity_id)
        timestamp = parser._parse_timestamp()
        hostname = parser._parse_hostname()
        message = ''.join(parser.data_iter)

        return Message(facility, severity, timestamp, hostname, message)

    def __init__(self, data):
        max_bytes = 1024  # as stated by the RFC
        self.data_iter = iter(data[:max_bytes])

    def _parse_priority_value(self):
        """Parse the priority value to extract facility and severity
        IDs.
        """
        start_delim = self._take_slice(1)
        assert start_delim == '<'

        priority_value = self._take_until('>')
        assert len(priority_value) in {1, 2, 3}

        facility_id, severity_id = divmod(int(priority_value), 8)
        return facility_id, severity_id

    def _parse_timestamp(self):
        """Parse timestamp into a `datetime` instance."""
        timestamp_str = self._take_slice(15)
        nothing = self._take_until(' ')  # Advance to next part.
        assert nothing == ''

        timestamp = datetime.strptime(timestamp_str, '%b %d %H:%M:%S')
        timestamp = timestamp.replace(year=datetime.today().year)
        return timestamp

    def _parse_hostname(self):
        return self._take_until(' ')

    def _take_until(self, value):
        return ''.join(takewhile(lambda c: c != value, self.data_iter))

    def _take_slice(self, n):
        return ''.join(islice(self.data_iter, n))
