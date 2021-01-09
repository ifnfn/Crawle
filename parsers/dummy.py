#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os

from engine import *
from urllib.parse import urljoin


# 解析资源列表
class pageList(KolaParser):
    def cmd_parser(self, text):
        data = {}
        if 'private' in text:
            data = text['private']

        soup = self.Html(text['data'])

        # 从当前页提取每一条记录
        for item in soup.findAll('div', {"class": "item"}):
            print(item)
            data = {
                'text': '',
                'href': '',
                'img' : '',
                'time': '',
                'date': '',
                'url': ''
            }
            # TODO

            if data['href']:
                    pageDetailed(data['href'], data).AddCommand()

        # 提出下一页
        next_url = ''
        for page in soup.findAll('a', {'class': 'page-link'}):
            next_url = urljoin(text['source'], page['href'])
            print(next_url)
            pageList(next_url).AddCommand()

        if not next_url:
            self.Finish()


# 解析资源详细数据
class pageDetailed(KolaParser):
    def __init__(self, url=None, data=None):
        super().__init__()
        if url:
            self.cmd['source'] = url
            self.cmd['cache'] = True
            self.cmd['private'] = data

    def cmd_parser(self, text):
        data = {}
        if 'private' in text:
            data = text['private']

        soup = self.Html(text['data'])

        # <div class="" id="cms_player"
        for v in soup.findAll('iframe', {}):
            data['url'] = v['src'][14:]
            print(os.path.basename(data['img']))
            # print(os.path.basename(data['img']), data['text'])
            break

        return data

class DummyEngine(EngineBase):
    def __init__(self):
        self.parserList = [
            pageDetailed(),
            pageList(),
        ]

    def Start(self):
        url = 'https://......................'
        pageList(url).AddCommand()


def DummyParser(filename):
    craw = Crawler(16)
    craw.AddEngine(DummyEngine)
    craw.Load(filename)
    craw.Fly()

    key = {}
    count = 0

    data_all = []
    for data in craw.data:
        ids = data['url']
        if ids not in key:
            count += 1
            key[ids] = data
            # print("%4d %10s %s %s" % (count, data['time'], data['url'], data['text']))
            data_all.append(data)
    craw.data = data_all

    print('count: ', len(data_all))

    craw.Save(filename)
