syslogmp Changelog
==================


Version 0.2.2
-------------

Released March 1, 2016

- Fixed `datetime.strptime` failing on February 29th. (Tests introduce
  a test depedency on FreezeGun).


Version 0.2.1
-------------

Released September 8, 2015

- Added missing files to distribution.


Version 0.2
-----------

Released September 7, 2015

- Data is required to be a byte string.
- Raise custom exception on message parsing errors instead of using
  assertions.
- Raise exception if message is too long instead of truncating and
  processing it.


Version 0.1.1
-------------

Released August 10, 2015

- Fixed packaging issue.


Version 0.1
-----------

Released August 10, 2015

- first official release
