TideHunter
==========

HTTP streaming toolbox with flow control, written in Python.

.. image:: https://travis-ci.org/amoa/tidehunter.png?branch=master
        :target: https://travis-ci.org/amoa/tidehunter

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

Note: the package will install all Python dependencies for you. However you need to have redis-server installed by yourself.

Usage
-----

See demo_.

.. _demo: https://github.com/amoa/tidehunter/tree/master/demo

Documentation
-------------

Coming up very soon!

License
-------

Copyright (c) 2013 Addictive Tech Corp., under The MIT License (MIT). See the full LICENSE_.

.. _LICENSE: https://github.com/amoa/tidehunter/blob/master/LICENSE
