# -*- coding: utf-8 -*-

"""
syslogmp.facility
~~~~~~~~~~~~~~~~~

Labels and numerical codes as seen in `RFC 3164`_.

.. _RFC 3164: http://tools.ietf.org/html/rfc3164


:Copyright: 2007-2016 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from enum import Enum, unique


@unique
class Facility(Enum):
    kernel = 0
    user = 1
    mail = 2
    system_daemons = 3
    security4 = 4
    internal = 5
    line_printer = 6
    network_news = 7
    uucp = 8
    clock9 = 9
    security10 = 10
    ftp = 11
    ntp = 12
    log_audit = 13
    log_alert = 14
    clock15 = 15
    local0 = 16
    local1 = 17
    local2 = 18
    local3 = 19
    local4 = 20
    local5 = 21
    local6 = 22
    local7 = 23

    @property
    def description(self):
        return DESCRIPTIONS[self.value]


DESCRIPTIONS = {
    0: 'kernel messages',
    1: 'user-level messages',
    2: 'mail system',
    3: 'system daemons',
    4: 'security/authorization messages',
    5: 'messages generated internally by syslogd',
    6: 'line printer subsystem',
    7: 'network news subsystem',
    8: 'UUCP subsystem',
    9: 'clock daemon',
    10: 'security/authorization messages',
    11: 'FTP daemon',
    12: 'NTP subsystem',
    13: 'log audit',
    14: 'log alert',
    15: 'clock daemon',
    16: 'local use 0 (local0)',
    17: 'local use 1 (local1)',
    18: 'local use 2 (local2)',
    19: 'local use 3 (local3)',
    20: 'local use 4 (local4)',
    21: 'local use 5 (local5)',
    22: 'local use 6 (local6)',
    23: 'local use 7 (local7)',
}
