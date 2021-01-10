#! /usr/bin/python3
# -*- coding: utf-8 -*-

from crawle.engine import *
from urllib.parse import urljoin
import hashlib
import json
class onehone_ListPage(HtmlParser):
    def cmd_parser(self, soup):
        # print(soup)
        for tc_nr in soup.findAll('li', {"class": "col-list"}):
            hrefs = tc_nr.findAll('a', {'target': '_blank'})
            img = hrefs[0].find('img', {'class': 'lazyload'})
            self.data['img'] = img['data-src']
            self.data['href'] = hrefs[1]['href']
            self.data['text'] = hrefs[1].text
            # print(self.data)

            self.engine.Add(onehone_DetailedPage(self.data['href'], self.data))

        # 下一页
        next_url = ''
        for href in soup.find('div', {'class': 'my_titlexpage'}).findAll('a', {}):
            if href.text == '下一页':
                next_url = urljoin(self.url, href['href'])
                # print(next_url)
                self.engine.Add(onehone_ListPage(next_url))

        if not next_url:
            self.engine.Finish()

        # 返回 True, 表示解析到完整的数据， False，返回未完成的数据，或者无效数据
        return False


class onehone_DetailedPage(HtmlParser):
    def cmd_parser(self, soup):
        # print(soup)

        ziliao = soup.find('ul', {'class': 'about_ul'})
        for li in ziliao.findAll('li', {}):
            key = li.text.split('：')
            if key[0] == '更新':
                self.data['date'] = key[1]
            else:
                self.data[key[0]] = key[1]

        ul = soup.find('ul', {'class': 'playerlist'})
        for data_purl in ul.findAll('li', {}):
            url = data_purl['data_purl'].split('?url=')
            if len(url) == 2:
                self.data['url'] = url[1]
            else:
                self.data['url'] = data_purl['data_purl']
            break

        # 返回 True, 表示解析到完整的数据， False，返回未完成的数据，或者无效数据
        return True

def OnehoneParser(filename, max_count=0):
    craw = Crawler(thread_num=1, max_count=max_count)
    craw.log = lambda data : print(data['id'], data['date'], data['text'], data['url'])
    craw.Load(filename)

    url = 'https://www.1hone.com/list_0_1_0_0_0_1.html'
    craw.Add(onehone_ListPage(url))
    craw.Fly()
    craw.Save(filename)
    # for _, d in craw.data.items():
    #     craw.log(d)

