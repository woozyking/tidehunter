#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import requests
from random import randint

import sys
import os

target_path = os.path.join(os.path.dirname(__file__), '..', 'tidehunter')
sys.path.append(target_path)

# Test Targets
from stream import Hunter


class DummyQueue(object):

    def put(self, var, block=True):
        pass


class HunterTest(unittest.TestCase):

    def setUp(self):
        url = 'https://httpbin.org/stream/20'
        q = DummyQueue()
        self.hunter = Hunter(url=url, q=q)

    def test_tide_on(self):
        try:
            limit = randint(1, 19)
            r = self.hunter.tide_on(limit)
            self.assertIsInstance(r, requests.models.Response)
            self.assertEqual(self.hunter.sc.get_total(), limit)

            limit2 = randint(1, 19)
            r = self.hunter.tide_on(limit2)
            self.assertIsInstance(r, requests.models.Response)
            self.assertEqual(self.hunter.sc.get_total(), limit + limit2)

            r = self.hunter.tide_on()
            self.assertIsInstance(r, requests.models.Response)
            self.assertEqual(self.hunter.sc.get_total(), limit + limit2 + 20)
        except requests.exceptions.ConnectionError:
            pass  # this could happen


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
