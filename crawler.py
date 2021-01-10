#!env python3
# -*- coding: utf-8 -*-

import sys
from crawle.parsers import *

def onehone_main():
    OnehoneParser("data_1hone")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '1hone':
            OnehoneParser("data_1hone")
        elif sys.argv[1] == 'caowo16':
            Caowo16Parser("data_caowo16")
        elif sys.argv[1] == 'x8x8':
            X8x8Parser('data_x8x8')
    else:
        OnehoneParser("data_1hone")