#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pycurl
import oauth2


class Hunter(object):

    def __init__(self, conf, sc, q):
        # stats
        # self.backoff = conf.get('backoff', 1)

        # flow control
        self.buffer = ""
        self.q = q
        self.sc = sc
        self.limit = conf.get('limit', 0)
        self.limit_bak = self.limit  # support tide_on() limit restore

        # connection
        self.conn = None
        self.url = str(conf['url'])
        self.delimiter = conf.get('delimiter', '\r\n')
        self.timeout = conf.get('timeout', 0)
        self.compressed = conf.get('compressed', True)

        # oauth
        oauth = conf.get('oauth')
        self.consumer = None
        self.token = None

        if oauth:
            self.consumer = oauth2.Consumer(
                key=oauth['consumer_key'], secret=oauth['consumer_secret'])
            self.token = oauth2.Token(
                key=oauth['token_key'], secret=oauth['token_secret'])

        # basic auth
        self.user = ''
        self.pw = ''

        if not self.consumer or not self.token:
            self.user = str(conf.get('user', ''))
            self.pw = str(conf.get('pass', ''))

        # setup connection
        self.setup_conn()

    def setup_conn(self):
        if self.conn:
            try:
                self.conn.close()
            except:  # pragma: no cover
                pass

            self.conn = None

        # reset buffer and record count
        self.buffer = ""

        # init curl
        self.conn = pycurl.Curl()
        self.conn.setopt(pycurl.URL, self.url)

        # Setup auth, oauth or basic
        if self.token and self.consumer:
            auth = get_oauth_header(self.consumer, self.token, self.url)
            self.conn.setopt(pycurl.HTTPHEADER, ['Authorization: %s' % auth])
        elif self.user and self.pw:
            auth = "%s:%s" % (self.user, self.pw)
            self.conn.setopt(pycurl.USERPWD, auth)

        # Other HTTP params
        if self.timeout > 0:
            self.conn.setopt(pycurl.CONNECTTIMEOUT, self.timeout)

        if self.compressed:
            self.conn.setopt(pycurl.ENCODING, 'gzip, deflate')

        # Incoming data handler
        self.conn.setopt(pycurl.WRITEFUNCTION, self._on_data_receive)

    def _on_data_receive(self, data):
        self.buffer += data

        if data.endswith(self.delimiter):
            q_data = self.buffer.strip()
            self.buffer = ""

            for j in iter_chunk(q_data, self.delimiter):
                if self.sc.started():
                    self.q.put(j)
                    self.sc.incr()

                if self.limit and self.sc.get_count() >= self.limit:
                    self.sc.stop()

        if self.sc.stopped():
            # the way to stop the stream, would raise pycurl.error
            # and pycurl also prints it regardless of handling the error
            return -1

    def tide_on(self, limit=None):
        # while self.sc.started():
        try:
            self.sc.start()
            self.q.put("{}")  # force reactivate queue
            self.setup_conn()

            if limit:
                self.limit = limit  # overwrite limit "on the fly"
            else:
                self.limit = self.limit_bak

            self.conn.perform()
        except pycurl.error as e:
            if e[0] == 23:
                pass  # pycurl prints this error regardless
            else:
                raise
        except:
            raise
        finally:
            # resets
            self.sc.stop()
            self.buffer = ""

        return self.conn.getinfo(pycurl.HTTP_CODE)


def get_oauth_header(consumer, token, url, method='GET'):
    """ Create and return OAuth header.
    """
    params = {'oauth_version': '1.0',
              'oauth_nonce': oauth2.generate_nonce(),
              'oauth_timestamp': int(time.time())}

    r = oauth2.Request(method=method, parameters=params, url=url)
    r.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)

    return r.to_header()['Authorization'].encode('utf-8')


def iter_chunk(data, delimiter):
    jstr_list = data.split(delimiter)

    for jstr in jstr_list:
        jstr = jstr.strip()

        if jstr:
            yield jstr
