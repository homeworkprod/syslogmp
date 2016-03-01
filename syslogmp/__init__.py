# -*- coding: utf-8 -*-

"""
syslogmp
~~~~~~~~

:Copyright: 2007-2016 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from .facility import Facility
from .message import Message
from .parser import Parser
from .severity import Severity


def parse(data):
    """Parse data and return syslog message."""
    return Parser.parse(data)
