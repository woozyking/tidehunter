tidehunter
==========

HTTP streaming with accurate flow control

Master branch: |Build Status|

**NOTE**: Not backward compatible with 0.x since 1.x.

Highlights
----------

-  Consumption limits, total control over your stream quota just on the
   client side.
-  Instant on/off switch and accurate consumption counter. Best used
   with `techies <https://github.com/woozyking/techies>`__.
-  Queue interface for scalable stream data consumption. Best used with
   `techies <https://github.com/woozyking/techies>`__.
-  Core mechanisms based on the solid
   `requests <https://github.com/kennethreitz/requests>`__ library,
   inherits all its goodness.

Installation
------------

.. code:: bash

    $ pip install tidehunter
    $ pip install tidehunter --upgrade

Usage
-----

Example 1 (with limit):
~~~~~~~~~~~~~~~~~~~~~~~

**NOTE**: when no external ``Queue`` or ``StateCounter`` supplied,
``Hunter`` uses the Python standard ``Queue`` and the builtin
``SimpleStateCounter`` respectively, which are usually enough for single
process designs and other simple cases.

.. code:: python

    from tidehunter import Hunter

    # The Hunter!
    h = Hunter(url='https://httpbin.org/stream/20')

    # Start streaming
    h.tide_on(limit=5)

    # Consume the data which should be in the data queue now
    while h.q.qsize():
        print(h.q.get())  # profit x 5

    # You can re-use the same Hunter object, with a difference limit
    r = h.tide_on(limit=1)  # this time we only want one record

    assert h.q.qsize() == 1  # or else there's a bug, create an issue!

    print(h.q.get())  # more profit

    # r is actually just a requests.Response object
    print(r.headers)
    print(r.status_code)
    # ... read up on requests library for more information

Example 2 (without limit):
~~~~~~~~~~~~~~~~~~~~~~~~~~

**NOTE**: this example uses ``techies`` and therefore requires Redis
installed.

Assume you have a process running the following code:

.. code:: python

    from techies import StateCounter, Queue
    from tidehunter import Hunter

    # The data queue
    q = Queue(key='demo_q', host='localhost', port=6379, db=0)

    # The state machine and record counter (state counter)
    sc = StateCounter(key='demo_sc', host='localhost', port=6379, db=0)

    # The Hunter!
    h = Hunter(url='SOME_ENDLESS_STREAM_LIKE_TWITTER_FIREHOSE', q=q, sc=sc)

    # Start streaming, FOREVA
    h.tide_on()

Then you delegate the flow control and data consumption to another/many
other processes such as:

.. code:: python

    from techies import StateCounter, Queue

    # The key is to have the SAME state counter
    sc = StateCounter(key='demo_sc', host='localhost', port=6379, db=0)

    # And the SAME data queue
    q = Queue(key='demo_q', host='localhost', port=6379, db=0)

    while sc.started:
        data = q.get()  # dequeue and
        # ...do something with data

        if SHT_HITS_THE_FAN:
            sc.stop()  # instant off switch
            # end of this loop, as well as the streaming process from above

    # If needed
    q.clear()
    sc.clear()

Example 3 (OAuth with Twitter Sample Firehose):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**NOTE**: this example requires ``requests_oauthlib``

.. code:: python

    import os
    import json
    from requests_oauthlib import OAuth1
    from tidehunter import Hunter

    url = 'https://stream.twitter.com/1.1/statuses/sample.json'
    auth = OAuth1(
        os.environ['TWITTER_CONSUMER_KEY'],
        os.environ['TWITTER_CONSUMER_SECRET'],
        os.environ['TWITTER_TOKEN_KEY'],
        os.environ['TWITTER_TOKEN_SECRET']
    )
    h = Hunter(url=url, q=q, auth=auth)
    r = h.tide_on(5)  # let's just get 5 for now

    print(r.status_code)
    print('')

    while h.q.qsize():
        print(json.loads(h.q.get()))
        print('')

You can find other authentications on `this requests
doc <http://docs.python-requests.org/en/latest/user/authentication/>`__.
In short, all you have to do is to pass the desired ``auth`` parameter
to ``Hunter``, like what you would do with ``requests``.

Test (Unit Tests)
=================

.. code:: bash

    $ pip install -r requirements.txt
    $ pip install -r test_requirements.txt
    $ nosetests --with-coverage --cover-package=tidehunter

License
=======

The MIT License (MIT). See the full
`LICENSE <https://github.com/woozyking/tidehunter/blob/master/LICENSE>`__.

.. |Build Status| image:: https://travis-ci.org/woozyking/tidehunter.png?branch=master
   :target: https://travis-ci.org/woozyking/tidehunter
