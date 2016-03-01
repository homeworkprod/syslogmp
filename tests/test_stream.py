# -*- coding: utf-8 -*-

"""
:Copyright: 2007-2016 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import unicode_literals
from unittest import TestCase

from nose2.tools import params

from syslogmp.stream import Stream


LETTERS = b'abcdefghijklmnopqrstuvwxyz'


class StreamTestCase(TestCase):

    @params(
        (LETTERS,                0, b''                          ),
        (LETTERS,                1, b'a'                         ),
        (LETTERS,                2, b'ab'                        ),
        (LETTERS, len(LETTERS)    , b'abcdefghijklmnopqrstuvwxyz'),
        (LETTERS, len(LETTERS) + 1, b'abcdefghijklmnopqrstuvwxyz'),
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
        (b'abcdef', b'a', b''      ),
        (b'abcdef', b'b', b'a'     ),
        (b'abcdef', b'c', b'ab'    ),
        (b'abcdef', b'z', b'abcdef'),  # Stop character not in data; return everything.
    )
    def test_read_until(self, data, stop_character, expected):
        stream = Stream(data)
        actual = stream.read_until(stop_character)
        self.assertEqual(actual, expected)

    def test_read_until_drops_stop_character(self):
        stream = Stream(b'abcdef')

        until = stream.read_until(b'd')
        self.assertEqual(until, b'abc')

        remainder = stream.read_remainder()
        self.assertEqual(remainder, b'ef')

    @params(
        (b'abcdef', b'a', b'a'     ),
        (b'abcdef', b'b', b'ab'    ),
        (b'abcdef', b'c', b'abc'   ),
        (b'abcdef', b'z', b'abcdef'),  # Stop character not in data; return everything.
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
        self.assertEqual(actual, b'uvwxyz')
