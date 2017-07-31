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

    def RunOne(self):
        book = None
        self.mutex.acquire()
        if self.id < self.lenght:
            book = self.books[self.id]
            self.id = self.id + 1
        self.mutex.release()

        if book != None:
            self.getId(book)
            self.putFile(book)
            # self.checkFile(book)

            return True

        return False

    def getId(self, book):
        book['id'] = ""
        ids = re.findall("/(\d*).html", book['href'])
        for i in ids:
            book['id'] = i

    def UploadQiniu(self, key, localFile):
        access_key = "LigcPM8yh3cnEtqIqiG8isRbUDDUA90pJa91lNSq"
        secret_key = "T0nIp2L9dWtSQd0FzruiFfVaZXMWggODeuJfQ9Tc"
        bucket_name = "books"

        q = qiniu.Auth(access_key, secret_key)

        bucket = qiniu.BucketManager(q)
        ret, info = bucket.stat(bucket_name, key)

        if not ret:  # and 'hash' in ret:
            token = q.upload_token(bucket_name)
            ret, info = qiniu.put_file(token, key, localFile)
            if ret is not None:
                print(key + ' -> Qiniu OK')
                return True
            else:
                print(info)

        return False

    def putFile(self, book):
        found = False

        if book['id'] != "":
            try:
                listfile = os.listdir("books/" + book['id'])
                for line in listfile:
                    key = book['id'] + ": " + line
                    localFile = "books/%s/%s" % (book['id'], line)
                    print(book['id'], book['name'])
                    self.UploadQiniu(key, localFile)
                    found = True
            except:
                pass
        if found == False:
            print(book['id'], "No found: " + book["href"])

        return found

    def checkFile(self, book):
        found = False
        if book['id'] != "":
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
    craw = Crawler(1).Wait()


if __name__ == '__main__':
    main()
