#! /usr/bin/python3
# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup as bs, Tag
import tornado.escape

from .engines import EngineBase, KolaParser
from .fetchTools import RegularMatchUrl


class ParserBookDetailed(KolaParser):
    """
    解析图书的详细信息
    http://www.kindlepush.com/book/17103
    """

    def __init__(self, url=None, data=None):
        super().__init__()
        if url:
            self.cmd['source'] = url
            self.cmd['cache'] = True
            if data:
                self.cmd['private'] = data

    def cmd_parser(self, text):
        """
        解析
        """
        data = text['private']
        soup = bs(text['data'], "html.parser", exclude_encodings='UTF8')

        bookdata = soup.findAll(
            'div', {"class": "m-bookdata j-bookdata f-cb"})

        for bookinfo in bookdata:
            img = bookinfo.findAll('img')
            if img:
                data["image"] = img[0]["src"]

            info = bookinfo.findAll('div', {"class": "data"})
            if info:
                text = info[0].prettify()
                # print(text)
                # continue

                author = re.findall("作者：(.*)", text)
                if author:
                    data["author"] = author[0]

                douban = re.findall("豆瓣评分：(.*)", text)
                if douban:
                    data["douban"] = douban[0]

                shared = re.findall("分享人：([\s\S].*)", text)
                if shared:
                    data["shared"] = shared[0]

                category = re.findall("类型：『(.*)』", text)
                if category:
                    data["category"] = category[0]

            print(data)

        order = soup.findAll(
            'div', {"class": "m-order j-order"})

        intro = soup.findAll(
            'article', {"class": "intro"})

        # print(bookdata)
        # print(order)
        # print(intro)
        return True, data


class ParserBookList(KolaParser):
    """
    图书列表解析器
    """

    def __init__(self, url=None):
        super().__init__()
        if url:
            self.cmd['source'] = url
            self.cmd['cache'] = True
            # self.cmd['regular'] = ['(<h6.*?>[\s\S]*?</h6>|<a href=.*class="next".*</a>)']

    def cmd_parser(self, text):
        """
        解析
        <a href="http://book.zi5.me/archives/book/1311" class="colorbox cboxElement" id="cb1311"><div style="position:relative;"> <img class="bookcover" src="/thumb-1311-254-200.jpg" style="height:254px;"> <span class="bookcoverlink">点击查看<br><sup>shift+左键新窗口查看</sup></span> <span class="rateNumbook" title="豆瓣平均评分">8.3</span></div><div class="thumbtitle">胭脂扣</div></a>
        """

        soup = bs(text['data'], "html.parser")  # , from_encoding = 'GBK')
        data = []
        booksList = soup.findAll('a', {"class": "colorbox cboxElement"})
        for p in booksList:
            book = {}
            book['href'] = p['href']
            book['name'] = p.text
            print(book)

            ParserBookDetailed(p['href'], book).Execute()
            data.append(book)

        # 下一页
        # <a href="http://www.kindlepush.com:80/category/-1/0/2" class="next " hidefocus="hidefocus">下一页</a>
        # next_text = soup.findAll(
        #     'a', {'class': 'next', "hidefocus": "hidefocus"})
        # for a in next_text:
        #     href = a.attrs['href']
        #     ParserBookList(href).Execute()

        return True, None

# JD 搜索引擎


class Zi5Engine(EngineBase):
    def __init__(self):
        super().__init__()

        self.engine_name = 'KindlePush'

        self.parserList = [
            ParserBookDetailed(),
            ParserBookList(),
        ]

    def Start(self):
        url = 'http://book.zi5.me/archives/book-gentre/xdwx'
        ParserBookList(url).Execute()
