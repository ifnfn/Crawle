#!env python3
# -*- coding: utf-8 -*-

import sys
from crawle.parsers import *

def onehone_main():
    OnehoneParser("data")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '1hone':
            OnehoneParser("data", 100)
        elif sys.argv[1] == 'caowo16':
            Caowo16Parser("data")
    else:
        OnehoneParser("data", 10)