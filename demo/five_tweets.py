#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json

from techies import StateCounter, Queue

# Take the following two lines out if you installed tidehunter through pip
target_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(target_path)

from tidehunter import Hunter


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
            'consumer_key': os.environ['TWITTER_CONSUMER_KEY'],
            'consumer_secret': os.environ['TWITTER_CONSUMER_SECRET'],
            'token_key': os.environ['TWITTER_TOKEN_KEY'],
            'token_secret': os.environ['TWITTER_TOKEN_SECRET']
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
