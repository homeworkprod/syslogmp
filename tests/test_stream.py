"""
:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from syslogmp.stream import Stream


LETTERS = b'abcdefghijklmnopqrstuvwxyz'


@pytest.mark.parametrize(
    'data, n, expected',
    [
        (LETTERS,                0, b''                          ),
        (LETTERS,                1, b'a'                         ),
        (LETTERS,                2, b'ab'                        ),
        (LETTERS, len(LETTERS)    , b'abcdefghijklmnopqrstuvwxyz'),
        (LETTERS, len(LETTERS) + 1, b'abcdefghijklmnopqrstuvwxyz'),
    ],
)
def test_read(data, n, expected):
    stream = Stream(data)
    assert stream.read(n) == expected


def test_read_with_negative_length():
    stream = Stream(LETTERS)

    with pytest.raises(ValueError):
        stream.read(-1)


@pytest.mark.parametrize(
    'data, stop_character, expected',
    [
        (b'abcdef', b'a', b''      ),
        (b'abcdef', b'b', b'a'     ),
        (b'abcdef', b'c', b'ab'    ),
        (b'abcdef', b'z', b'abcdef'),  # Stop character not in data; return everything.
    ],
)
def test_read_until(data, stop_character, expected):
    stream = Stream(data)
    assert stream.read_until(stop_character) == expected


def test_read_until_drops_stop_character():
    stream = Stream(b'abcdef')

    until = stream.read_until(b'd')
    assert until == b'abc'

    remainder = stream.read_remainder()
    assert remainder == b'ef'


@pytest.mark.parametrize(
    'data, stop_character, expected',
    [
        (b'abcdef', b'a', b'a'     ),
        (b'abcdef', b'b', b'ab'    ),
        (b'abcdef', b'c', b'abc'   ),
        (b'abcdef', b'z', b'abcdef'),  # Stop character not in data; return everything.
    ],
)
def test_read_until_inclusive(data, stop_character, expected):
    stream = Stream(data)
    assert stream.read_until_inclusive(stop_character) == expected


def test_read_remainder_without_other_reads():
    stream = Stream(LETTERS)
    assert stream.read_remainder() == LETTERS


def test_read_remainder_after_other_reads():
    stream = Stream(LETTERS)
    stream.read(20)
    assert stream.read_remainder() == b'uvwxyz'
