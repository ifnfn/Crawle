#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import traceback
import queue
import threading
import hashlib
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from .fetchTools import *


MAX_TRY = 3

class HtmlParser:
    """
    网页解析器
    """

    def __init__(self, url=None, data={}):
        self.url = url
        self.method = "GET"
        self.body = {}
        self.header = {}
        self.cached = True
        self.data = data.copy()

        self.engine = None
        self.cmd = {}
        self.name = self.__class__.__module__ + '.' + self.__class__.__name__
        self.cmd['engine'] = self.name
        self.cmd['cache'] = True
        if url:
            self.cmd['source'] = url


    def Finish(self):
        pass

    def cmd_parser(self, text, data={}):
        return None


    def Html(self, text):
        return bs(text, "html.parser", exclude_encodings='UTF8')


    def Process(self):
        response, found = fetch(self.url, self.method, self.header, self.body, self.cached)
        if found == False:
            return None

        # 对数据 response 转码
        coding = 'utf8'
        try:
            if type(response) == bytes:
                response = response.decode(coding)
        except:
            coding = 'GB18030'
            if type(response) == bytes:
                response = response.decode(coding)

        if response:
            if type(response) == bytes:
                response = response.decode(coding)

            soup = bs(response, "html.parser", exclude_encodings='UTF8')

            if self.cmd_parser(soup):
                self.engine.AppendData(self.data)

        else:
            print("[WARNING] Data is empty", self.url)

class Crawler:
    def __init__(self, thread_num=1, max_count=0):
        self.page_queue = queue.Queue()
        self.quit = False
        self.count = max_count
        self.log = lambda data : print(data['id'], data['text'], data['url'])

        self.threads = []
        for _ in range(thread_num):
            self.threads.append(Work(self))

        self.data = {}
        self.index = 0


    def AppendData(self, data):
        if self.count == 0 or self.index < self.count:
            hash_str = hashlib.md5(json.dumps(data).encode()).hexdigest()
            if hash_str not in self.data:
                data['id'] = self.index
                data['hash'] = hash_str
                self.data[hash_str] = data

                self.index += 1
                if self.log:
                    self.log(data)
        else:
            self.quit = True


    def Add(self, page):
        page.engine = self
        if not self.quit:
            self.page_queue.put(page)

    def Get(self):
        ret = None
        while not ret:
            try:
                ret = self.page_queue.get(True, 3)
            except:
                if self.quit:
                    return None

        return ret

    def Save(self, filename):
        with gzip.open(filename, 'wb') as fil:
            pickle.dump(self.data, fil)

    def Load(self, filename):
        if os.path.exists(filename):
            with gzip.open(filename, 'rb') as fil:
                self.data = pickle.load(fil)

    def Finish(self):
        self.quit = True

    def Fly(self):
        for item in self.threads:
            item.start()
        for item in self.threads:
            item.join()
        print("Finish!")

    def RunOne(self):
        page = self.Get()
        if page:
            page.Process()
            return True

        return False


class Work(threading.Thread):
    def __init__(self, crawler):
        super().__init__()
        self.crawler = crawler

    def run(self):
        while self.crawler.RunOne():
            pass
