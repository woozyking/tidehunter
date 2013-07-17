TideHunter
==========

HTTP streaming toolbox with flow control, written in Python.

.. image:: https://travis-ci.org/amoa/tidehunter.png?branch=master
        :target: https://travis-ci.org/amoa/tidehunter

.. image:: https://coveralls.io/repos/amoa/tidehunter/badge.png?branch=master
        :target: https://coveralls.io/r/amoa/tidehunter?branch=master

.. image:: https://pypip.in/d/tidehunter/badge.png?
        :target: https://pypi.python.org/pypi/tidehunter

Highlights
----------

- Stream data queue, state machine, and record counter based on Redis and redis-py.
- Based on the solid cURL and PycURL.
- OAuth support based on python-oauth2.

Installation
------------

.. code-block:: bash

    $ pip install tidehunter

Or to update:

.. code-block:: bash

    $ pip install tidehunter --upgrade

Note: the package will install all Python dependencies for you. However you need to have Redis installed and running.

Usage
-----

See demo_.

.. _demo: https://github.com/amoa/tidehunter/tree/master/demo

Test (Unit Tests)
-----------------

The tests are done through Travis-CI already.

However, running the full test within your local environment is just three lines, provided that you have Redis installed and running:

.. code-block:: bash

    $ pip install -r requirements.txt
    $ pip install -r test_requirements.txt
    $ nosetests --with-coverage --cover-package=tidehunter

Documentation
-------------

Coming up very soon!

License
-------

Copyright (c) 2013 Addictive Tech Corp., under The MIT License (MIT). See the full LICENSE_.

.. _LICENSE: https://github.com/amoa/tidehunter/blob/master/LICENSE
