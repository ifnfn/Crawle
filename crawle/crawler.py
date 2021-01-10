#!env python3
# -*- coding: utf-8 -*-

import sys
from .crawle import *


def onehone_main():
    OnehoneParser("data", 10)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv in parsers:
            parsers[sys.argv[1]('data', 400)
