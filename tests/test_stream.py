# -*- coding: utf-8 -*-

"""
:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import unicode_literals
from unittest import TestCase

from nose2.tools import params

from syslogmp.stream import Stream


LETTERS = 'abcdefghijklmnopqrstuvwxyz'


class StreamTestCase(TestCase):

    @params(
        (LETTERS,                0, ''                          ),
        (LETTERS,                1, 'a'                         ),
        (LETTERS,                2, 'ab'                        ),
        (LETTERS, len(LETTERS)    , 'abcdefghijklmnopqrstuvwxyz'),
        (LETTERS, len(LETTERS) + 1, 'abcdefghijklmnopqrstuvwxyz'),
    )
    def test_read(self, data, n, expected):
        stream = Stream(data)
        actual = stream.read(n)
        self.assertEqual(actual, expected)

    def test_read_with_negative_length(self):
        stream = Stream(LETTERS)

        with self.assertRaises(ValueError):
            stream.read(-1)

    @params(
        ('abcdef', 'a', ''      ),
        ('abcdef', 'b', 'a'     ),
        ('abcdef', 'c', 'ab'    ),
        ('abcdef', 'z', 'abcdef'),  # Stop character not in data; return everything.
    )
    def test_read_until(self, data, stop_character, expected):
        stream = Stream(data)
        actual = stream.read_until(stop_character)
        self.assertEqual(actual, expected)

    @params(
        ('abcdef', 'a', 'a'     ),
        ('abcdef', 'b', 'ab'    ),
        ('abcdef', 'c', 'abc'   ),
        ('abcdef', 'z', 'abcdef'),  # Stop character not in data; return everything.
    )
    def test_read_until_inclusive(self, data, stop_character, expected):
        stream = Stream(data)
        actual = stream.read_until_inclusive(stop_character)
        self.assertEqual(actual, expected)

    def test_read_remainder_without_other_reads(self):
        stream = Stream(LETTERS)
        actual = stream.read_remainder()
        self.assertEqual(actual, LETTERS)

    def test_read_remainder_after_other_reads(self):
        stream = Stream(LETTERS)
        stream.read(20)

        actual = stream.read_remainder()
        self.assertEqual(actual, 'uvwxyz')
