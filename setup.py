#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'tidehunter'
]

requires = [
    "pycurl>=7.18.1",
    "oauth2>=1.5.211",
    "redis>=2.7.6",
    "hiredis>=0.1.1"
]

import tidehunter

setup(
    name='tidehunter',
    version=tidehunter.__version__,
    description='HTTP streaming toolbox with flow control.',
    long_description=open('README.md').read(),
    author=tidehunter.__author__,
    author_email='runzhou.li@gmail.com',
    url='https://github.com/amoa/tidehunter',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'tidehunter': 'tidehunter'},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
    ),
)
