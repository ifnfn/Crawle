#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.command.build_ext import build_ext as _build_ext
from distutils.core import Extension
import os
import sys
import platform
from codecs import open  # To use a consistent encoding

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

APP_NAME = 'html-crawle'

settings = dict()

settings.update(
    name=APP_NAME,
    version="1.0.1",
    description='HTML parser tools, crawle data framework.',
    author='Zhuzhg',
    author_email='zzg@ifnfn.com',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4'
    ],

    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'crawler = crawle.crawler:onehone_main',
        ],
    },

    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
)

setup(**settings)
