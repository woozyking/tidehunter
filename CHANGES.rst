Changelog
---------

0.1.9 (2013-12-24)
~~~~~~~~~~~~~~~~~~

-  ``PyCurl`` and ``Redis`` Python libraries bumped to the latest
   versions.
-  ``Queue`` now is **almost** Python Queue compatible (in a complaint
   free fashion), with the exception of ``Queue.full`` which always
   returns ``False``; ``Queue.task_done`` and ``Queue.join`` do nothing.
-  NEW: Both ``Queue`` and ``StateCounter`` now have a ``clear`` method
   which performs a Redis ``DEL`` command on the said key and
   reinitialize based on each class's ``initialize`` method.

0.1.8 (2013-10-02)
~~~~~~~~~~~~~~~~~~

-  Added alias methods ``put_nowait()`` and ``get_nowait()`` and other
   place holders to map the Python built-in Queue interfaces.
-  Added ``rstgen`` shell script for Markdown to reStructuredText. To
   use, run ``$ source rstgen`` in the root folder.
-  Credentials involved in unit tests and demo are now using environment
   variables.

0.1.7 (2013-07-22)
~~~~~~~~~~~~~~~~~~

-  Massive update to README.rst
-  Fixed PyPi rendering of long description.

0.1.5 (2013-07-22)
~~~~~~~~~~~~~~~~~~

-  NEW: ``Hunter.tide_on()`` now accepts an optional limit parameter for
   on the fly limit adjustment. The adjustment is not permanent, meaning
   if you want to reuse the same Hunter object, the old limit (or
   default None) is in effect.
-  Fixed a potential issue of Hunter puts in more records than desired
   limit.
-  Added temp Basic Auth test case (no stream, need to find a better
   source).

0.1.3 (2013-07-13)
~~~~~~~~~~~~~~~~~~

-  Use the great httpbin.org (by Kenneth Reitz) for unit test now.
-  Auth (oauth or basic) is no longer required, as long as the target
   stream server supports access without auth.

0.1.2 (2013-07-12)
~~~~~~~~~~~~~~~~~~

-  Include CHANGES (changelog) to be shown on PyPi.
-  Use with statement to open files for setup.py.
-  Added the first
   `demo <https://github.com/amoa/tidehunter/tree/master/demo>`__.

0.1.1 (2013-07-12)
~~~~~~~~~~~~~~~~~~

-  Clean up setup.py to ensure requirements are installed/updated.

0.1.0 (2013-07-12)
~~~~~~~~~~~~~~~~~~

-  Initial release
