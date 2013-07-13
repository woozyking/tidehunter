#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json

target_path = os.path.join(os.path.dirname(__file__), '..', 'tidehunter')
sys.path.append(target_path)

# Test Targets
from stream import StateCounter, Queue, Hunter


if __name__ == '__main__':
    # Init StateCounter
    key_sc = 'demo_sc'
    sc = StateCounter(key=key_sc, host='localhost', port=6379, db=0)

    # Init Queue
    key_q = 'demo_q'
    q = Queue(key=key_q, host='localhost', port=6379, db=0)

    # Init Hunter with conf
    conf = {
        'url': 'https://stream.twitter.com/1.1/statuses/sample.json',
        'oauth': {
            'consumer_key': '5wgrdrBSvbfXBuopdGgY9Q',
            'consumer_secret': 'GKtn1buVpvynFlDsFmTl8tRJmnbVsSmULRGUbEMNU',
            'token_key': '974720028-xyfPogLX9ynU05xQYwYNiPtiZengdpdYbyxnpXBI',
            'token_secret': 'rFDXV79FIG3881oxYT3XpYKEXi22bk74DaM7poYR0g'
        },
        'limit': 5
    }
    h = Hunter(conf=conf, sc=sc, q=q)

    try:
        http_code = h.tide_on()

        assert http_code == 200

        while len(q):
            data = json.loads(q.get())

            if data:
                print(data)
    except:
        raise
    finally:
        # Some cleanup
        sc.conn.delete(key_sc)
        q.conn.delete(key_q)
