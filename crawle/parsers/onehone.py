#! /usr/bin/python3
# -*- coding: utf-8 -*-

from crawle.engine import *
from urllib.parse import urljoin

class ListPage(HtmlParser):
    def cmd_parser(self, soup):
        for tc_nr in soup.findAll('li', {"class": "col-list"}):
            self.data = {
                'text': '',
                'href': '',
                'img' : '',
                'time': '',
                'date': '',
                'url': ''
            }

            hrefs = tc_nr.findAll('a')
            img = hrefs[0].findAll('img', {'class': 'lazyload'})
            self.data['img'] = img[0]['data-src']
            self.data['href'] = hrefs[1]['href']
            self.data['text'] = hrefs[1].text
            # print(self.data)
            self.engine.Add(DetailedPage(self.data['href'], self.data))

        # 下一页
        next_url = ''
        for page in soup.findAll('div', {'class': 'my_titlexpage'}):
            for href in page.findAll('a', {}):
                if href.text == '下一页':
                    next_url = urljoin(self.url, href['href'])
                    # print(next_url)
                    self.engine.Add(ListPage(next_url))
        if not next_url:
            self.engine.Finish()

        return False


class DetailedPage(HtmlParser):
    def cmd_parser(self, soup):
        # print(soup)

        ziliao = soup.findAll('ul', {'class': 'about_ul'})
        for li in ziliao[0].findAll('li', {}):
            key = li.text.split('：')
            if key[0] == '更新':
                self.data['date'] = key[1]
            else:
                self.data[key[0]] = key[1]

        for v in soup.findAll('ul', {'class': 'playerlist'}):
            for data_purl in v.findAll('li', {}):
                url = data_purl['data_purl'].split('?url=')
                if len(url) > 0:
                    self.data['url'] = url[0]
                    break
            break

        return True

def OnehoneParser(filename):
    craw = Crawler(thread_num=1, max_count=400)
    craw.log = lambda data : print(data['id'], data['date'], data['text'], data['url'])

    url = 'https://www.1hone.com/list_0_1_0_0_0_1.html'
    craw.Add(ListPage(url))
    craw.Fly()
    craw.Save(filename)
