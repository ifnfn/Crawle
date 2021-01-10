#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os

from crawle.engine import *
from urllib.parse import urljoin

class caowo16_pageList(HtmlParser):
    def cmd_parser(self, soup):
        for tc_nr in soup.findAll('div', {"class": "item"}):
            href = tc_nr.find('a')
            if href and href['href'] != '/':
                self.data['href'] = urljoin(self.url, href['href'])
                self.data['text'] = href['title']
                self.data['time'] = ''
                self.data['date'] = ''

                self.data['img'] = href.find('img', {"class": "thumb lazy-load"})['src']
                self.engine.Add(caowo16_pageDetailed(self.data['href'], self.data))

        # 下一页
        # <li class="page-item disabled">
        next_url = ''
        for page in soup.findAll('a', {'class': 'page-link'}):
            if page.text == '»':
                next_url = urljoin(self.url, page['href'])
                # print(next_url)
                self.engine.Add(caowo16_pageList(next_url, {}))
        if not next_url:
            self.Finish()


class caowo16_pageDetailed(HtmlParser):
    def cmd_parser(self, soup):
        iframe = soup.find('iframe', {})

        url = iframe['src'].split('?url=')

        if len(url) == 2:
            self.data['url'] = url[1]

            return True

def Caowo16Parser(filename, max_count=0):
    craw = Crawler(thread_num=1, max_count=max_count)
    # craw.log = lambda data : print(data['id'], data['date'], data['text'], data['url'])

    url = 'https://www.caowo16.com/index.php?s=/list-select-id-19-type--area--year--star--state--order-addtime.html'

    craw.Add(caowo16_pageList(url))
    craw.Fly()
    craw.Save(filename)