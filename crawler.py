#!env python3
# -*- coding: utf-8 -*-

import engine
import os

from books import X8Engine

def main():
    craw = engine.Crawler(10)
    craw.AddEngine(X8Engine)
    # craw.Load('data_all')
    craw.Fly()
    # craw.Save('data_1200')

def data_test():
    data1 = engine.data_load('data_all')
    data2 = engine.data_load('data_1200')
    for data in data2:
        data1.append(data)
    engine.data_save('data_all', data1)

    # count = 0
    # for data in data1:
    #     count += 1
    #     # print(data)
    #     print("%4d %10s %s %s" % (count, data['time'], data['url'], data['text']))



if __name__ == '__main__':
    main()
    # data_test()
