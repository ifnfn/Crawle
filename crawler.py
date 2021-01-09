#!env python3
# -*- coding: utf-8 -*-

import engine
import os

from parsers import *


def data_show(filename):
    data1 = engine.data_load(filename)
    count = 0

    for data in data1:
        count += 1
        if 'time' in data:
            print("%4d %10s %s %s" % (count, data['time'], data['url'], data['text']))
        else:
            print("%4d %s %s" % (count, data['url'], data['text']))

if __name__ == '__main__':
    # SokindleParser()
    #X8Parser('data/data_all_only_x8x8')
    Caowo16Parser('data/data_all_only_caowo16')
    # data_show('data/data_all_only_caowo16')
