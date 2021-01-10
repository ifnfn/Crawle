#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os

from crawle.engine import *
from urllib.parse import urljoin

class x8x8_pageList(HtmlParser):
    def cmd_parser(self, soup):
        # print(soup)
        for tc_nr in soup.find('main', {"id": "main"}).find('div', {"class": "lm_lb"}).findAll('li', {"class": ''}):
            href = tc_nr.find('a', {'name': "点击播放"})
            if href and href['href'] != '#':
                self.data['href'] = urljoin(self.url, href['href'])
                self.data['img'] = urljoin(self.url, href.find('img')['src'])
                self.data['text'] = tc_nr.find('p', ).find('a').text
                self.engine.Add(x8x8_pageDetailed(self.data['href'], self.data))


        # 下一页
        # <li class="page-item disabled">
        next_url = ''
        return False
        for page in soup.findAll('a', {'class': 'page-link'}):
            if page.text == '»':
                next_url = urljoin(self.url, page['href'])
                # print(next_url)
                self.engine.Add(x8x8_pageList(next_url, {}))
        if not next_url:
            self.Finish()


class x8x8_pageDetailed(HtmlParser):
    def cmd_parser(self, soup):
        # print(soup)
        v = soup.find('div', {'class': 's_p'}).find('span', {'id': 'downloadurl'})
        self.data['url'] = v.text
            # self.data['url'] = v['src'][14:]

        return True

def X8x8Parser(filename, max_count=0):
    craw = Crawler(thread_num=1, max_count=max_count)
    # craw.log = lambda data : print(data['id'], data['date'], data['text'], data['url'])

    url = 'https://8xrxt0.xyz/html/category/video/'

    craw.Add(x8x8_pageList(url))
    craw.Fly()
    craw.Save(filename)