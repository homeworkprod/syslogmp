"""
syslogmp
~~~~~~~~

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from .facility import Facility
from .message import Message
from .parser import Parser
from .severity import Severity


VERSION = '0.3'


def parse(data):
    """Parse data and return syslog message."""
    return Parser.parse(data)
