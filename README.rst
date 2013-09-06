TideHunter
==========

HTTP streaming toolbox with flow control, written in Python.

|Build Status| |Coverage Status| |Downloads|

Background
----------

This project was born for a need in my day time job at Addictive
Mobility (Addictive Tech Corp.). Before this project was open sourced,
it went through two major overhauls. I briefly mentioned the techniques
I used in previous versions in a `blog
post <http://runzhou.li/blog/2013/07/02/tame-py-curl/>`__.

Highlights
----------

-  Accurate quota limit - total control over your stream quota.
-  An instant off switch - when sht hits the fan and you don't want to
   crash your process.
-  Redis backed control tools - semi-persisted, fast, and scalable.
-  Core mechanisms based on the solid cURL and PycURL - inherits the
   built-in goodness (gzip support and more).
-  OAuth support based on python-oauth2 - see `this
   demo <https://github.com/woozyking/tidehunter/blob/master/demo/five_tweets.py>`__
   in action.

Installation
------------

.. code:: bash

    $ pip install tidehunter

Or to update:

.. code:: bash

    $ pip install tidehunter --upgrade

Note: the package will install all Python dependencies for you. However
you need to have both cURL (the headers from dev package are also
required for PycURL) and Redis installed.

Usage
-----

Example 1 (with limit):
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from tidehunter.stream import StateCounter, Queue, Hunter

    # The state machine and record counter (state counter)
    sc = StateCounter(key='demo_sc', host='localhost', port=6379, db=0)

    # The data queue
    q = Queue(key='demo_q', host='localhost', port=6379, db=0)

    # The Hunter!
    conf = {
        'url': 'https://httpbin.org/stream/100',
        'limit': 5,  # desired limit
        'delimiter': '\n'
    }
    h = Hunter(conf=conf, sc=sc, q=q)

    # Start streaming
    h.tide_on()

    # Consume the data which should be in the data queue now
    while len(q):
        print q.get()  # profit x 5

    # You can re-use the same Hunter object, and add a one-time limit
    h.tide_on(limit=1)  # this time we only want one record

    assert len(q) == 1  # or else there's a bug, create an issue!

    print q.get()  # more profit

Example 2 (without limit):
~~~~~~~~~~~~~~~~~~~~~~~~~~

Assume you have a process running the following code:

.. code:: python

    from tidehunter.stream import StateCounter, Queue, Hunter

    # The state machine and record counter (state counter)
    sc = StateCounter(key='demo_sc', host='localhost', port=6379, db=0)

    # The data queue
    q = Queue(key='demo_q', host='localhost', port=6379, db=0)

    # The Hunter!
    conf = {'url': 'https://some.forever.streaming.api.endpoint'}
    h = Hunter(conf=conf, sc=sc, q=q)

    # Start streaming, FOREVA
    h.tide_on()

You can delegate the responsibility of data consumption and stream
control to another process:

.. code:: python

    from tidehunter.stream import StateCounter, Queue

    # The SAME state machine and record counter (state counter)
    sc = StateCounter(key='demo_sc', host='localhost', port=6379, db=0)

    # The SAME data queue
    q = Queue(key='demo_q', host='localhost', port=6379, db=0)

    while sc.started():
        data = q.get()  # dequeue and
        # ...do something with data

        if SHT_HITS_THE_FAN:
            sc.stop()  # instant off switch, end of while loop, as well as the process above

See `demo <https://github.com/woozyking/tidehunter/tree/master/demo>`__
for more examples.

Test (Unit Tests)
-----------------

The tests are done through Travis-CI already.

However, running the full test within your local environment is just
three lines, provided that you have Redis installed and running:

.. code:: bash

    $ pip install -r requirements.txt
    $ pip install -r test_requirements.txt
    $ nosetests --with-coverage --cover-package=tidehunter

Documentation
-------------

Coming up very soon!

License
-------

The MIT License (MIT). See the full
`LICENSE <https://github.com/woozyking/tidehunter/blob/master/LICENSE>`__.

.. |Build Status| image:: https://travis-ci.org/woozyking/tidehunter.png?branch=master
   :target: https://travis-ci.org/woozyking/tidehunter
.. |Coverage Status| image:: https://coveralls.io/repos/woozyking/tidehunter/badge.png?branch=master
   :target: https://coveralls.io/r/woozyking/tidehunter?branch=master
.. |Downloads| image:: https://pypip.in/d/tidehunter/badge.png
   :target: https://pypi.python.org/pypi/tidehunter
