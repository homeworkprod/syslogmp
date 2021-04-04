syslogmp
========

A parser for BSD syslog protocol (RFC 3164) messages

This library was extracted from syslog2IRC_.


Requirements
------------

- Python 3.7+


Installation
------------

Install this package via pip_:

.. code:: sh

    $ pip install syslogmp


Usage
-----

To parse a syslog message:

.. code:: python

    from syslogmp import parse

    # Parse data (usually received via network).
    message = parse(data)

    # Let's see what we've got here.
    print(message.facility)
    print(message.facility.description)
    print(message.severity)
    print(message.timestamp)
    print(message.hostname)
    print(message.message)


Further Reading
---------------

For more information, see `RFC 3164`_, "The BSD syslog Protocol".

Please note that there is `RFC 5424`_, "The Syslog Protocol", which
obsoletes `RFC 3164`_. This package, however, only implements the
latter.


.. _syslog2IRC: http://homework.nwsnet.de/releases/c474/#syslog2irc
.. _pip:        http://www.pip-installer.org/
.. _RFC 3164:   http://tools.ietf.org/html/rfc3164
.. _RFC 5424:   http://tools.ietf.org/html/rfc5424


:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
