#!env python3
# -*- coding: utf-8 -*-

import engine
import os

from books import *

def main_x8x8():
    craw = engine.Crawler(10)
    craw.AddEngine(X8Engine)
    craw.Load('data_all_only')
    craw.Fly()

    key = {}
    count = 0

    data_all = []
    for data in craw.data:
        ids = os.path.basename(data['url'][:-4])
        if ids not in key:
            count += 1
            key[ids] = data
            # print("%4d %10s %s %s" % (count, data['time'], data['url'], data['text']))
            data_all.append(data)
    craw.data = data_all

    print('count: ', len(data_all))

    craw.Save('data_all_only')


def data_test():
    data1 = engine.data_load('data_all_only')

    for data in data1:
        count += 1
        print("%4d %10s %s %s" % (count, data['time'], data['url'], data['text']))


def main_book():
    craw = engine.Crawler(12)
    craw.AddEngine(SokindleEngine)
    craw.Fly()


if __name__ == '__main__':
    # main_book()
    main_x8x8()
    # data_test()
