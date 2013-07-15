#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json

# Take the following two lines out if you installed tidehunter through pip
target_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(target_path)

from tidehunter.stream import StateCounter, Queue, Hunter


if __name__ == '__main__':
    # Init StateCounter
    key_sc = 'demo_sc'
    sc = StateCounter(key=key_sc, host='localhost', port=6379, db=0)

    # Init Queue
    key_q = 'demo_q'
    q = Queue(key=key_q, host='localhost', port=6379, db=0)

    # Init Hunter with conf
    conf = {
        'url': 'https://httpbin.org/stream/20',
        'limit': 5,  # desired limit, might go over
        'delimiter': '\n'
    }
    h = Hunter(conf=conf, sc=sc, q=q)

    for i in xrange(5):
        try:
            http_code = h.tide_on()

            assert http_code == 200
            print "Iteration " + str(i + 1) + ":\t",

            count = 0

            while len(q):
                data = json.loads(q.get())

                if data:
                    count += 1
                    print count,

            print
        except:
            raise
        finally:
            # Some cleanup
            sc.conn.delete(key_sc)
            q.conn.delete(key_q)
