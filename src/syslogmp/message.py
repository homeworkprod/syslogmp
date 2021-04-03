"""
syslogmp.message
~~~~~~~~~~~~~~~~

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from dataclasses import dataclass
from datetime import datetime

from .facility import Facility
from .severity import Severity


@dataclass(frozen=True)
class Message:
    facility: Facility
    severity: Severity
    timestamp: datetime
    hostname: str
    message: bytes
