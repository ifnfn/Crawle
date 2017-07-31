#!env python3
# -*- coding: utf-8 -*-
# flake8: noqa

""" 用于 """

import threading
import engine
import pymongo
import tornado.escape
import json
import re
import os
import subprocess
import qiniu
import qiniu.config


class Crawler:
    def __init__(self, thread_num=1):
        self.threads = []
        for _ in range(thread_num):
            self.threads.append(Work(self))

        file = open('data.json')
        self.books = json.load(file)
        file.close()

        self.id = 0
        self.lenght = len(self.books)
        self.mutex = threading.Lock()

    def Wait(self):
        for item in self.threads:
            item.start()
        for item in self.threads:
            if item.isAlive():
                item.join()

        # for v in self.b:
        #     print(v['name'])
            # text = tornado.escape.json_encode(v)
            # print(text)

        # file = open('data.json', 'w')
        # text = tornado.escape.json_encode(self.b)
        # file.write(text)
        # file.close()
        # print(self.b)

    def RunOne(self):
        book = None
        self.mutex.acquire()
        if self.id < self.lenght:
            book = self.books[self.id]
            self.id = self.id + 1
        self.mutex.release()

        if book != None:
            self.getId(book)
            if not self.checkFile(book):
                print(book['name'])
                self.Download(book)

            return True

        return False

    def getId(self, book):
        book['id'] = ""
        ids = re.findall("/(\d*).html", book['href'])
        for i in ids:
            book['id'] = i

    def Download(self, book):
        if 'download' in book and 'password' in book and book['id'] != "":
            secret = "--secret=%s" % book['password']
            dirs = "--dir=books/%s" % book['id']
            url = book['download']
            print(url)
            subprocess.Popen(["bd", "download", url, secret, dirs]).wait()

            return True

        return False

    def checkFile(self, book):
        found = False
        try:
            listfile = os.listdir("books/" + book['id'])
            for line in listfile:
                key = book['id'] + ": " + line
                localFile = "books/%s/%s" % (book['id'], line)
                found = True
        except:
            pass

        if found == False:
            print("No found: " + book["href"])
        return found


class Work(threading.Thread):
    def __init__(self, crawler):
        super().__init__()
        self.crawler = crawler

    def run(self):
        while self.crawler.RunOne():
            pass


def main():
    craw = Crawler(10).Wait()


if __name__ == '__main__':
    main()
