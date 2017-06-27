#!env python3
# -*- coding: utf-8 -*-

import base64
import hashlib
import os
import sys
import traceback
import zlib
import re

import httplib2


global headers

MAX_TRY = 3
socket_timeout = 30

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive': '115',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
}


def fetch_httplib2(url, method='GET', data=None, header=headers, cookies=None, referer=None, acceptencoding=None):
    if cookies and cookies != 'none':
        header['Cookie'] = cookies
    if referer:
        header['referer'] = referer
    if acceptencoding == None or acceptencoding == 'default':
        header['Accept-Encoding'] = 'gzip, deflate'
    else:
        header['Accept-Encoding'] = acceptencoding

    if method == 'POST':
        header['Content-Type'] = 'application/x-www-form-urlencoded'
    conn = httplib2.Http('.cache', timeout=socket_timeout)
    conn.follow_redirects = True
    response, responses = conn.request(uri=url, method=str(
        method).upper(), body=data,  headers=header)
    try:
        content_type = response['content-type']
    except:
        content_type = ''
    try:
        location = response['location']
    except:
        location = ''

    if 'referer' in headers:
        headers.pop('referer')
    if 'Cookie' in headers:
        headers.pop('Cookie')

    return response['status'], content_type, location, responses


def get_cache(url):
    filename = './cache/' + hashlib.md5(url.encode('utf8')).hexdigest().upper()
    exists = os.path.exists(filename)
    response = None

    if exists:
        f = open(filename, 'rb')
        response = f.read()
        f.close()
        print(filename, url)

    return response, exists


def save_cache(url, response):
    filename = './cache/' + hashlib.md5(url.encode('utf8')).hexdigest().upper()
    try:
        f = open(filename, 'wb')
        f.write(response)
        f.close()
    except:
        pass


def get_url(url, times=0):
    if times > MAX_TRY:
        return '', False
    try:
        status, _, _, response = fetch_httplib2(url)
        if status != '200' and status != '304' and status != '404':
            print('status %s, try %d ...' % (status, times + 1))
            return get_url(url, times + 1)
        return response, True
    except:
        t, v, tb = sys.exc_info()
        print("get_url: %s %s, %s, %s" %
              (url, t, v, traceback.format_tb(tb)))
        return get_url(url, times + 1)


def post_url(url, header={}, data=None, cached=False, times=0):
    if times > MAX_TRY:
        return '', False
    try:
        status, _, _, response = fetch_httplib2(url, 'POST', data, header)
        if status != '200' and status != '304' and status != '404':
            print('status %s, try %d ...' % (status, times + 1))
            return post_url(url, method, header, data, cached, times + 1)
        return response, True
    except:
        print("try: ", url)
        return post_url(url, header, data, cached, times + 1)


def fetch(url, method, header={}, data=None, cached=False):
    exists = False
    response = None

    if cached:
        response, exists = get_cache(url)

    if method == None:
        method = "GET"

    if not exists:
        if method.upper() == "POST":
            response, exists = post_url(url, header, data, cached)
        else:
            response, exists = get_url(url)
        if exists:
            save_cache(url, response)
    return response, exists


def RegularMatch(regular, text):
    x = ''
    for r in regular:
        res = re.finditer(r, text)
        if (res):
            for i in res:
                if type(i.group(1)) == bytes:
                    x += i.group(1).decode("GB18030") + '\n'
                else:
                    x += i.group(1) + '\n'
            text = x
    if x:
        x = x[0:len(x) - 1]
    return x


def RegularMatchUrl(url, regular):
    response, _ = fetch(url, "GET", cached=True)
    # 对数据 response 转码
    coding = 'utf8'
    try:
        if type(response) == bytes:
            response = response.decode(coding)
    except:
        coding = 'GB18030'
        if type(response) == bytes:
            response = response.decode(coding)

    return RegularMatch([regular], response)


if __name__ == '__main__':
    # url = 'http://store.tv.sohu.com/view_content/movie/5008825_704321.html'
    # url = 'http://index.tv.sohu.com/index/switch-aid/1012657'
    # url = 'http://www.kolatv.com/'
    # _, _, _, response = fetch_httplib2(url)
    # print(response.decode())

    # url = "http://127.0.0.1:8080/get"
    url = "https://sokindle.com/books/4660.html"
    data = "e_secret_key=523523"

    header = {}
    header["User-Agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36"
    header["Content-Type"] = "application/x-www-form-urlencoded"

    response, found = fetch(url, "GET", cached=False)
    print(response.decode())

    response, found = fetch(url, "POST", header, data, False)
    # response, responses = conn.request(
    #     uri=url, method="POST", body=data, headers=header)
    # try:
    #     content_type = response['content-type']
    # except:
    #     content_type = ''
    print(response.decode())
