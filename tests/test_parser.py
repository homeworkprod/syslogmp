# -*- coding: utf-8 -*-

"""
:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import unicode_literals
from datetime import datetime
from unittest import TestCase

from nose2.tools import params

from syslogmp import Facility, parse, Severity
from syslogmp.parser import MessageFormatError


CURRENT_YEAR = datetime.today().year


class ParseTestCase(TestCase):

    @params(
        (
            # Example 1 from RFC 3164.
            b'<34>Oct 11 22:14:15 mymachine su: \'su root\' failed for lonvick on /dev/pts/8',
            Facility.security4,
            'security/authorization messages',
            Severity.critical,
            datetime(CURRENT_YEAR, 10, 11, 22, 14, 15),
            'mymachine',
            b'su: \'su root\' failed for lonvick on /dev/pts/8',
        ),
        (
            # Example 2 from RFC 3164.
            b'<13>Feb  5 17:32:18 10.0.0.99 Use the BFG!',
            Facility.user,
            'user-level messages',
            Severity.notice,
            datetime(CURRENT_YEAR, 2, 5, 17, 32, 18),
            '10.0.0.99',
            b'Use the BFG!',
        ),
        (
            # Example 3 from RFC 3164.
            # Note that the HOSTNAME and MSG fields in this example are not
            # consistent with what the RFC defines.
            b'<165>Aug 24 05:34:00 CST 1987 mymachine myproc[10]: %% It\'s time to make the do-nuts.  %%  Ingredients: Mix=OK, Jelly=OK # Devices: Mixer=OK, Jelly_Injector=OK, Frier=OK # Transport: Conveyer1=OK, Conveyer2=OK # %%',
            Facility.local4,
            'local use 4 (local4)',
            Severity.notice,
            datetime(CURRENT_YEAR, 8, 24, 5, 34, 0),
            'CST',
            b'1987 mymachine myproc[10]: %% It\'s time to make the do-nuts.  %%  Ingredients: Mix=OK, Jelly=OK # Devices: Mixer=OK, Jelly_Injector=OK, Frier=OK # Transport: Conveyer1=OK, Conveyer2=OK # %%',
        ),
            # Example 4 from RFC 3164 (included for the sake of completeness).
            # This cannot be parsed because the format of the TIMESTAMP field
            # is invalid.
            #'<0>1990 Oct 22 10:52:01 TZ-6 scapegoat.dmz.example.org 10.1.2.3 sched[0]: That\'s All Folks!',
        (
            # Example 5 from RFC 3164.
            b'<0>Oct 22 10:52:12 scapegoat 1990 Oct 22 10:52:01 TZ-6 scapegoat.dmz.example.org 10.1.2.3 sched[0]: That\'s All Folks!',
            Facility.kernel,
            'kernel messages',
            Severity.emergency,
            datetime(CURRENT_YEAR, 10, 22, 10, 52, 12),
            'scapegoat',
            b'1990 Oct 22 10:52:01 TZ-6 scapegoat.dmz.example.org 10.1.2.3 sched[0]: That\'s All Folks!',
        ),
    )
    def test_parse(
            self,
            data,
            expected_facility,
            expected_facility_description,
            expected_severity,
            expected_timestamp,
            expected_hostname,
            expected_message):
        """Test parsing of a syslog message."""
        actual = parse(data)

        self.assertEqual(actual.facility, expected_facility)
        self.assertEqual(actual.facility.description, expected_facility_description)
        self.assertEqual(actual.severity, expected_severity)
        self.assertEqual(actual.timestamp, expected_timestamp)
        self.assertEqual(actual.hostname, expected_hostname)
        self.assertEqual(actual.message, expected_message)

    @params(
        ( '<165>Nov 14 12:34:56 localhost foobar' ), # not a byte string
        (b'165>Nov 14 12:34:56 localhost foobar'  ), # PRI part not starting with '<'
        (b'<165 Nov 14 12:34:56 localhost foobar' ), # PRI part not ending with '>'
        (b'<>Nov 14 12:34:56 localhost foobar'    ), # priority value too short
        (b'<0123>Nov 14 12:34:56 localhost foobar'), # priority value too long
        (b'<abc>Nov 14 12:34:56 localhost foobar' ), # priority value not a number
        (b'<165>Nov 14 12:34:56localhost foobar'  ), # no space after timestamp

        # Example 4 from RFC 3164
        # Cannot be parsed because TIMESTAMP field format is invalid.
        (b'<0>1990 Oct 22 10:52:01 TZ-6 scapegoat.dmz.example.org 10.1.2.3 sched[0]: That\'s All Folks!'),
    )
    def test_parse_erroneous_message(self, data):
        with self.assertRaises(MessageFormatError):
            parse(data)
