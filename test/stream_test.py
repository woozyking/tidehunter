#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import sys
import os

from techies import Queue, StateCounter

target_path = os.path.join(os.path.dirname(__file__), '..', 'tidehunter')
sys.path.append(target_path)

# Test Targets
from stream import Hunter


class HunterTest(unittest.TestCase):

    def _conf(self):
        self.hunter_conf = {
            'url': 'https://httpbin.org/stream/20',
            'limit': 5,
            'delimiter': '\n',
            'timeout': 30
        }

    def setUp(self):
        self.sc_key = 'test_sc'
        self.sc = StateCounter(key=self.sc_key, host='localhost', port=6379,
                               db=0)
        self.q_key = 'test_q'
        self.q = Queue(key=self.q_key, host='localhost', port=6379, db=0)

        self._conf()  # load in the hunter_conf
        self.h = Hunter(self.hunter_conf, self.sc, self.q)

    def test_tide_on(self):
        self.h.tide_on()
        self.assertEqual(self.sc.get_total(), 5)

        # test the case of on-the-fly limit adjustment
        self.sc.conn.hset(self.sc_key, 'total', 0)
        self.h.tide_on(limit=10)
        self.assertEqual(self.sc.get_total(), 10)

    def tearDown(self):
        self.sc.conn.delete(self.sc_key)
        self.q.conn.delete(self.q_key)

        try:
            self.h.conn.close()
        except:  # pragma: no cover
            pass


class HunterTestBasicAuth(unittest.TestCase):

    # TODO: find a stream with BASIC Auth requirement to test
    # atm just basic auth without streaming
    def setUp(self):
        self.sc_key = 'test_sc'
        self.sc = StateCounter(key=self.sc_key, host='localhost', port=6379,
                               db=0)
        self.q_key = 'test_q'
        self.q = Queue(key=self.q_key, host='localhost', port=6379, db=0)

        conf = {
            'url': 'http://httpbin.org/hidden-basic-auth/user/passwd',
            'user': 'woozyking',
            'pass': 'kingwoozy'
        }
        self.h = Hunter(conf, self.sc, self.q)

    def test_tide_on(self):
        actual = self.h.tide_on()
        expected = 404
        self.assertEqual(actual, expected)

    def tearDown(self):
        self.sc.conn.delete(self.sc_key)
        self.q.conn.delete(self.q_key)

        try:
            self.h.conn.close()
        except:  # pragma: no cover
            pass


class HunterTestOAuth(HunterTest):

    def _conf(self):
        oauth_config = {
            'consumer_key': os.environ['TWITTER_CONSUMER_KEY'],
            'consumer_secret': os.environ['TWITTER_CONSUMER_SECRET'],
            'token_key': os.environ['TWITTER_TOKEN_KEY'],
            'token_secret': os.environ['TWITTER_TOKEN_SECRET']
        }

        self.hunter_conf = {
            'url': 'https://stream.twitter.com/1.1/statuses/sample.json',
            'oauth': oauth_config,
            'limit': 5,
            'timeout': 30
        }


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
