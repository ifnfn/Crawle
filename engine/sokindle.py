#! /usr/bin/python3
# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup as bs, Tag
import tornado.escape

from .engines import EngineBase, KolaParser
from .fetchTools import RegularMatchUrl


class ParserDoubanISBN(KolaParser):
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

        soup = bs(text['data'], "html.parser", exclude_encodings='UTF8')

        for info in soup.findAll("div", {"class": "info"}):
            href = info.findAll("a", {"onclick": re.compile('.*')})
            if href:
                data['douban'] = href[0]['href']

        return data


class ParserBookDetailed(KolaParser):
    """
    解析图书的详细信息
    http://www.kindlepush.com/book/17103
    """

    def __init__(self, url=None, data=None):
        super().__init__()
        if url:
            header = {}
            header["User-Agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36"
            header["Content-Type"] = "application/x-www-form-urlencoded"
            self.cmd['method'] = 'POST'
            self.cmd['body'] = "e_secret_key=523523"
            self.cmd['header'] = header
            self.cmd['source'] = url
            self.cmd['cache'] = True
            if data:
                self.cmd['private'] = data

    def cmd_parser(self, text):
        """
        解析
        <div class="item">
            <div class="bookpic">
                <img src="https://img3.doubanio.com/lpic/s29468916.jpg" title="庞贝三日"/>
            </div>
            <div class="bookinfo">
                <ul>
                    <li><strong>书名：</strong>庞贝三日</li>
                    <li><strong>作者：</strong>阿尔贝托・安杰拉</li>
                    <li><strong>格式：</strong>MOBI</li>
                    <li><strong>浏览：</strong>4370次</li>
                    <li><strong>标签：</strong><a href="https://sokindle.com/books/tag/lishi" rel="tag">历史</a> <a href="https://sokindle.com/books/tag/%e6%84%8f%e5%a4%a7%e5%88%a9" rel="tag">意大利</a> <a href="https://sokindle.com/books/tag/%e8%80%83%e5%8f%a4" rel="tag">考古</a></li>
                    <li><strong>时间：</strong>2017-06-19</li>
                    <li><strong>评分：</strong><b class="dbpf dbpf8"></b></li> <li><strong>ISBN：</strong>9787516185735</li>
                    <ul></ul>
                </ul>
            </div>
        </div>
        """

        data = {}
        if 'private' in text:
            data = text['private']
        soup = bs(text['data'], "html.parser", exclude_encodings='UTF8')

        secret_data = soup.findAll('div', {"class": "e-secret"})

        for secret in secret_data:
            password = re.findall("提取密码：(.*)", secret.text)
            if password:
                data["password"] = password[0]

        bookdata = soup.findAll('a', {"rel": "nofollow", "target": "_blank"})
        for bookinfo in bookdata:
            download = bookinfo['href']
            if "pan.baidu.com" in download:
                x = re.findall("url=(.*)", download)
                if x:
                    data["download"] = x[0]

        bookdata = soup.findAll('div', {"class": "item"})
        for bookinfo in bookdata:
            # print(bookinfo)
            img = bookinfo.findAll('img')
            if img:
                data["image"] = img[0]["src"]

            li = bookinfo.findAll('li')
            for l in li:
                # print(l.text)
                text = l.text

                author = re.findall("作者：(.*)", text)
                if author:
                    data["author"] = author[0]

                formats = re.findall("格式：(.*)", text)
                if formats:
                    data["formats"] = formats[0]

                count = re.findall("浏览：(.*)", text)
                if count:
                    data["count"] = count[0]

                category = re.findall("标签：(.*)", text)
                if category:
                    data["category"] = category[0]

                time = re.findall("时间：(.*)", text)
                if time:
                    data["time"] = time[0]

                douban = re.findall("豆瓣评分：(.*)", text)
                if douban:
                    data["douban"] = douban[0]

                isbn = re.findall("ISBN：(.*)", text)
                if isbn:
                    if 'ISBN: ' in isbn[0]:
                        isbn = re.findall("ISBN: (.*)", isbn[0])
                    if isbn:
                        data["isbn"] = isbn[0]

        if 'isbn' in data and data['isbn']:
            url = 'https://book.douban.com/subject_search?search_text=%s&cat=1001' % data['isbn']
            # print(url)
            ParserDoubanISBN(url, data).AddCommand()
        else:
            print("No found isbn")

        return None
        return data


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
        booksList = soup.findAll('div', {"class": "thumb-img focus"})
        for p in booksList:
            # print(p)
            x = p.findAll('a', {"title": re.compile('.*')})
            if x:
                book = {}
                book['href'] = x[0]['href']
                book['name'] = x[0]['title']

                # print(book)
                ParserBookDetailed(book['href'], book).AddCommand()

        # 下一页
        # <li class="next-page"><a href="https://sokindle.com/page/2">下一页</a></li>
        next_text = soup.findAll('li', {'class': 'next-page'})
        for aaa in next_text:
            # print(aaa.prettify())
            for url in aaa.findAll('a'):
                # print(url['href'])
                ParserBookList(url['href']).AddCommand()

        return None

# JD 搜索引擎


class SokindleEngine(EngineBase):
    def __init__(self):
        self.parserList = [
            ParserBookList(),
            ParserBookDetailed(),
            ParserDoubanISBN(),
        ]

    def Start(self):
        # url = "https://sokindle.com/books/4600.html"
        # ParserBookDetailed(url).AddCommand()

        url = 'https://sokindle.com'
        ParserBookList(url).AddCommand()

        # data = {}
        # data['isbn'] = '9787221124913'
        # ParserDoubanISBN('9787221124913', data).AddCommand()
        pass
