# -*- coding: utf-8 -*-

"""
:Copyright: 2007-2016 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import unicode_literals
from datetime import datetime
from unittest import TestCase

from freezegun import freeze_time
from nose2.tools import params

from syslogmp import Facility, parse, Severity
from syslogmp.parser import MessageFormatError


CURRENT_YEAR = datetime.today().year


def create_long_data(length):
    data = b'<13>Sep  5 23:50:37 localhost '
    return pad_data(data, length, b'x')


def pad_data(value, width, fillbyte):
    """Append the fill byte to the end of the value until it has the
    requested width.
    """
    return value.ljust(width, fillbyte)


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

    def test_parse_message_just_not_too_long(self):
        data = create_long_data(1024)
        self.assertEqual(len(data), 1024)
        parse(data)

    @params(
        ( '<165>Nov 14 12:34:56 localhost foobar' ), # not a byte string
        (create_long_data(1025)                   ), # whole message too long
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

    @params(
        (2012),
        (2016),
        (2020),
    )
    def test_parse_leap_day_in_leap_year(self, current_year):
        data = b'<165>Feb 29 19:56:43 localhost foobar'
        fake_date = '{:d}-01-01'.format(current_year)
        expected_timestamp = datetime(current_year, 2, 29, 19, 56, 43)

        with freeze_time(fake_date):
            actual = parse(data)

        self.assertEqual(actual.timestamp, expected_timestamp)

    @params(
        (1900),
        (2015),
        (2017),
        (2018),
    )
    def test_parse_leap_day_in_non_leap_year(self, current_year):
        data = b'<165>Feb 29 19:56:43 localhost foobar'
        fake_date = '{:d}-01-01'.format(current_year)

        with self.assertRaises(MessageFormatError):
            with freeze_time(fake_date):
                parse(data)
