#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import random
import string

import sys
import os

target_path = os.path.join(os.path.dirname(__file__), '..', 'tidehunter')
sys.path.append(target_path)

# Test Targets
from stream import StateCounter, Queue, Hunter


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
            'consumer_key': '5wgrdrBSvbfXBuopdGgY9Q',
            'consumer_secret': 'GKtn1buVpvynFlDsFmTl8tRJmnbVsSmULRGUbEMNU',
            'token_key': '974720028-xyfPogLX9ynU05xQYwYNiPtiZengdpdYbyxnpXBI',
            'token_secret': 'rFDXV79FIG3881oxYT3XpYKEXi22bk74DaM7poYR0g'
        }

        self.hunter_conf = {
            'url': 'https://stream.twitter.com/1.1/statuses/sample.json',
            'oauth': oauth_config,
            'limit': 5,
            'timeout': 30
        }


class QueueTest(unittest.TestCase):

    def setUp(self):
        self.key = "test_q"
        self.q = Queue(key=self.key, host='localhost', port=6379, db=0)
        self.q.conn.delete(self.key)

    def test__len__(self):
        # When empty
        self.assertEqual(len(self.q), 0)

        # When not empty
        length = random.randint(1, 32)

        for i in xrange(length):
            self.q.conn.rpush(self.key, i)

        self.assertEqual(len(self.q), length)

    def test_put(self):
        val = ''.join(random.choice(string.ascii_uppercase + string.digits)
                      for x in range(32))
        self.assertTrue(self.q.put(val))
        self.assertEqual(self.q.conn.lpop(self.key), val)

    def test_get(self):
        # When empty
        # self.assertIsNone(self.q.get())
        self.assertTrue(self.q.get() is None)  # 2.1 - 2.6 support

        # When not empty
        val = ''.join(random.choice(string.ascii_uppercase + string.digits)
                      for x in range(32))
        self.q.conn.rpush(self.key, val)
        self.assertEqual(self.q.get(), val)

    def tearDown(self):
        self.q.conn.delete(self.key)


class StateCounterTest(unittest.TestCase):

    def setUp(self):
        self.key = "test_sc"
        self.sc = StateCounter(key=self.key, host='localhost', port=6379,
                               db=0)

    def test_str(self):
        self.assertEqual(str(self.sc), "State: 1\tCount: 0\tTotal: 0")

    def test_get_state(self):
        self.assertEqual(self.sc.get_state(), 1)

    def test_get_count(self):
        self.assertEqual(self.sc.get_count(), 0)

    def test_get_total(self):
        self.assertEqual(self.sc.get_total(), 0)

    def test_get_all(self):
        expected = {'count': '0', 'state': '1', 'total': '0'}
        actual = self.sc.get_all()

        self.assertEqual(actual, expected)

    def test_start(self):
        self.sc.conn.hset(self.key, 'state', 0)
        self.assertEqual(self.sc.get_state(), 0)
        self.sc.conn.hset(self.key, 'count', 100)
        self.assertEqual(self.sc.get_count(), 100)

        self.sc.start()

        self.assertEqual(self.sc.get_state(), 1)
        self.assertEqual(self.sc.get_count(), 0)

    def test_stop(self):
        self.assertEqual(self.sc.get_state(), 1)
        self.sc.conn.hset(self.key, 'count', 100)
        self.assertEqual(self.sc.get_count(), 100)
        self.assertEqual(self.sc.get_total(), 0)

        self.sc.stop()

        self.assertEqual(self.sc.get_state(), 0)
        self.assertEqual(self.sc.get_count(), 0)
        self.assertEqual(self.sc.get_total(), 100)

    def test_incr(self):
        self.assertEqual(self.sc.get_count(), 0)
        self.sc.incr()
        self.assertEqual(self.sc.get_count(), 1)

    def test_started(self):
        self.assertTrue(self.sc.started())
        self.sc.stop()
        self.assertFalse(self.sc.started())

    def test_stopped(self):
        self.assertFalse(self.sc.stopped())
        self.sc.stop()
        self.assertTrue(self.sc.stopped())

    def tearDown(self):
        self.sc.conn.delete(self.key)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
