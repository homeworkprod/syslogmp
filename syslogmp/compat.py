# -*- coding: utf-8 -*-

"""
syslogmp.compat
~~~~~~~~~~~~~~~

Python 2/3 compatibility


:Copyright: 2007-2016 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from sys import version_info


PYTHON3 = version_info[0] == 3


if PYTHON3:
    binary_type = bytes
else:
    binary_type = str
