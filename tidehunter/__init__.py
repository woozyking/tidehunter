#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = 'tidehunter'
__version__ = '0.1.0'
__author__ = 'Runzhou Li (Leo)'
__license__ = 'MIT'
__copyright__ = 'Copyright 2013 Addictive Tech Corp.'

from . import stream

# Set default logging handler to avoid "No handler found" warnings.
import logging

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):

        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
