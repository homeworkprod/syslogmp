"""
syslogmp.parser
~~~~~~~~~~~~~~~

A message consists of three parts:

- PRI (facility, severity)
- HEADER (timestamp, hostname/IP address)
- MSG (additional information, text)

Its length must not exceed 1024 bytes.

For more information, see `RFC 3164`_, "The BSD syslog Protocol".

Please note that there is `RFC 5424`_, "The Syslog Protocol", which
obsoletes `RFC 3164`_. This package, however, only implements the
latter.

.. _RFC 3164: http://tools.ietf.org/html/rfc3164
.. _RFC 5424: http://tools.ietf.org/html/rfc5424


:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple

from .facility import Facility
from .message import Message
from .severity import Severity
from .stream import Stream


MAX_MESSAGE_LENGTH: int = 1024


def parse(data: bytes) -> Message:
    """Parse a syslog message."""
    parser = _Parser(data)

    priority_value = parser._parse_pri_part()
    timestamp, hostname = parser._parse_header_part()
    message = parser._parse_msg_part()

    return Message(
        facility=priority_value.facility,
        severity=priority_value.severity,
        timestamp=timestamp,
        hostname=hostname,
        message=message,
    )


class _Parser:
    """Parse a syslog message."""

    def __init__(self, data: bytes) -> None:
        ensure(isinstance(data, bytes), 'Data must be a byte string.')

        ensure(
            len(data) <= MAX_MESSAGE_LENGTH,
            'Message must not be longer than 1024 bytes.',
        )

        self.stream = Stream(data)

    def _parse_pri_part(self) -> PriorityValue:
        """Extract facility and severity from the PRI part."""
        pri_part = self.stream.read_until_inclusive(b'>')
        return _create_priority_value_from_pri_part(pri_part)

    def _parse_header_part(self) -> Tuple[datetime, str]:
        """Extract timestamp and hostname from the HEADER part."""
        timestamp = self._parse_timestamp()

        # Advance to hostname.
        nothing = self.stream.read_until(b' ')
        ensure(
            nothing == b'', 'Timestamp must be followed by a space character.'
        )

        hostname = self._parse_hostname()

        return timestamp, hostname

    def _parse_timestamp(self) -> datetime:
        """Parse timestamp into a `datetime` instance."""
        timestamp_bytes = self.stream.read(15)
        timestamp_ascii = timestamp_bytes.decode('ascii')

        # Explicitly specify the current year to work around
        # `datetime.strptime` failing on February 29th if no year is
        # given ("ValueError: day is out of range for month") in which
        # case the (non-leap) year 1900 would be used.
        current_year = datetime.today().year
        timestamp_ascii_with_year = f'{current_year:d} {timestamp_ascii}'

        try:
            timestamp = datetime.strptime(
                timestamp_ascii_with_year, '%Y %b %d %H:%M:%S'
            )
        except ValueError as e:
            raise MessageFormatError(e)

        return timestamp

    def _parse_hostname(self) -> str:
        hostname_bytes = self.stream.read_until(b' ')
        return hostname_bytes.decode('ascii')

    def _parse_msg_part(self) -> bytes:
        return self.stream.read_remainder()


@dataclass(frozen=True)
class PriorityValue:
    facility: Facility
    severity: Severity


def _create_priority_value_from_pri_part(pri_part: bytes) -> PriorityValue:
    """Create priority value from PRI part."""
    ensure(len(pri_part) in {3, 4, 5}, 'PRI part must have 3, 4, or 5 bytes.')

    ensure(
        pri_part.startswith(b'<'),
        'PRI part must start with an opening angle bracket (`<`).',
    )

    ensure(
        pri_part.endswith(b'>'),
        'PRI part must end with a closing angle bracket (`>`).',
    )

    priority_value = pri_part[1:-1]

    try:
        priority_value_number = int(priority_value)
    except ValueError:
        raise MessageFormatError(
            "Priority value must be a number, but is '{priority_value}'."
        )

    facility_id, severity_id = divmod(priority_value_number, 8)

    facility = Facility(facility_id)
    severity = Severity(severity_id)

    return PriorityValue(facility=facility, severity=severity)


def ensure(expression: bool, error_message: str) -> None:
    """Raise exception if the expression evaluates to `False`."""
    if not expression:
        raise MessageFormatError(error_message)


class MessageFormatError(ValueError):
    """Raised when data does not match the expected message structure."""
