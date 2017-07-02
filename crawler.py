#!env python3
# -*- coding: utf-8 -*-

""" 用于 """

import threading
import engine
import pymongo
import tornado.escape
import json
import re
import os


class Crawler:
    def __init__(self, thread_num=1):
        self.threads = []
        for _ in range(thread_num):
            self.threads.append(Work(self))

        self.tv = engine.KolaEngine()
        self.tv.Start()
        self.db = pymongo.MongoClient().sumfeel
        self.books = self.db.books
        self.b = []

    def Wait(self):
        for item in self.threads:
            item.start()
        for item in self.threads:
            if item.isAlive():
                item.join()

        file = open('data.json', 'w')
        text = tornado.escape.json_encode(self.b)
        file.write(text)
        file.close()

        for v in self.b:
            print(v['name'])

    def RunOne(self):
        cmd = self.tv.GetCommand()
        if cmd:
            data = self.tv.ProcessCommand(cmd, 3)
            if data:
                # print(data)
                # self.books.insert_one(data)
                # del data['_id']
                self.b.append(data)
            return True
        return False


class Work(threading.Thread):
    def __init__(self, crawler):
        super().__init__()
        self.crawler = crawler

    def run(self):
        while self.crawler.RunOne():
            pass


def main():
    craw = Crawler(4)
    craw.Wait()


if __name__ == '__main__':
    main()
