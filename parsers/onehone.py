#! /usr/bin/python3
# -*- coding: utf-8 -*-

from engine import *
from urllib.parse import urljoin

class pageList(KolaParser):
    def cmd_parser(self, text):
        data = {}
        if 'private' in text:
            data = text['private']

        soup = self.Html(text['data'])

        for tc_nr in soup.findAll('li', {"class": "col-list"}):
            data = {
                'text': '',
                'href': '',
                'img' : '',
                'time': '',
                'date': '',
                'url': ''
            }

            hrefs = tc_nr.findAll('a')
            img = hrefs[0].findAll('img', {'class': 'lazyload'})
            data['img'] = img[0]['data-src']
            data['href'] = hrefs[1]['href']
            data['text'] = hrefs[1].text

            pageDetailed(data['href'], data).AddCommand()

        # 下一页
        next_url = ''
        for page in soup.findAll('div', {'class': 'my_titlexpage'}):
            for href in page.findAll('a', {}):
                if href.text == '下一页':
                    next_url = urljoin(text['source'], href['href'])
                    print(next_url)
                    pageList(next_url).AddCommand()
        if not next_url:
            self.Finish()


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
        # print(soup)

        ziliao = soup.findAll('ul', {'class': 'about_ul'})
        for li in ziliao[0].findAll('li', {}):
            key = li.text.split('：')
            if key[0] == '更新':
                data['date'] = key[1]
            else:
                data[key[0]] = key[1]

        for v in soup.findAll('ul', {'class': 'playerlist'}):
            for data_purl in v.findAll('li', {}):
                url = data_purl['data_purl'].split('?url=')[1]
                if url:
                    data['url'] = url
                    break
            break

        print(data['date'], data['text'], data['url'])
        # print(data)

        return data

class OnehoneEngine(EngineBase):
    def __init__(self):
        self.parserList = [
            pageDetailed(),
            pageList(),
        ]

    def Start(self):
        url = 'https://www.1hone.com/list_0_1_0_0_0_1.html'
        pageList(url).AddCommand()


def OnehoneParser(filename):
    craw = Crawler(16)
    craw.AddEngine(OnehoneEngine)
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
