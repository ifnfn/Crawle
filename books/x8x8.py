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


class X8List(KolaParser):
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

        i = 0
        for tc_nr in soup.findAll('div', {"class": "tc_nr l_b"}):
            for li in tc_nr.findAll('li'):
                for videoinfo in li.findAll('div', {"class": "w_z"}):
                    href = videoinfo.findAll('a')
                    if href and href[0]['href'] != '/':
                        data = {}
                        data['href'] = urljoin(text['source'], href[0]['href'])
                        data['text'] = href[0].text

                        img = li.findAll('img', {"class": "lazy"})
                        data['img'] = img[0]['data-original']
                        data['id'] = os.path.basename(data['img'][:-4])

                        span = li.findAll('span')
                        data['time'] = span[0].text
                        data['date'] = span[1].text

                        # if len(data['id']) != 32:
                        X8Detailed(data['href'], data).AddCommand()
                        i += 1

        # self.Finish()
        # return
        # 下一页
        for page in soup.findAll('a', {'class': 'pagenum extend'}):
            if page.text == '下一页' and page['href'] != 'page_20000.html':
                next_url = urljoin(text['source'], page['href'])
                print(next_url)
                X8List(next_url).AddCommand()
            else:
                self.Finish()


class X8Detailed(KolaParser):
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

        for v in soup.findAll('span', {"id": "vpath"}):
            vservers = ["https://aikantp.com/v/", "https://jiuktp.com/v/"]
            url_0 = urljoin(vservers[0], v.text)
            url_1 = urljoin(vservers[1], v.text)
            data['m3u8'] = [url_0, url_1]
            data['id2'] = os.path.basename(v.text[:-11])
            break

        for v in soup.findAll('div', {"class": "x_z"}):
            x = v.findAll(
                'a', {'rel': "noopener noreferrer", 'target': "_self"})
            if x:
                if x[0]['href'] != '#':
                    data['url'] = x[0]['href']
                    break

        if 'url' in data and data['url']:
            count += 1
            # print("%4d %s %10s %s %s" % (count, data['date'], data['time'], data['url'], data['text']))
            print("%4d %s %10s %s %s" % (count, data['date'], data['time'], data['url'], ''))

            return data


class X8Engine(EngineBase):
    def __init__(self):
        self.parserList = [
            X8Detailed(),
            X8List(),
        ]

    def Start(self):
        url = 'https://8atw.com/html/category/video/'

        # text, ret = get_url('https://8x8x.com')
        # print(text)
        # if ret:
        #     soup = bs(text, "html.parser", exclude_encodings='UTF8')
        #     for v in soup.findAll('span', {"class": "abc"}):
        #         urls = v.findAll('a')
        #         if urls:
        #             url = urljoin(urls[0]['href'], 'html/category/video/')

        url = 'https://8bwj.com/html/category/video/page_724.html'
        # url = 'https://8aam.com/html/category/video/page_1.html'
        # # url = 'https://8aam.com/html/category/video/page_1220.html'
        X8List(url).AddCommand()
