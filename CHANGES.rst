Changelog
=========


Version 0.4
-----------

Unreleased

- Removed support for Python versions 3.6.

- Turn namedtuples ``Message`` and ``PriorityValue`` into dataclasses.


Version 0.3
-----------

Released 2021-03-03

- Removed support for end-of-life Python versions 2.7, 3.3, 3.4, and
  3.5.

- Added support for Python 3.6, 3.7, 3.8, and 3.9.


Version 0.2.2
-------------

Released 2016-03-01

- Fixed ``datetime.strptime`` failing on February 29th. (Tests introduce
  a test dependency on FreezeGun).


Version 0.2.1
-------------

Released 2015-09-08

- Added missing files to distribution.


Version 0.2
-----------

Released 2015-09-07

- Data is required to be a byte string.

- Raise custom exception on message parsing errors instead of using
  assertions.

- Raise exception if message is too long instead of truncating and
  processing it.


Version 0.1.1
-------------

Released 2015-08-10

- Fixed packaging issue.


Version 0.1
-----------

Released 2015-08-10

- first official release
