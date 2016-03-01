# -*- coding: utf-8 -*-

"""
syslogmp.severity
~~~~~~~~~~~~~~~~~

Names and numerical codes as seen in `RFC 3164`_.

.. _RFC 3164: http://tools.ietf.org/html/rfc3164


:Copyright: 2007-2016 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from enum import Enum, unique


@unique
class Severity(Enum):
    emergency = 0
    alert = 1
    critical = 2
    error = 3
    warning = 4
    notice = 5
    informational = 6
    debug = 7
