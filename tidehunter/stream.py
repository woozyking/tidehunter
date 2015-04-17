#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.version_info[0] < 3:  # Python 2.x
    from Queue import Queue
else:  # Python 3.x
    from queue import Queue

import requests


class SimpleStateCounter(object):

    def __init__(self):
        self.count = 0
        self.total = 0
        self.state = 0

    def incr(self):
        self.state = 1
        self.count += 1

    def stop(self):
        self.total += self.count
        self.count = 0
        self.state = 0

    def start(self):
        self.total += self.count
        self.count = 0
        self.state = 1

    @property
    def started(self):
        return bool(self.state)

    @property
    def stopped(self):
        return not self.started

    def get_count(self):
        return self.count

    def get_state(self):
        return self.state

    def get_total(self):
        return self.total

    def clear(self):
        self.stop()
        self.total = 0


class Hunter(object):

    def __init__(self, url, q=None, sc=None, **kwargs):
        self.url = url

        if not q:
            q = Queue()

        self.q = q

        if not sc:
            sc = SimpleStateCounter()

        self.sc = sc

        if kwargs.get('stream'):
            del kwargs['stream']

        self.kwargs = kwargs

    def tide_on(self, limit=0):
        self.sc.start()

        r = requests.get(self.url, stream=True, **self.kwargs)

        for line in r.iter_lines():
            if self.sc.stopped:
                break

            if line:
                self.q.put(line, block=False)
                self.sc.incr()

            if limit > 0 and self.sc.get_count() >= limit:
                break

        r.close()
        self.sc.stop()

        return r
