#! /usr/bin/python3
# -*- coding: utf-8 -*-

from engine import *
from bs4 import BeautifulSoup as bs
import os
import re
import sys
sys.path.append("../")

try:
    import urllib2 as urllib
except:
    from urllib.parse import urljoin

count = 0


class Caowo16List(KolaParser):
    def __init__(self, url=None):
        super().__init__()
        if url:
            self.cmd['source'] = url
            # self.cmd['cache'] = False

    def cmd_parser(self, text):
        data = {}
        if 'private' in text:
            data = text['private']

        soup = bs(text['data'], "html.parser", exclude_encodings='UTF8')
        # print(text['data'])

        for tc_nr in soup.findAll('div', {"class": "item"}):
            href = tc_nr.findAll('a')
            if href and href[0]['href'] != '/':
                data = {}
                data['href'] = urljoin(text['source'], href[0]['href'])
                data['text'] = href[0]['title']
                data['time'] = ''
                data['date'] = ''

                img = href[0].findAll('img', {"class": "thumb lazy-load"})
                if img:
                    data['img'] = img[0]['src']
                    Caowo16Detailed(data['href'], data).AddCommand()

        # 下一页
        # <li class="page-item disabled">
        next_url = ''
        for page in soup.findAll('a', {'class': 'page-link'}):
            if page.text == '»':
                next_url = urljoin(text['source'], page['href'])
                print(next_url)
                Caowo16List(next_url).AddCommand()
        if not next_url:
            self.Finish()

class Caowo16Detailed(KolaParser):
    def __init__(self, url=None, data=None):
        super().__init__()
        if url:
            self.cmd['source'] = url
            self.cmd['cache'] = True
            self.cmd['private'] = data

    def cmd_parser(self, text):
        global count

        data = {}
        if 'private' in text:
            data = text['private']

        soup = bs(text['data'], "html.parser", exclude_encodings='UTF8')

        # <div class="" id="cms_player"
        for v in soup.findAll('iframe', {}):
            data['url'] = v['src'][14:]
            print(os.path.basename(data['img']))
            # print(os.path.basename(data['img']), data['text'])
            break

        return data

class Caowo16Engine(EngineBase):
    def __init__(self):
        self.parserList = [
            Caowo16Detailed(),
            Caowo16List(),
        ]

    def Start(self):
        for i in range(19, 38):
            url = 'https://www.caowo16.com/index.php?s=/list-select-id-%d-type--area--year--star--state--order-addtime.html' % i
            Caowo16List(url).AddCommand()
