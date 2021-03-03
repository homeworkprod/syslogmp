"""
syslogmp.message
~~~~~~~~~~~~~~~~

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from collections import namedtuple


Message = namedtuple('Message', 'facility severity timestamp hostname message')
