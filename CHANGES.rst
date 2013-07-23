Changelog
---------

0.1.7 (2013-07-22)
~~~~~~~~~~~~~~~~~~

- Minor: Massive update to README.rst
- Minor: Fixed PyPi rendering of long description.


0.1.5 (2013-07-22)
~~~~~~~~~~~~~~~~~~

- NEW: Hunter.tide_on() now accepts an optional limit parameter for on the fly limit adjustment. The adjustment is not permanent, meaning if you want to reuse the same Hunter object, the old limit (or default None) is in effect.
- Major: Fixed a potential issue of Hunter puts in more records than desired limit.
- Minor: Added temp Basic Auth test case (no stream, need to find a better source).


0.1.3 (2013-07-13)
~~~~~~~~~~~~~~~~~~

- Major: use the great httpbin.org (by Kenneth Reitz) for unit test now.
- Major: auth (oauth or basic) is no longer required, as long as the target stream server supports access without auth.


0.1.2 (2013-07-12)
~~~~~~~~~~~~~~~~~~

- Minor: include CHANGES (changelog) to be shown on PyPi.
- Minor: use with statement to open files for setup.py.
- Minor: added the first `demo <https://github.com/amoa/tidehunter/tree/master/demo>`_.


0.1.1 (2013-07-12)
~~~~~~~~~~~~~~~~~~

- Minor: clean up setup.py to ensure requirements are installed/updated.


0.1.0 (2013-07-12)
~~~~~~~~~~~~~~~~~~

- Initial release
